#!/usr/bin/env python3
"""Discover docs-scaffold project context for tranche orchestration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_STATUSES = ["active", "in-review", "blocked", "backlog", "stale", "completed"]
TARGETABLE_STATUSES = ["active", "in-review", "backlog", "stale", "blocked"]
GOVERNANCE_FILES = ["AGENTS.md", "ROADMAP.md", "CHANGELOG.md"]
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
DEPENDENCY_RE = re.compile(r"(?i)\b(?:depends on|dependency|dependencies|gated on|blocked by)\b")
BLOCKER_RE = re.compile(r"(?i)\b(?:blocker|blocked|risk)\b")
NEXT_RE = re.compile(r"(?i)\b(?:next checkpoint|next step|next actions?|before next checkpoint)\b")
ACCEPTANCE_HEADINGS = (
    "acceptance",
    "success criteria",
    "exit criteria",
    "done when",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--statuses",
        nargs="*",
        default=DEFAULT_STATUSES,
        help="Lifecycle status folders to inspect.",
    )
    return parser.parse_args()


def find_docs_root(repo: Path) -> Path | None:
    candidates = []
    for name in ("DOCS", "docs", "documentation"):
        candidate = repo / name
        if not candidate.is_dir():
            continue
        projects_dir = candidate / "PROJECTS"
        score = 0
        if projects_dir.is_dir():
            score += 3
        if (candidate / "README.md").exists():
            score += 1
        if (candidate / "index.md").exists():
            score += 1
        candidates.append((score, candidate))
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (-item[0], str(item[1])))[0][1]


def parse_sections(text: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current = {"heading": "", "level": 0, "lines": []}
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            if current["heading"] or current["lines"]:
                sections.append(current)
            current = {
                "heading": match.group(2).strip(),
                "level": len(match.group(1)),
                "lines": [],
            }
            continue
        current["lines"].append(line)
    if current["heading"] or current["lines"]:
        sections.append(current)
    return sections


def extract_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        bullet = re.match(r"^(?:[-*+]|\d+\.)\s+(.*)$", line)
        items.append((bullet.group(1) if bullet else line).strip())
    return items


def first_heading_title(sections: list[dict[str, object]], fallback: str) -> str:
    for section in sections:
        heading = str(section["heading"]).strip()
        if heading:
            return heading
    return fallback


def section_matches(section: dict[str, object], patterns: tuple[str, ...]) -> bool:
    heading = str(section["heading"]).lower()
    return any(pattern in heading for pattern in patterns)


def collect_matching_items(sections: list[dict[str, object]], pattern: re.Pattern[str]) -> list[str]:
    matches: list[str] = []
    for section in sections:
        lines = extract_items(section["lines"])
        for item in lines:
            if pattern.search(item):
                matches.append(item)
    return unique(matches)


def collect_section_items(sections: list[dict[str, object]], patterns: tuple[str, ...]) -> list[str]:
    matches: list[str] = []
    for section in sections:
        if section_matches(section, patterns):
            matches.extend(extract_items(section["lines"]))
    return unique(matches)


def unique(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def relative(path: Path, repo: Path) -> str:
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def parse_project_doc(path: Path, repo: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    status = path.parent.name
    acceptance = collect_section_items(sections, ACCEPTANCE_HEADINGS)
    dependencies = collect_section_items(sections, ("dependency", "dependencies"))
    dependencies.extend(collect_matching_items(sections, DEPENDENCY_RE))
    blockers = collect_section_items(sections, ("blocker", "blockers", "risks", "risk"))
    blockers.extend(collect_matching_items(sections, BLOCKER_RE))
    next_actions = collect_section_items(sections, ("next checkpoint", "next steps", "next step", "next actions"))
    next_actions.extend(collect_matching_items(sections, NEXT_RE))
    checkpoints = unique(DATE_RE.findall(text))
    stem = path.stem
    project_id = stem.split("_", 1)[0] if re.match(r"^\d+", stem) else stem
    return {
        "id": project_id,
        "title": first_heading_title(sections, stem),
        "path": relative(path, repo),
        "status": status,
        "dependencies": unique(dependencies),
        "blockers": unique(blockers),
        "acceptance_criteria": acceptance,
        "next_actions": unique(next_actions),
        "checkpoint_dates": checkpoints,
        "has_acceptance_criteria": bool(acceptance),
        "has_blockers": bool(blockers),
    }


def build_projects(repo: Path, docs_root: Path, statuses: list[str]) -> list[dict[str, object]]:
    projects_dir = docs_root / "PROJECTS"
    projects: list[dict[str, object]] = []
    if not projects_dir.is_dir():
        return projects
    for status in statuses:
        status_dir = projects_dir / status
        if not status_dir.is_dir():
            continue
        for path in sorted(status_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            projects.append(parse_project_doc(path, repo))
    return projects


def select_recommended_project(projects: list[dict[str, object]]) -> dict[str, object] | None:
    priorities = {name: index for index, name in enumerate(TARGETABLE_STATUSES)}

    def project_key(project: dict[str, object]) -> tuple[int, int, int, str]:
        status = str(project["status"])
        blocked_penalty = 1 if project["has_blockers"] and status != "blocked" else 0
        acceptance_penalty = 0 if project["has_acceptance_criteria"] else 1
        return (
            priorities.get(status, len(priorities)),
            blocked_penalty,
            acceptance_penalty,
            str(project["path"]),
        )

    candidates = [project for project in projects if project["status"] != "completed"]
    if not candidates:
        return None
    candidates.sort(key=project_key)
    return candidates[0]


def build_summary(projects: list[dict[str, object]]) -> dict[str, int]:
    summary = {status: 0 for status in DEFAULT_STATUSES}
    for project in projects:
        status = str(project["status"])
        summary[status] = summary.get(status, 0) + 1
    return summary


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).expanduser().resolve()
    docs_root = find_docs_root(repo)
    governance = {
        name: relative(repo / name, repo) for name in GOVERNANCE_FILES if (repo / name).exists()
    }
    missing_governance = [name for name in GOVERNANCE_FILES if name not in governance]

    payload: dict[str, object] = {
        "repo_root": str(repo),
        "governance_files": governance,
        "missing_governance_files": missing_governance,
    }

    if docs_root is None:
        payload["error"] = "No docs root found. Expected DOCS/, docs/, or documentation/."
        print(json.dumps(payload, indent=2))
        return 1

    projects_dir = docs_root / "PROJECTS"
    payload["docs_root"] = relative(docs_root, repo)
    payload["projects_root"] = relative(projects_dir, repo)

    if not projects_dir.is_dir():
        payload["error"] = f"Docs root '{relative(docs_root, repo)}' is missing PROJECTS/."
        print(json.dumps(payload, indent=2))
        return 1

    projects = build_projects(repo, docs_root, args.statuses)
    payload["projects"] = projects
    payload["status_summary"] = build_summary(projects)
    payload["recommended_project"] = select_recommended_project(projects)

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
