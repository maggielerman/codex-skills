#!/usr/bin/env python3
"""Apply in-review/blocked lifecycle extensions to ML-docs-system-scaffold repos."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply in-review/blocked project lifecycle extensions.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to target repository root (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing files.",
    )
    return parser.parse_args()


def find_child(
    parent: Path,
    candidate_names: tuple[str, ...],
    *,
    require_dir: bool = False,
    require_file: bool = False,
) -> Path | None:
    entries = [entry for entry in parent.iterdir()]

    def matches(entry: Path) -> bool:
        if require_dir and not entry.is_dir():
            return False
        if require_file and not entry.is_file():
            return False
        return True

    for candidate_name in candidate_names:
        for entry in entries:
            if entry.name == candidate_name and matches(entry):
                return entry

    for candidate_name in candidate_names:
        lower_name = candidate_name.lower()
        for entry in entries:
            if entry.name.lower() == lower_name and matches(entry):
                return entry

    return None


def detect_docs_root(repo: Path) -> Path:
    existing: list[Path] = []
    for candidate_name in ("DOCS", "docs", "documentation"):
        entry = find_child(repo, (candidate_name,), require_dir=True)
        if entry is not None and entry not in existing:
            existing.append(entry)

    if not existing:
        raise FileNotFoundError(
            "No docs root found. Expected DOCS/, docs/, or documentation/."
        )

    with_projects = [
        path
        for path in existing
        if find_child(path, ("PROJECTS", "projects"), require_dir=True) is not None
    ]
    if with_projects:
        for candidate_name in ("DOCS", "docs", "documentation"):
            for candidate in with_projects:
                if candidate.name == candidate_name:
                    return candidate
        return with_projects[0]

    for candidate_name in ("DOCS", "docs", "documentation"):
        for candidate in existing:
            if candidate.name == candidate_name:
                return candidate
    return existing[0]


def get_timestamp(repo: Path) -> str | None:
    cmd = ["node", "scripts/docs/timestamp-et.mjs", "--json"]
    try:
        result = subprocess.run(
            cmd,
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        return None

    timestamp = payload.get("timestampEt")
    if isinstance(timestamp, str) and timestamp:
        return timestamp
    return None


def replace_last_updated(markdown: str, timestamp: str) -> str:
    if not markdown.startswith("---\n"):
        return markdown

    match = re.match(r"\A---\n(.*?)\n---\n", markdown, flags=re.DOTALL)
    if not match:
        return markdown

    frontmatter = match.group(1)
    updated_frontmatter = re.sub(
        r'^lastUpdated:\s*"[^"]*"\s*$',
        f'lastUpdated: "{timestamp}"',
        frontmatter,
        count=1,
        flags=re.MULTILINE,
    )

    if updated_frontmatter == frontmatter:
        return markdown

    return markdown[: match.start(1)] + updated_frontmatter + markdown[match.end(1) :]


def contains_case_insensitive(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def insert_lines_after_anchor(
    text: str,
    anchor: str,
    new_lines: list[str],
    guard_substrings: list[str],
) -> str:
    if all(contains_case_insensitive(text, substring) for substring in guard_substrings):
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if anchor in line:
            updated = lines[: index + 1] + new_lines + lines[index + 1 :]
            return "\n".join(updated) + ("\n" if text.endswith("\n") else "")
    return text


def append_section_if_missing(text: str, heading: str, body_lines: list[str], marker: str) -> str:
    if contains_case_insensitive(text, marker):
        return text

    suffix = "\n" if text.endswith("\n") else ""
    return text.rstrip("\n") + "\n\n" + heading + "\n\n" + "\n".join(body_lines) + "\n" + suffix


def append_lines_to_section(
    text: str,
    section_heading: str,
    body_lines: list[str],
    marker: str,
) -> str:
    if contains_case_insensitive(text, marker):
        return text

    lines = text.splitlines()
    start_index = -1
    end_index = len(lines)

    for index, line in enumerate(lines):
        if line.strip() == section_heading:
            start_index = index
            break

    if start_index < 0:
        return append_section_if_missing(text, section_heading, body_lines, marker)

    for index in range(start_index + 1, len(lines)):
        if lines[index].startswith("## "):
            end_index = index
            break

    updated = lines[:end_index]
    if updated and updated[-1] != "":
        updated.append("")
    updated.extend(body_lines)
    if end_index < len(lines) and updated and updated[-1] != "":
        updated.append("")
    updated.extend(lines[end_index:])

    return "\n".join(updated) + ("\n" if text.endswith("\n") else "")


def transform_docs_readme(text: str, docs_root_name: str, projects_dir_name: str) -> str:
    text = insert_lines_after_anchor(
        text,
        f"- `{docs_root_name}/{projects_dir_name}/active/`",
        [
            f"- `{docs_root_name}/{projects_dir_name}/in-review/` - completed implementation awaiting walkthrough/sign-off",
            f"- `{docs_root_name}/{projects_dir_name}/blocked/` - waiting on user decisions/permissions/input",
        ],
        [
            f"{docs_root_name}/{projects_dir_name}/in-review/",
            f"{docs_root_name}/{projects_dir_name}/blocked/",
        ],
    )
    return text


def transform_projects_readme(text: str) -> str:
    text = insert_lines_after_anchor(
        text,
        "  - `active/`",
        [
            "  - `in-review/` - implementation complete, waiting for walkthrough/sign-off",
            "  - `blocked/` - waiting for user decisions/permissions/input",
        ],
        ["`in-review/`", "`blocked/`"],
    )

    text = append_section_if_missing(
        text,
        "## Lifecycle Transition Rules",
        [
            "1. Start implementation in `active/` with `status: active`.",
            "2. Move to `in-review/` with `status: in-review` after end-to-end execution is done and before walkthrough/sign-off.",
            "3. Move to `blocked/` with `status: blocked` when progress requires user decisions, permissions, access, or inputs.",
            "4. Move to `completed/` only after walkthrough/sign-off.",
            "5. Continue autonomous execution from backlog/stale while projects are in `in-review/` or `blocked`.",
        ],
        "## Lifecycle Transition Rules",
    )
    return text


def transform_docs_index(text: str, docs_root_name: str, projects_dir_name: str) -> str:
    return append_section_if_missing(
        text,
        "## Project Lifecycle Status Folders",
        [
            f"- `{docs_root_name}/{projects_dir_name}/active/` - in progress",
            f"- `{docs_root_name}/{projects_dir_name}/in-review/` - ready for collaborative walkthrough",
            f"- `{docs_root_name}/{projects_dir_name}/blocked/` - waiting on user input or permissions",
            f"- `{docs_root_name}/{projects_dir_name}/completed/` - delivered after walkthrough/sign-off",
            f"- `{docs_root_name}/{projects_dir_name}/backlog/` - queued",
            f"- `{docs_root_name}/{projects_dir_name}/stale/` - paused or deprecated",
        ],
        f"{docs_root_name}/{projects_dir_name}/in-review/",
    )


def transform_agents(text: str, docs_root_name: str, projects_dir_name: str) -> str:
    marker = f"`{docs_root_name}/{projects_dir_name}/in-review/`"
    text = insert_lines_after_anchor(
        text,
        "- Move the doc across status folders as work progresses.",
        [
            f"- Move a project to `{docs_root_name}/{projects_dir_name}/in-review/` and set `status: in-review` when implementation is complete but walkthrough/sign-off has not happened yet.",
            f"- Move a project to `{docs_root_name}/{projects_dir_name}/blocked/` and set `status: blocked` when waiting on user decisions, permissions, access, or missing inputs.",
            f"- Do not move a project to `{docs_root_name}/{projects_dir_name}/completed/` until collaborative walkthrough/sign-off is complete.",
            "- While projects are in `in-review` or `blocked`, continue execution by pulling the next prioritized backlog/stale stream.",
        ],
        [marker],
    )
    return text


def transform_template(text: str) -> str:
    text = re.sub(
        r"^status:\s*draft\s*$",
        "status: active",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    marker = "## Lifecycle Status Handling"
    if marker in text:
        return text

    heading = "# NNNN - Project Title"
    if heading not in text and "# NNNN – Project Title" in text:
        heading = "# NNNN – Project Title"

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            insert_at = index + 1
            block = [
                "",
                "## Lifecycle Status Handling",
                "",
                "- Keep project docs in `active/` with `status: active` while implementation is in progress.",
                "- Move docs to `in-review/` with `status: in-review` when implementation is complete and awaiting walkthrough/sign-off.",
                "- Move docs to `blocked/` with `status: blocked` when waiting on user decisions, permissions, access, or inputs.",
                "- Move docs to `completed/` with `status: completed` only after walkthrough/sign-off.",
                "",
            ]
            updated = lines[:insert_at] + block + lines[insert_at:]
            return "\n".join(updated) + ("\n" if text.endswith("\n") else "")
    return text


def transform_repo_readme(text: str, docs_root_name: str, projects_dir_name: str) -> str:
    marker = f"`{docs_root_name}/{projects_dir_name}/in-review/`"
    return append_lines_to_section(
        text,
        "## Docs",
        [
            "Project lifecycle folders:",
            f"- `{docs_root_name}/{projects_dir_name}/active/` - in progress",
            f"- `{docs_root_name}/{projects_dir_name}/in-review/` - implementation complete, awaiting walkthrough/sign-off",
            f"- `{docs_root_name}/{projects_dir_name}/blocked/` - waiting for user decisions/permissions/input",
            f"- `{docs_root_name}/{projects_dir_name}/completed/` - delivered after walkthrough/sign-off",
        ],
        marker,
    )


def transform_optional_instruction_markdown(
    text: str, docs_root_name: str, projects_dir_name: str
) -> str:
    return append_section_if_missing(
        text,
        "## Project Lifecycle Status Rules",
        [
            f"- Use `{docs_root_name}/{projects_dir_name}/in-review/` with `status: in-review` for completed implementation awaiting walkthrough/sign-off.",
            f"- Use `{docs_root_name}/{projects_dir_name}/blocked/` with `status: blocked` when waiting on user decisions, permissions, or required inputs.",
            f"- Move to `{docs_root_name}/{projects_dir_name}/completed/` only after collaborative walkthrough/sign-off.",
            "- Continue autonomous execution from backlog/stale work while waiting on in-review or blocked items.",
        ],
        f"{projects_dir_name}/in-review",
    )


def transform_optional_instruction_text(
    text: str, docs_root_name: str, projects_dir_name: str
) -> str:
    marker = f"{projects_dir_name}/in-review"
    if contains_case_insensitive(text, marker):
        return text

    block = [
        "",
        "Project lifecycle status rules:",
        f"- Use {docs_root_name}/{projects_dir_name}/in-review with status: in-review when implementation is done and awaiting walkthrough/sign-off.",
        f"- Use {docs_root_name}/{projects_dir_name}/blocked with status: blocked when waiting on user decisions/permissions/input.",
        f"- Move to {docs_root_name}/{projects_dir_name}/completed only after collaborative walkthrough/sign-off.",
    ]
    return text.rstrip("\n") + "\n" + "\n".join(block) + "\n"


def ensure_directories(projects_dir: Path, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    for folder_name in ("in-review", "blocked"):
        folder = projects_dir / folder_name
        gitkeep = folder / ".gitkeep"

        if not folder.exists():
            if not dry_run:
                folder.mkdir(parents=True, exist_ok=True)
            changed.append(folder)

        if not gitkeep.exists():
            if not dry_run:
                gitkeep.write_text("", encoding="utf-8")
            changed.append(gitkeep)

    return changed


def apply_text_update(
    path: Path,
    transform: Callable[[str], str],
    dry_run: bool,
    timestamp: str | None,
) -> bool:
    if not path.exists() or not path.is_file():
        return False

    original = path.read_text(encoding="utf-8")
    updated = transform(original)

    if updated != original and timestamp and path.suffix.lower() == ".md":
        updated = replace_last_updated(updated, timestamp)

    if updated == original:
        return False

    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True


def collect_optional_instruction_files(repo: Path, docs_root: Path) -> tuple[list[Path], list[Path]]:
    markdown_targets: list[Path] = []
    text_targets: list[Path] = []

    github_dir = find_child(repo, (".github",), require_dir=True)
    if github_dir is not None:
        copilot = find_child(
            github_dir,
            ("copilot-instructions.md", "COPILOT-INSTRUCTIONS.MD"),
            require_file=True,
        )
        if copilot is not None:
            markdown_targets.append(copilot)

    claude_file = find_child(repo, ("CLAUDE.md", "claude.md"), require_file=True)
    if claude_file is not None:
        markdown_targets.append(claude_file)

    cursor_dir = find_child(repo, (".cursor",), require_dir=True)
    cursor_rules = (
        find_child(cursor_dir, ("rules",), require_dir=True)
        if cursor_dir is not None
        else None
    )
    if cursor_rules is not None:
        for path in sorted(cursor_rules.rglob("*")):
            if path.is_file():
                if path.suffix.lower() == ".md":
                    markdown_targets.append(path)
                else:
                    text_targets.append(path)

    for root in (repo, docs_root):
        for path in sorted(root.iterdir()):
            if not path.is_file():
                continue
            lowered = path.name.lower()
            if not lowered.startswith("llm"):
                continue
            if not (lowered.endswith(".md") or lowered.endswith(".txt")):
                continue
            if path.suffix.lower() == ".md":
                if path not in markdown_targets:
                    markdown_targets.append(path)
            else:
                if path not in text_targets:
                    text_targets.append(path)

    return markdown_targets, text_targets


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()

    if not repo.is_dir():
        print(f"[ERROR] repo does not exist: {repo}", file=sys.stderr)
        return 1

    try:
        docs_root = detect_docs_root(repo)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    projects_dir = find_child(docs_root, ("PROJECTS", "projects"), require_dir=True)
    if projects_dir is None:
        print(
            f"[ERROR] Missing expected projects directory under: {docs_root}",
            file=sys.stderr,
        )
        return 1

    timestamp = get_timestamp(repo)
    if timestamp:
        print(f"[INFO] Using timestampEt from script: {timestamp}")
    else:
        print(
            "[WARN] Could not read scripts/docs/timestamp-et.mjs --json; "
            "frontmatter lastUpdated will not be refreshed."
        )

    docs_root_name = docs_root.name
    projects_dir_name = projects_dir.name
    changed_paths: list[Path] = []

    changed_paths.extend(ensure_directories(projects_dir, args.dry_run))

    docs_readme = find_child(docs_root, ("README.md", "readme.md"), require_file=True)
    docs_index = find_child(docs_root, ("index.md", "INDEX.md"), require_file=True)
    projects_readme = find_child(projects_dir, ("README.md", "readme.md"), require_file=True)
    active_dir = find_child(projects_dir, ("active", "ACTIVE"), require_dir=True)
    project_template = (
        find_child(
            active_dir,
            ("NNNN_project_template.md", "nnnn_project_template.md"),
            require_file=True,
        )
        if active_dir is not None
        else None
    )
    agents_file = find_child(repo, ("AGENTS.md", "agents.md"), require_file=True)
    repo_readme = find_child(repo, ("README.md", "readme.md"), require_file=True)

    file_updates: list[tuple[Path, Callable[[str], str]]] = []
    if docs_readme is not None:
        file_updates.append(
            (
                docs_readme,
                lambda text: transform_docs_readme(
                    text, docs_root_name, projects_dir_name
                ),
            )
        )
    if docs_index is not None:
        file_updates.append(
            (
                docs_index,
                lambda text: transform_docs_index(
                    text, docs_root_name, projects_dir_name
                ),
            )
        )
    if projects_readme is not None:
        file_updates.append((projects_readme, transform_projects_readme))
    if project_template is not None:
        file_updates.append((project_template, transform_template))
    if agents_file is not None:
        file_updates.append(
            (
                agents_file,
                lambda text: transform_agents(text, docs_root_name, projects_dir_name),
            )
        )
    if repo_readme is not None:
        file_updates.append(
            (
                repo_readme,
                lambda text: transform_repo_readme(
                    text, docs_root_name, projects_dir_name
                ),
            )
        )

    for path, transform in file_updates:
        if apply_text_update(path, transform, args.dry_run, timestamp):
            changed_paths.append(path)

    markdown_optional, text_optional = collect_optional_instruction_files(repo, docs_root)

    for path in markdown_optional:
        if apply_text_update(
            path,
            lambda text, docs_name=docs_root_name, projects_name=projects_dir_name: transform_optional_instruction_markdown(
                text, docs_name, projects_name
            ),
            args.dry_run,
            timestamp,
        ):
            changed_paths.append(path)

    for path in text_optional:
        if apply_text_update(
            path,
            lambda text, docs_name=docs_root_name, projects_name=projects_dir_name: transform_optional_instruction_text(
                text, docs_name, projects_name
            ),
            args.dry_run,
            None,
        ):
            changed_paths.append(path)

    if changed_paths:
        print("[OK] Applied lifecycle extension updates:")
        for changed in sorted({path.resolve() for path in changed_paths}):
            print(f"- {changed}")
    else:
        print("[OK] No updates needed. Repository already matches lifecycle extension.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
