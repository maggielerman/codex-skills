#!/usr/bin/env python3
"""Install the tracked workstation baseline with recoverable local backups."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


IGNORED_NAMES = {".DS_Store", "__pycache__"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--host-overlay", type=Path)
    parser.add_argument("--skip-plugins", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Apply changes; omission is preview-only")
    return parser.parse_args()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return "missing"
    if root.is_file():
        digest.update(root.read_bytes())
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
            digest.update(path.read_bytes())
        elif path.is_dir():
            digest.update(f"dir\0{relative}\0".encode("utf-8"))
    return digest.hexdigest()


def run_codex(*args: str) -> str:
    result = subprocess.run(
        ["codex", "plugin", *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Codex plugin command failed: {' '.join(args)}")
    return result.stdout


def source_root(name: str, repo_root: Path, overlay: Dict[str, Any]) -> Path:
    if name == "codex-skills":
        return repo_root
    configured = overlay.get("repositoryRoots", {}).get(name)
    if not configured:
        raise RuntimeError(f"Host overlay is missing repository root: {name}")
    return Path(configured).expanduser().resolve()


def install_files(repo_root: Path, codex_home: Path, manifest: Dict[str, Any], apply: bool) -> None:
    policy_source = repo_root / manifest["globalPolicy"]
    skill_sources = [
        (skill["name"], repo_root / skill["source"])
        for skill in manifest.get("standaloneSkills", [])
    ]
    missing = [str(path) for _, path in skill_sources if not path.is_dir()]
    if not policy_source.is_file():
        missing.append(str(policy_source))
    if missing:
        raise RuntimeError("Missing baseline sources: " + ", ".join(missing))

    print(f"PLAN: install global policy and {len(skill_sources)} standalone skills")
    if not apply:
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = codex_home / "backups" / "workstation-bootstrap" / timestamp
    codex_home.mkdir(parents=True, exist_ok=True)
    (codex_home / "skills").mkdir(parents=True, exist_ok=True)

    policy_target = codex_home / "AGENTS.md"
    if policy_target.exists():
        backup_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(policy_target, backup_root / "AGENTS.md")
    shutil.copy2(policy_source, policy_target)
    policy_target.chmod(0o600)

    for name, source in skill_sources:
        target = codex_home / "skills" / name
        if target.exists() or target.is_symlink():
            destination = backup_root / "skills" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(destination))
        shutil.copytree(source, target, symlinks=True)
    print(f"APPLIED: backup root {backup_root}")


def install_plugins(
    repo_root: Path,
    manifest: Dict[str, Any],
    overlay: Dict[str, Any],
    apply: bool,
) -> None:
    required_plugins = [
        plugin for plugin in manifest.get("plugins", []) if plugin.get("required", True)
    ]
    print(f"PLAN: ensure {len(required_plugins)} required plugins")
    if not apply:
        return

    marketplace_output = run_codex("marketplace", "list")
    configured = {
        line.split()[0]
        for line in marketplace_output.splitlines()[1:]
        if line.strip()
    }
    for marketplace in manifest.get("marketplaces", []):
        if marketplace["name"] in configured:
            continue
        root = source_root(marketplace["sourceRoot"], repo_root, overlay)
        run_codex("marketplace", "add", str(root), "--json")

    state = json.loads(run_codex("list", "--available", "--json"))
    installed = {item.get("name"): item for item in state.get("installed", [])}
    for plugin in required_plugins:
        observed = installed.get(plugin["name"])
        expected_root = source_root(plugin.get("sourceRoot", "codex-skills"), repo_root, overlay)
        expected_digest = tree_digest(expected_root / plugin["source"])
        actual_path = observed.get("source", {}).get("path") if observed else None
        actual_digest = tree_digest(Path(actual_path)) if actual_path else "missing"
        current = (
            observed is not None
            and observed.get("version") == plugin["version"]
            and bool(observed.get("enabled")) == bool(plugin.get("enabled", True))
            and actual_digest == expected_digest
        )
        if not current:
            run_codex("add", f"{plugin['name']}@{plugin['marketplace']}", "--json")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    codex_home = args.codex_home.expanduser().resolve()
    manifest_path = args.manifest or repo_root / "config" / "workstation-baseline.json"
    try:
        manifest = load_json(manifest_path)
        overlay = load_json(args.host_overlay) if args.host_overlay else {}
        install_files(repo_root, codex_home, manifest, args.apply)
        if not args.skip_plugins:
            install_plugins(repo_root, manifest, overlay, args.apply)
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"Bootstrap error: {error}", file=sys.stderr)
        return 2

    print("Preview complete." if not args.apply else "Bootstrap complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
