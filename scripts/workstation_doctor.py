#!/usr/bin/env python3
"""Compare a workstation's installed custom capabilities with the repo baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


IGNORED_NAMES = {".DS_Store", "__pycache__"}
MACOS_HOME_PATH = re.compile(rb"/Users/[^/\s`'\"<>]+/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--plugin-state-json", type=Path)
    parser.add_argument("--host-overlay", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return "missing"
    if root.is_file():
        mode = root.stat().st_mode & 0o777
        digest.update(f"file\0.\0{mode:o}\0".encode("utf-8"))
        with root.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if any(part in IGNORED_NAMES for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"symlink\0{relative}\0{os.readlink(path)}\0".encode("utf-8"))
        elif path.is_file():
            mode = path.stat().st_mode & 0o777
            digest.update(f"file\0{relative}\0{mode:o}\0".encode("utf-8"))
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        elif path.is_dir():
            digest.update(f"dir\0{relative}\0".encode("utf-8"))
    return digest.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def file_content_digest(path: Path) -> str:
    if not path.is_file():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def policy_check(expected: Path, actual: Path) -> Dict[str, Any]:
    expected_digest = file_content_digest(expected)
    actual_digest = file_content_digest(actual)
    actual_mode = f"{actual.stat().st_mode & 0o777:o}" if actual.exists() else "missing"
    matches = expected_digest == actual_digest and actual_mode == "600"
    return {
        "kind": "global-policy",
        "name": "AGENTS.md",
        "status": "pass" if matches else "drift",
        "expectedDigest": expected_digest,
        "actualDigest": actual_digest,
        "expectedMode": "600",
        "actualMode": actual_mode,
    }


def plugin_state(path: Path | None) -> Dict[str, Any]:
    if path is not None:
        return load_json(path)
    result = subprocess.run(
        ["codex", "plugin", "list", "--available", "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Unable to read Codex plugin state.")
    return json.loads(result.stdout)


def digest_check(kind: str, name: str, expected: Path, actual: Path) -> Dict[str, Any]:
    expected_digest = tree_digest(expected)
    actual_digest = tree_digest(actual)
    return {
        "kind": kind,
        "name": name,
        "status": "pass" if expected_digest == actual_digest else "drift",
        "expectedDigest": expected_digest,
        "actualDigest": actual_digest,
    }


def portable_source_check(name: str, source: Path) -> Dict[str, Any]:
    affected: List[str] = []
    if source.exists():
        candidates = [source] if source.is_file() else sorted(source.rglob("*"))
        for path in candidates:
            if any(part in IGNORED_NAMES for part in path.relative_to(source).parts):
                continue
            if path.is_symlink():
                content = os.readlink(path).encode("utf-8", errors="replace")
            elif path.is_file():
                try:
                    content = path.read_bytes()
                except OSError:
                    continue
            else:
                continue
            if MACOS_HOME_PATH.search(content):
                affected.append("." if path == source else path.relative_to(source).as_posix())
    return {
        "kind": "portable-source",
        "name": name,
        "status": "pass" if not affected else "drift",
        "workstationSpecificPathFiles": affected,
    }


def build_report(
    repo_root: Path,
    codex_home: Path,
    manifest: Dict[str, Any],
    state: Dict[str, Any],
    host_overlay: Dict[str, Any],
) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    policy_source = repo_root / manifest["globalPolicy"]
    checks.append(policy_check(policy_source, codex_home / "AGENTS.md"))

    for name, configured_path in sorted(host_overlay.get("repositoryRoots", {}).items()):
        present = Path(configured_path).expanduser().is_dir()
        checks.append(
            {
                "kind": "repository-root",
                "name": name,
                "status": "pass" if present else "drift",
                "expectedPresent": True,
                "actualPresent": present,
            }
        )

    for skill in manifest.get("standaloneSkills", []):
        skill_source = repo_root / skill["source"]
        checks.append(
            digest_check(
                "standalone-skill",
                skill["name"],
                skill_source,
                codex_home / "skills" / skill["name"],
            )
        )
        checks.append(portable_source_check(f"standalone-skill:{skill['name']}", skill_source))

    installed = {item.get("name"): item for item in state.get("installed", [])}
    for plugin in manifest.get("plugins", []):
        if plugin.get("required", True) is False:
            continue
        observed = installed.get(plugin["name"])
        source_root_name = plugin.get("sourceRoot", "codex-skills")
        if source_root_name == "codex-skills":
            source_root = repo_root
        else:
            source_root = Path(host_overlay.get("repositoryRoots", {}).get(source_root_name, ""))
        expected_source = source_root / plugin["source"]
        expected_digest = tree_digest(expected_source)
        actual_digest = "missing"
        observed_version = None
        observed_enabled = False
        if observed is not None:
            observed_version = observed.get("version")
            observed_enabled = bool(observed.get("enabled"))
            source_path = observed.get("source", {}).get("path")
            if source_path:
                actual_digest = tree_digest(Path(source_path))
        matches = (
            observed is not None
            and observed_version == plugin["version"]
            and observed_enabled == bool(plugin.get("enabled", True))
            and actual_digest == expected_digest
        )
        checks.append(
            {
                "kind": "plugin",
                "name": plugin["name"],
                "status": "pass" if matches else "drift",
                "expectedVersion": plugin["version"],
                "actualVersion": observed_version,
                "expectedEnabled": bool(plugin.get("enabled", True)),
                "actualEnabled": observed_enabled,
                "expectedDigest": expected_digest,
                "actualDigest": actual_digest,
            }
        )
        checks.append(portable_source_check(f"plugin:{plugin['name']}", expected_source))

    status = "pass" if all(check["status"] == "pass" for check in checks) else "drift"
    return {"schemaVersion": 1, "status": status, "checks": checks}


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    codex_home = args.codex_home.expanduser().resolve()
    manifest_path = args.manifest or repo_root / "config" / "workstation-baseline.json"
    try:
        host_overlay = load_json(args.host_overlay) if args.host_overlay else {}
        report = build_report(
            repo_root,
            codex_home,
            load_json(manifest_path),
            plugin_state(args.plugin_state_json),
            host_overlay,
        )
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"Doctor error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in report["checks"]:
            print(f"{check['status'].upper()}: {check['kind']} {check['name']}")
        print(f"Workstation baseline: {report['status'].upper()}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
