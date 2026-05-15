#!/usr/bin/env python3
"""Backfill visual design quality gate docs into existing product OS scaffold repos."""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo


DOCS_ROOT_CANDIDATES = ("DOCS", "docs", "documentation")


@dataclass
class PendingWrite:
    path: Path
    before: str | None
    after: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill visual design critique gates into an existing product operating system scaffold.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to target repository root (default: current directory).",
    )
    parser.add_argument(
        "--docs-root",
        help="Explicit docs root name, for example DOCS or docs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    return parser.parse_args()


def find_case_insensitive_dir(parent: Path, name: str) -> Path | None:
    if not parent.exists():
        return None
    for child in parent.iterdir():
        if child.is_dir() and child.name.lower() == name.lower():
            return child
    return None


def score_docs_root(candidate: Path) -> int:
    score = 0
    if find_case_insensitive_dir(candidate, "PROJECTS"):
        score += 10
    if (candidate / "README.md").exists():
        score += 2
    if (candidate / "index.md").exists():
        score += 1
    if (candidate / "development").is_dir():
        score += 1
    return score


def discover_docs_root(repo_root: Path, explicit: str | None) -> Path:
    if explicit:
        docs_root = repo_root / explicit
        if not docs_root.is_dir():
            raise FileNotFoundError(f"Docs root not found: {docs_root}")
        return docs_root

    matches: list[Path] = []
    for name in DOCS_ROOT_CANDIDATES:
        candidate = find_case_insensitive_dir(repo_root, name)
        if candidate is None:
            continue
        if any(candidate.samefile(existing) for existing in matches):
            continue
        matches.append(candidate)

    if not matches:
        raise FileNotFoundError("Could not find DOCS/, docs/, or documentation/ in the target repo.")

    ranked = sorted((score_docs_root(path), path.name, path) for path in matches)
    best_score, _, best_path = ranked[-1]
    if len(ranked) > 1 and ranked[-2][0] == best_score:
        raise RuntimeError("Multiple docs roots matched with the same score. Re-run with --docs-root.")
    return best_path


def ensure_projects_root(docs_root: Path) -> Path:
    projects_root = find_case_insensitive_dir(docs_root, "PROJECTS")
    if not projects_root:
        raise FileNotFoundError(
            f"Could not find PROJECTS/ under {docs_root}. Run the product operating system scaffold first."
        )
    return projects_root


def timestamp_et(repo_root: Path) -> str:
    script = repo_root / "scripts" / "docs" / "timestamp-et.mjs"
    if script.exists():
        try:
            result = subprocess.run(
                ["node", "scripts/docs/timestamp-et.mjs", "--json"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout.strip())
            value = payload.get("timestampEt")
            if isinstance(value, str) and value:
                return value
        except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError):
            pass

    now = datetime.now(ZoneInfo("America/New_York"))
    return now.strftime("%Y-%m-%d %H:%M ET (America/New_York)")


def ensure_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def append_section_if_missing(text: str, heading: str, body: str, marker: str) -> str:
    if marker.lower() in text.lower():
        return text
    return text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n"


def append_line_after_anchor(text: str, anchor: str, line_to_add: str, marker: str) -> str:
    if marker.lower() in text.lower():
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if anchor in line:
            updated = lines[: index + 1] + [line_to_add] + lines[index + 1 :]
            return "\n".join(updated) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line_to_add + "\n"


def append_lines_after_anchor(text: str, anchor: str, lines_to_add: list[str], marker: str) -> str:
    if marker.lower() in text.lower():
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if anchor in line:
            updated = lines[: index + 1] + lines_to_add + lines[index + 1 :]
            return "\n".join(updated) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + "\n".join(lines_to_add) + "\n"


def insert_section_after_heading(text: str, heading: str, section: str, marker: str) -> str:
    if marker.lower() in text.lower():
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            end = len(lines)
            for next_index in range(index + 1, len(lines)):
                if lines[next_index].startswith("## "):
                    end = next_index
                    break
            updated = lines[:end]
            if updated and updated[-1] != "":
                updated.append("")
            updated.extend(section.strip().splitlines())
            updated.append("")
            updated.extend(lines[end:])
            return "\n".join(updated).rstrip() + "\n"
    return text.rstrip() + "\n\n" + section.strip() + "\n"


def visual_gate_doc(docs_root_name: str, timestamp: str) -> str:
    return f"""---
title: Visual Design Quality Gate
description: Required critique checkpoint for significant user-facing UI work
status: evolving
lastUpdated: "{timestamp}"
owner: Product/Design/Engineering
---

# Visual Design Quality Gate

Use this gate for significant user-facing UI work: app screens, dashboards, websites, landing pages, forms, redesigns, restyles, route screenshot audits, and visual QA.

## Required Skill

Use `$visual-design-critique` before implementation sign-off or before moving the owning project doc to `PROJECTS/in-review/`.

## Review Scope

The critique must cover:

- product intent and first read
- information architecture and hierarchy
- composition, spacing, alignment, and density
- typography, labels, data text, and responsive wrapping
- color, contrast, material, shadows, and semantic status treatment
- component anatomy, consistency, and interaction states
- accessibility, focus visibility, keyboard path, target size, and reduced-motion needs
- responsive behavior across the relevant viewport set
- product fit, taste, restraint, and brand tone

## Evidence

Use rendered screenshots, route captures, supplied mockups, accepted concepts, or numbered review-board packets as evidence.

Preserve artifacts under `{docs_root_name}/evidence/active/<project>/` only when they are needed for durable verification, sign-off, or future comparison.

## Project Doc Entry

Record the critique outcome in the owning project doc:

- verdict
- evidence paths
- must-fix issues
- should-fix issues
- approved deviations
- follow-up verification

Use `MAGGIE TODO:` if human taste approval, manual screenshot review, brand input, or external stakeholder review gates completion.
"""


def update_development_index(text: str) -> str:
    return append_line_after_anchor(
        text,
        "- [Checkpoint Workflow](./checkpoint-workflow.md)",
        "- [Visual Design Quality Gate](./visual-design-quality-gate.md)",
        "visual-design-quality-gate.md",
    )


def update_docs_readme(text: str, docs_root_name: str) -> str:
    text = append_line_after_anchor(
        text,
        f"- `{docs_root_name}/development/checkpoint-workflow.md`",
        f"- `{docs_root_name}/development/visual-design-quality-gate.md` (visual UI/UX critique gate)",
        "visual-design-quality-gate.md",
    )
    return append_section_if_missing(
        text,
        "## Visual Design Quality",
        "- Use `$visual-design-critique` before sign-off for significant user-facing UI work.\n"
        "- Record critique outcomes in the owning project doc and preserve screenshots or review-board packets only when they are useful durable evidence.",
        "$visual-design-critique",
    )


def update_docs_index(text: str, docs_root_name: str) -> str:
    return append_line_after_anchor(
        text,
        f"- `{docs_root_name}/development/`",
        f"- `{docs_root_name}/development/visual-design-quality-gate.md`",
        "visual-design-quality-gate.md",
    )


def update_projects_readme(text: str, docs_root_name: str) -> str:
    return append_section_if_missing(
        text,
        "## Visual/UX Quality Gate",
        "- For significant user-facing UI work, run `$visual-design-critique` before moving to `in-review/`.\n"
        "- Record the critique verdict, evidence paths, must-fix issues, approved deviations, and follow-up verification in the owning project doc.\n"
        f"- Use `{docs_root_name}/development/visual-design-quality-gate.md` as the repo-local standard.",
        "Visual/UX Quality Gate",
    )


def update_project_template(text: str) -> str:
    section = """## Visual/UX Quality Gate
For significant user-facing UI work, use `$visual-design-critique` before implementation sign-off or movement to `in-review`.

- Critique verdict:
- Evidence paths:
- Must-fix issues:
- Approved deviations:
- Follow-up verification:"""
    return insert_section_after_heading(text, "## Success Criteria", section, "Critique verdict:")


def update_agents(text: str) -> str:
    text = append_line_after_anchor(
        text,
        "- Prefer `DOCS/`",
        "- For significant user-facing UI, redesign, restyle, dashboard, app, website, form, screenshot-route, or visual QA work, use `$visual-design-critique` before implementation sign-off or movement to `in-review`.",
        "$visual-design-critique",
    )
    return append_line_after_anchor(
        text,
        "- Maintain a checkpoint log",
        "- Record visual design critique outcomes in the project doc for user-facing UI work, including the verdict, must-fix issues, evidence paths, and remaining approved deviations.",
        "visual design critique outcomes",
    )


def read_or_empty(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def queue_update(
    writes: list[PendingWrite],
    path: Path,
    transform: Callable[[str], str],
    *,
    create_if_missing: str | None = None,
) -> None:
    before = path.read_text(encoding="utf-8") if path.exists() else None
    source = before if before is not None else create_if_missing
    if source is None:
        return

    after = ensure_trailing_newline(transform(source))
    if before != after:
        writes.append(PendingWrite(path, before, after))


def print_diff(write: PendingWrite, repo_root: Path) -> None:
    rel = write.path.relative_to(repo_root) if write.path.is_relative_to(repo_root) else write.path
    before_lines = [] if write.before is None else write.before.splitlines(keepends=True)
    after_lines = write.after.splitlines(keepends=True)
    diff = difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=f"a/{rel}",
        tofile=f"b/{rel}",
    )
    sys.stdout.writelines(diff)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).expanduser().resolve()
    if not repo_root.is_dir():
        print(f"Repository root not found: {repo_root}", file=sys.stderr)
        return 1

    try:
        docs_root = discover_docs_root(repo_root, args.docs_root)
        projects_root = ensure_projects_root(docs_root)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    docs_root_name = docs_root.name
    timestamp = timestamp_et(repo_root)
    writes: list[PendingWrite] = []

    guide_path = docs_root / "development" / "visual-design-quality-gate.md"
    queue_update(
        writes,
        guide_path,
        lambda text: text if "Visual Design Quality Gate" in text else visual_gate_doc(docs_root_name, timestamp),
        create_if_missing=visual_gate_doc(docs_root_name, timestamp),
    )

    queue_update(writes, docs_root / "development" / "index.md", update_development_index)
    queue_update(writes, docs_root / "README.md", lambda text: update_docs_readme(text, docs_root_name))
    queue_update(writes, docs_root / "index.md", lambda text: update_docs_index(text, docs_root_name))
    queue_update(writes, projects_root / "README.md", lambda text: update_projects_readme(text, docs_root_name))
    queue_update(writes, projects_root / "active" / "NNNN_project_template.md", update_project_template)
    queue_update(writes, repo_root / "AGENTS.md", update_agents)

    if args.dry_run:
        if not writes:
            print("No changes needed.")
            return 0
        for write in writes:
            print_diff(write, repo_root)
        return 0

    for write in writes:
        write.path.parent.mkdir(parents=True, exist_ok=True)
        write.path.write_text(write.after, encoding="utf-8")

    print(f"Docs root: {docs_root}")
    print(f"Projects root: {projects_root}")
    if writes:
        print("Updated files:")
        for write in writes:
            rel = write.path.relative_to(repo_root) if write.path.is_relative_to(repo_root) else write.path
            print(f"- {rel}")
    else:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
