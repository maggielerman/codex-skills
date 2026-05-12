#!/usr/bin/env python3
"""Audit a repo for automatic CI and hosting build triggers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORKFLOW_EVENT_RE = re.compile(r"^\s*(push|pull_request|pull_request_target|workflow_dispatch|workflow_call|schedule|release|deployment|repository_dispatch)\s*:", re.MULTILINE)
INLINE_ON_RE = re.compile(r"^\s*on\s*:\s*\[(.*?)\]\s*$", re.MULTILINE)
SIMPLE_ON_RE = re.compile(r"^\s*on\s*:\s*(push|pull_request|pull_request_target|workflow_dispatch|workflow_call|schedule|release|deployment|repository_dispatch)\s*$", re.MULTILINE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def scan_workflows(repo: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    workflow_dir = repo / ".github" / "workflows"
    if not workflow_dir.exists():
        return results

    for path in sorted(workflow_dir.glob("*.y*ml")):
        text = read_text(path)
        events = set()
        for match in WORKFLOW_EVENT_RE.finditer(text):
            events.add(match.group(1))
        for match in SIMPLE_ON_RE.finditer(text):
            events.add(match.group(1))
        for match in INLINE_ON_RE.finditer(text):
            for event in match.group(1).split(","):
                cleaned = event.strip().strip("'\"")
                if cleaned:
                    events.add(cleaned)

        automatic = sorted(events & {"push", "pull_request", "pull_request_target", "schedule", "release", "deployment", "repository_dispatch"})
        manual = sorted(events & {"workflow_dispatch", "workflow_call"})
        results.append(
            {
                "file": str(path.relative_to(repo)),
                "events": sorted(events),
                "automatic_events": automatic,
                "manual_events": manual,
                "risk": "automatic" if automatic else "manual-or-unknown",
            }
        )
    return results


def scan_file(path: Path, repo: Path, patterns: dict[str, str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = read_text(path)
    findings = []
    for label, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({"file": str(path.relative_to(repo)), "signal": label})
    return findings


def scan_hosting(repo: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    findings.extend(
        scan_file(
            repo / "vercel.json",
            repo,
            {
                "vercel config present": r".",
                "vercel auto deployments disabled": r'"deploymentEnabled"\s*:\s*false',
                "legacy vercel github.enabled": r'"enabled"\s*:\s*false',
            },
        )
    )
    findings.extend(
        scan_file(
            repo / "netlify.toml",
            repo,
            {
                "netlify config present": r".",
                "netlify ignore command": r"^\s*ignore\s*=",
                "netlify build command": r"^\s*command\s*=",
            },
        )
    )
    for name in ("render.yaml", "render.yml"):
        findings.extend(
            scan_file(
                repo / name,
                repo,
                {
                    "render blueprint present": r".",
                    "render autoDeploy false": r"autoDeploy\s*:\s*false",
                    "render autoDeploy configured": r"autoDeploy\s*:",
                },
            )
        )
    return findings


def scan_package(repo: Path) -> list[dict[str, str]]:
    path = repo / "package.json"
    if not path.exists():
        return []
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return [{"file": "package.json", "signal": "package.json invalid json"}]
    scripts = data.get("scripts", {})
    findings = []
    if isinstance(scripts, dict):
        for name, command in scripts.items():
            if re.search(r"\b(vercel|netlify|render|deploy)\b", str(command), re.IGNORECASE):
                findings.append({"file": "package.json", "signal": f"deploy script: {name}"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit automatic CI and hosting build triggers.")
    parser.add_argument("--repo", default=".", help="Repository root to audit")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        parser.error(f"repo does not exist: {repo}")

    report = {
        "repo": str(repo),
        "github_workflows": scan_workflows(repo),
        "hosting": scan_hosting(repo),
        "package_scripts": scan_package(repo),
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"Repo: {repo}")
    print("\nGitHub workflows:")
    workflows = report["github_workflows"]
    if workflows:
        for workflow in workflows:
            print(f"- {workflow['file']}: events={workflow['events']} risk={workflow['risk']}")
    else:
        print("- none found")

    print("\nHosting signals:")
    if report["hosting"]:
        for finding in report["hosting"]:
            print(f"- {finding['file']}: {finding['signal']}")
    else:
        print("- none found")

    print("\nPackage deploy scripts:")
    if report["package_scripts"]:
        for finding in report["package_scripts"]:
            print(f"- {finding['file']}: {finding['signal']}")
    else:
        print("- none found")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
