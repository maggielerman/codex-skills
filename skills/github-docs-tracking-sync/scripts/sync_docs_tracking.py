#!/usr/bin/env python3
"""
Sync docs-driven project tracking into GitHub issues, a roadmap issue, and a 1027-style
single GitHub Project board.

Default mode is dry-run. Use --apply to mutate GitHub.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STATUS_FOLDERS = ("active", "backlog", "drafts", "stale", "completed")

STATUS_LABEL_BY_FOLDER = {
    "active": "status:in-progress",
    "backlog": "status:triaged",
    "drafts": "status:triaged",
    "stale": "status:blocked",
    "completed": "status:resolved",
}

PROJECT_STATUS_BY_FOLDER = {
    "active": "In Progress",
    "backlog": "Triaged",
    "drafts": "Triaged",
    "stale": "Blocked",
    "completed": "Done",
}

LABEL_DEFS = {
    "type:incident": {"color": "D73A49", "description": "Operational incident"},
    "type:bug": {"color": "B60205", "description": "Product/runtime bug"},
    "type:feature": {"color": "1D76DB", "description": "Feature delivery work item"},
    "type:task": {"color": "5319E7", "description": "General execution task"},
    "priority:p0": {"color": "B60205", "description": "Critical priority"},
    "priority:p1": {"color": "D93F0B", "description": "High priority"},
    "priority:p2": {"color": "FBCA04", "description": "Medium priority"},
    "area:seo-gates": {"color": "0E8A16", "description": "SEO/agent monitoring"},
    "area:ops": {"color": "0052CC", "description": "Operations and release checks"},
    "area:intake": {"color": "5319E7", "description": "Intake workflows and artifacts"},
    "area:admin": {"color": "BFDADC", "description": "Admin system and controls"},
    "area:viz": {"color": "C5DEF5", "description": "Visualization and graph UX"},
    "area:docs": {"color": "D4C5F9", "description": "Documentation and governance"},
    "status:triaged": {"color": "FBCA04", "description": "Triaged and ready for execution"},
    "status:in-progress": {"color": "0E8A16", "description": "Actively in progress"},
    "status:blocked": {"color": "B60205", "description": "Blocked pending dependency"},
    "status:resolved": {"color": "1D76DB", "description": "Resolved and verified"},
    "env:production": {"color": "0052CC", "description": "Production environment"},
    "env:preview": {"color": "5319E7", "description": "Preview environment"},
    "env:local": {"color": "BFD4F2", "description": "Local environment"},
}

AREA_RULES = [
    (re.compile(r"seo|gate", re.I), "area:seo-gates"),
    (re.compile(r"intake|import|hydrat", re.I), "area:intake"),
    (re.compile(r"admin|domain", re.I), "area:admin"),
    (re.compile(r"viz|visual|canvas|constellation|diagram", re.I), "area:viz"),
    (re.compile(r"docs|roadmap|changelog|checkpoint|governance", re.I), "area:docs"),
    (re.compile(r"ops|release|workflow|ci|github|tracking", re.I), "area:ops"),
]

FIELD_SPECS = [
    {"name": "Type", "data_type": "SINGLE_SELECT", "options": ["incident", "bug", "feature", "task"]},
    {"name": "Priority", "data_type": "SINGLE_SELECT", "options": ["p0", "p1", "p2"]},
    {"name": "Area", "data_type": "SINGLE_SELECT", "options": ["seo-gates", "ops", "intake", "admin", "viz", "docs"]},
    {"name": "Docs Project ID", "data_type": "TEXT"},
    {"name": "Incident ID", "data_type": "TEXT"},
    {"name": "Start Date", "data_type": "DATE"},
    {"name": "Target Date", "data_type": "DATE"},
    {"name": "Completed Date", "data_type": "DATE"},
]

ISSUE_TEMPLATE_CONFIG = {
    "config.yml": """blank_issues_enabled: false
contact_links:
  - name: Docs Governance
    url: https://github.com/{repo}/tree/main/{docs_root}
    about: Policy decisions, checkpoints, and roadmap context live in {docs_root}.
""",
    "incident.yml": """name: Incident
description: Report an operational incident from gate failures, deploy regressions, or monitoring anomalies.
title: "[Incident] "
labels:
  - type:incident
  - status:triaged
body:
  - type: markdown
    attributes:
      value: |
        Use this template for operational incidents. Keep `incident_id` stable over the incident lifecycle.
  - type: input
    id: incident_id
    attributes:
      label: Incident ID
      description: Stable ID (example `ci-gate-release-parity` or `seo-gate-gate_c-20260219`).
      placeholder: ci-gate-release-parity
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - P0
        - P1
        - P2
    validations:
      required: true
  - type: input
    id: detected_at
    attributes:
      label: Detected At (UTC)
      description: ISO 8601 timestamp from gate report or monitoring signal.
      placeholder: 2026-02-19T17:38:43Z
    validations:
      required: true
  - type: input
    id: gate
    attributes:
      label: Gate / Signal
      description: Gate ID/name or signal source.
      placeholder: parity (Admin/public parity)
    validations:
      required: true
  - type: dropdown
    id: environment
    attributes:
      label: Environment
      options:
        - production
        - preview
        - local
    validations:
      required: true
  - type: textarea
    id: summary
    attributes:
      label: Signal Summary
      description: What failed and how it impacts release/operations.
      placeholder: Parity login failed with 403 due to host/origin mismatch.
    validations:
      required: true
  - type: textarea
    id: artifacts
    attributes:
      label: Artifact References
      description: Include run URLs, artifact names, or report paths.
      placeholder: |
        https://github.com/OWNER/REPO/actions/runs/123456789
        tmp/ops/release-gate/release-2026-02-19T17-38-38-002Z.json
    validations:
      required: true
  - type: textarea
    id: next_checkpoint_target
    attributes:
      label: Next Checkpoint Target
      description: Explicit follow-up target to carry into docs checkpoint.
      placeholder: Set SITE_URL to canonical host and re-run push gate validation.
    validations:
      required: true
  - type: input
    id: docs_project_id
    attributes:
      label: Docs Project ID
      description: Reference the docs project number (for example `1022`, `1026`, `1027`).
      placeholder: "1022"
    validations:
      required: true
""",
    "bug.yml": """name: Bug
description: Report a product or runtime defect not modeled as an operational incident.
title: "[Bug] "
labels:
  - type:bug
  - status:triaged
body:
  - type: input
    id: summary
    attributes:
      label: Summary
      placeholder: Node detail page renders duplicated markdown metadata blocks.
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Context
      description: Scope, affected routes/components, and impact.
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: Priority
      options:
        - P0
        - P1
        - P2
    validations:
      required: true
  - type: input
    id: docs_project_id
    attributes:
      label: Docs Project ID
      placeholder: "1016"
    validations:
      required: true
  - type: textarea
    id: verification
    attributes:
      label: Verification Plan
      description: Tests/checks required before closeout.
      placeholder: Add regression test and validate in production route.
    validations:
      required: true
""",
    "feature.yml": """name: Feature
description: Track a feature delivery item for roadmap, completion charts, and release planning.
title: "[Feature] "
labels:
  - type:feature
  - status:triaged
body:
  - type: input
    id: feature_name
    attributes:
      label: Feature Name
      placeholder: Canvas traditional tree-view mode
    validations:
      required: true
  - type: textarea
    id: outcome
    attributes:
      label: Outcome
      description: User/problem outcome this feature should deliver.
      placeholder: Let users switch from force-directed map to deterministic tree hierarchy on /canvas.
    validations:
      required: true
  - type: textarea
    id: scope
    attributes:
      label: Scope
      description: In-scope and out-of-scope boundaries.
    validations:
      required: true
  - type: input
    id: docs_project_id
    attributes:
      label: Docs Project ID
      placeholder: "1025"
    validations:
      required: true
  - type: input
    id: target_date
    attributes:
      label: Target Date
      description: YYYY-MM-DD for roadmap view.
      placeholder: 2026-03-15
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance Criteria
      description: Concrete completion criteria used for closure.
    validations:
      required: true
""",
    "task.yml": """name: Task
description: Track operational or implementation work that is not a bug/incident/feature.
title: "[Task] "
labels:
  - type:task
  - status:triaged
body:
  - type: input
    id: summary
    attributes:
      label: Summary
      placeholder: Add project board field conventions to docs runbook.
    validations:
      required: true
  - type: textarea
    id: deliverable
    attributes:
      label: Deliverable
      description: Expected output/result.
    validations:
      required: true
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - P0
        - P1
        - P2
    validations:
      required: true
  - type: input
    id: docs_project_id
    attributes:
      label: Docs Project ID
      placeholder: "1027"
    validations:
      required: true
  - type: textarea
    id: notes
    attributes:
      label: Notes
      description: Additional constraints, dependencies, or references.
""",
}


@dataclass
class ProjectDoc:
    project_id: str
    title: str
    path: str
    status_folder: str
    description: str
    owner: str
    last_updated: str
    next_checkpoint_target: str
    blockers: list[str]
    dependencies: list[str]
    issue_type: str
    priority_label: str
    area_label: str
    target_date: str | None


@dataclass
class ProjectFieldMap:
    project_id: str
    project_url: str
    field_id_by_name: dict[str, str]
    single_select_option_id: dict[str, dict[str, str]]


@dataclass
class ProjectItemPayload:
    issue_url: str
    issue_title: str
    issue_type: str
    priority: str
    area: str
    docs_project_id: str
    incident_id: str
    status: str
    start_date: str | None
    target_date: str | None
    completed_date: str | None


class CommandError(RuntimeError):
    pass


def run_cmd(
    cmd: list[str],
    cwd: Path,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        input=input_text,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise CommandError(
            f"command failed: {' '.join(cmd)}\n"
            f"exit={result.returncode}\n"
            f"stdout={result.stdout.strip()}\n"
            f"stderr={result.stderr.strip()}"
        )
    return result


def run_cmd_json(cmd: list[str], cwd: Path) -> Any:
    raw = run_cmd(cmd, cwd=cwd).stdout.strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CommandError(f"invalid JSON from command: {' '.join(cmd)}\nerror={exc}\nraw={raw[:300]}") from exc


def require_tool(binary: str) -> None:
    if shutil.which(binary):
        return
    raise CommandError(f"required tool not found in PATH: {binary}")


def normalize_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def normalize_iso_date(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", value)
    return match.group(1) if match else None


def extract_frontmatter(raw: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n?", raw, flags=re.DOTALL)
    if not match:
        return {}

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if not m:
            continue
        key = m.group(1)
        value = m.group(2).strip().strip('"').strip("'")
        frontmatter[key] = value
    return frontmatter


def extract_section_lines(raw: str, heading: str) -> list[str]:
    pattern = re.compile(rf"^##+\s+{re.escape(heading)}\s*$", flags=re.IGNORECASE | re.MULTILINE)
    start_match = pattern.search(raw)
    if not start_match:
        return []

    start = start_match.end()
    next_heading = re.search(r"^##+\s+", raw[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(raw)
    section = raw[start:end]

    lines: list[str] = []
    for line in section.splitlines():
        stripped = re.sub(r"^\s*[-*]\s*", "", line).strip()
        if stripped:
            lines.append(stripped)
    return lines


def infer_issue_type(raw: str, title: str, status_folder: str) -> str:
    corpus = f"{title}\n{raw}"
    if re.search(r"\bincident\b", corpus, flags=re.IGNORECASE):
        return "incident"
    if re.search(r"\bbug\b|\bdefect\b|\bregression\b", corpus, flags=re.IGNORECASE):
        return "bug"
    if re.search(r"\bfeature\b|\broadmap\b|\bmilestone\b|\bdelivery\b", corpus, flags=re.IGNORECASE):
        return "feature"
    if status_folder in {"active", "backlog"}:
        return "feature"
    return "task"


def infer_priority_label(raw: str, title: str, status_folder: str) -> str:
    corpus = f"{title}\n{raw}"
    priority_match = re.search(r"\bP([0-2])\b", corpus)
    if priority_match:
        return f"priority:p{priority_match.group(1)}"
    if status_folder == "active":
        return "priority:p1"
    return "priority:p2"


def infer_area_label(raw: str, title: str, path: str) -> str:
    corpus = f"{path}\n{title}\n{raw}"
    for pattern, label in AREA_RULES:
        if pattern.search(corpus):
            return label
    return "area:ops"


def extract_target_date(raw: str) -> str | None:
    for line in raw.splitlines():
        if re.search(r"target\s+date", line, flags=re.IGNORECASE):
            value = normalize_iso_date(line)
            if value:
                return value
    return None


def discover_repo_inputs(repo_root: Path) -> dict[str, Any]:
    files = run_cmd(["rg", "--files"], cwd=repo_root).stdout.splitlines()

    roadmap = None
    changelog = None
    agents = None
    for file in files:
        if file == "ROADMAP.md" or file.endswith("/ROADMAP.md"):
            roadmap = file
        if file == "CHANGELOG.md" or file.endswith("/CHANGELOG.md"):
            changelog = file
        if file == "AGENTS.md" or file.endswith("/AGENTS.md"):
            agents = file

    project_pattern = re.compile(
        r"^(?P<root>(?:DOCS|docs)/(?:PROJECTS|projects))/"
        r"(?P<status>active|backlog|drafts|stale|completed)/"
        r"(?P<name>[^/]+\.md)$"
    )

    by_root: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for file in files:
        match = project_pattern.match(file)
        if not match:
            continue
        by_root[match.group("root")].append((file, match.group("status")))

    if not by_root:
        raise CommandError("could not discover docs project folders (expected DOCS/PROJECTS/*)")

    project_root = max(by_root.items(), key=lambda item: len(item[1]))[0]
    project_files = by_root[project_root]
    docs_root = project_root.split("/", 1)[0]

    return {
        "agents": agents,
        "changelog": changelog,
        "roadmap": roadmap,
        "project_root": project_root,
        "docs_root": docs_root,
        "project_files": project_files,
    }


def parse_project_doc(repo_root: Path, path: str, status_folder: str) -> ProjectDoc:
    raw = (repo_root / path).read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(raw)

    project_id_match = re.match(r"^(\d{4,})_", Path(path).name)
    title_match = re.search(r"^#\s+(.+)$", raw, flags=re.MULTILINE)

    project_id = project_id_match.group(1) if project_id_match else "unknown"
    title = frontmatter.get("title") or (title_match.group(1).strip() if title_match else Path(path).stem)

    dependencies = extract_section_lines(raw, "Dependencies")

    blockers: list[str] = []
    for line in raw.splitlines():
        if re.search(r"\bblocker\b|\bblocked\b|\brisk\b|\bdependency\b", line, flags=re.IGNORECASE):
            stripped = re.sub(r"^\s*[-*]\s*", "", line).strip()
            if stripped and stripped not in blockers:
                blockers.append(stripped)

    next_checkpoint_matches = re.findall(
        r"Next before next checkpoint:\s*(.+)$", raw, flags=re.IGNORECASE | re.MULTILINE
    )
    next_checkpoint_target = next_checkpoint_matches[-1].strip() if next_checkpoint_matches else "Not specified"

    issue_type = infer_issue_type(raw, title, status_folder)
    priority_label = infer_priority_label(raw, title, status_folder)
    area_label = infer_area_label(raw, title, path)

    return ProjectDoc(
        project_id=project_id,
        title=title,
        path=path,
        status_folder=status_folder,
        description=frontmatter.get("description", ""),
        owner=frontmatter.get("owner", "Unknown"),
        last_updated=frontmatter.get("lastUpdated", "Unknown"),
        next_checkpoint_target=next_checkpoint_target,
        blockers=blockers[:10],
        dependencies=dependencies[:10],
        issue_type=issue_type,
        priority_label=priority_label,
        area_label=area_label,
        target_date=extract_target_date(raw),
    )


def parse_active_execution_order(roadmap_text: str) -> list[str]:
    section_match = re.search(
        r"##\s+Active Execution Order\s*(.+?)(?:\n##\s+|\Z)",
        roadmap_text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not section_match:
        return []

    lines = section_match.group(1).splitlines()
    project_ids: list[str] = []
    for line in lines:
        match = re.search(r"`(\d{4,})`", line)
        if not match:
            match = re.search(r"\b(\d{4,})\b", line)
        if match:
            value = match.group(1)
            if value not in project_ids:
                project_ids.append(value)
    return project_ids


def gh_repo_slug(repo_root: Path, explicit_repo: str | None) -> str:
    if explicit_repo:
        return explicit_repo

    result = run_cmd(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        cwd=repo_root,
    )
    value = result.stdout.strip()
    if not value:
        raise CommandError("could not determine repo slug from gh repo view")
    return value


def gh_auth_status(repo_root: Path) -> None:
    run_cmd(["gh", "auth", "status"], cwd=repo_root)


def gh_list_labels(repo_root: Path, repo: str) -> set[str]:
    result = run_cmd(["gh", "label", "list", "-R", repo, "--limit", "1000", "--json", "name"], cwd=repo_root)
    payload = json.loads(result.stdout or "[]")
    return {item.get("name", "") for item in payload if item.get("name")}


def ensure_labels(repo_root: Path, repo: str, labels: set[str], apply: bool) -> None:
    existing = gh_list_labels(repo_root, repo)
    missing = sorted(label for label in labels if label not in existing)
    for label in missing:
        config = LABEL_DEFS.get(label, {"color": "5319E7", "description": "Auto-created label"})
        if apply:
            run_cmd(
                [
                    "gh",
                    "label",
                    "create",
                    label,
                    "-R",
                    repo,
                    "--color",
                    config["color"],
                    "--description",
                    config["description"],
                ],
                cwd=repo_root,
            )
            print(f"[apply] created label {label}")
        else:
            print(f"[dry-run] would create label {label}")


def ensure_issue_templates(
    repo_root: Path,
    repo: str,
    docs_root: str,
    apply: bool,
    overwrite: bool,
) -> None:
    template_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    desired = {
        name: content.format(repo=repo, docs_root=docs_root)
        for name, content in ISSUE_TEMPLATE_CONFIG.items()
    }

    for file_name, content in desired.items():
        target = template_dir / file_name
        exists = target.exists()

        if exists and not overwrite:
            print(f"[skip] issue template exists: {target}")
            continue

        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            action = "updated" if exists else "created"
            print(f"[apply] {action} issue template {target}")
        else:
            action = "update" if exists else "create"
            print(f"[dry-run] would {action} issue template {target}")


def gh_list_issues(repo_root: Path, repo: str) -> list[dict[str, Any]]:
    result = run_cmd(
        [
            "gh",
            "issue",
            "list",
            "-R",
            repo,
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "number,title,body,url,labels,state",
        ],
        cwd=repo_root,
    )
    return json.loads(result.stdout or "[]")


def marker_for_project(project: ProjectDoc) -> str:
    return f"<!-- docs-project-sync:key:project-{project.project_id} -->"


def marker_for_roadmap() -> str:
    return "<!-- docs-project-sync:key:roadmap -->"


def build_project_issue(project: ProjectDoc) -> tuple[str, str, list[str]]:
    type_label = f"type:{project.issue_type}"
    status_label = STATUS_LABEL_BY_FOLDER.get(project.status_folder, "status:triaged")

    title_prefix = f"[Project {project.project_id}]" if project.project_id != "unknown" else "[Project]"
    title = f"{title_prefix} {project.title}"

    deps = "\n".join(f"- {item}" for item in project.dependencies) or "- None recorded"
    blockers = "\n".join(f"- {item}" for item in project.blockers) or "- None explicitly recorded"

    body = "\n".join(
        [
            marker_for_project(project),
            "",
            f"Docs Project ID: {project.project_id}",
            f"Docs Status: {project.status_folder}",
            f"Source Doc: {project.path}",
            f"Owner: {project.owner}",
            f"Last Updated: {project.last_updated}",
            "",
            "Summary",
            project.description or "No description present in frontmatter.",
            "",
            "Dependencies",
            deps,
            "",
            "Blockers/Risks",
            blockers,
            "",
            "Next Checkpoint Target",
            project.next_checkpoint_target,
        ]
    )

    labels = [type_label, project.priority_label, project.area_label, status_label]
    return title, body, labels


def parse_issue_number_from_url(url: str) -> int | None:
    match = re.search(r"/issues/(\d+)$", url)
    return int(match.group(1)) if match else None


def build_existing_issue_map(issues: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    markers: dict[str, dict[str, Any]] = {}
    for issue in issues:
        body = issue.get("body") or ""
        for marker in re.findall(r"<!--\s*docs-project-sync:key:[^>]+-->", body):
            markers[marker.strip()] = issue
    return markers


def upsert_issue(
    repo_root: Path,
    repo: str,
    existing_by_marker: dict[str, dict[str, Any]],
    marker: str,
    title: str,
    body: str,
    desired_labels: list[str],
    apply: bool,
) -> dict[str, Any]:
    existing = existing_by_marker.get(marker)

    if existing:
        number = existing["number"]
        url = existing["url"]
        current_labels = {label.get("name") for label in existing.get("labels", []) if label.get("name")}
        desired_set = set(desired_labels)

        remove_labels = sorted(
            label
            for label in current_labels
            if (
                label.startswith("type:")
                or label.startswith("priority:")
                or label.startswith("status:")
                or label.startswith("area:")
            )
            and label not in desired_set
        )
        add_labels = sorted(label for label in desired_set if label not in current_labels)

        if apply:
            cmd = [
                "gh",
                "issue",
                "edit",
                str(number),
                "-R",
                repo,
                "--title",
                title,
                "--body-file",
                "-",
            ]
            if add_labels:
                cmd += ["--add-label", ",".join(add_labels)]
            if remove_labels:
                cmd += ["--remove-label", ",".join(remove_labels)]

            run_cmd(cmd, cwd=repo_root, input_text=body)
            print(f"[apply] updated issue #{number} ({url})")
        else:
            print(f"[dry-run] would update issue #{number} ({url})")

        result = dict(existing)
        result["labels"] = [{"name": label} for label in sorted(desired_set)]
        result["title"] = title
        result["body"] = body
        return result

    if apply:
        cmd = [
            "gh",
            "issue",
            "create",
            "-R",
            repo,
            "--title",
            title,
            "--body-file",
            "-",
            "--label",
            ",".join(desired_labels),
        ]
        result = run_cmd(cmd, cwd=repo_root, input_text=body)
        url = result.stdout.strip().splitlines()[-1].strip()
        number = parse_issue_number_from_url(url)
        print(f"[apply] created issue {url}")
    else:
        url = f"https://github.com/{repo}/issues/<new>"
        number = None
        print(f"[dry-run] would create issue: {title}")

    return {
        "number": number,
        "url": url,
        "title": title,
        "body": body,
        "labels": [{"name": label} for label in desired_labels],
    }


def build_roadmap_issue_body(
    roadmap_path: str,
    project_docs: list[ProjectDoc],
    project_issue_urls: dict[str, str],
    execution_order: list[str],
) -> str:
    project_by_id = {item.project_id: item for item in project_docs if item.project_id != "unknown"}

    checklist: list[str] = []
    seen: set[str] = set()
    for project_id in execution_order:
        project = project_by_id.get(project_id)
        if not project:
            continue
        issue_url = project_issue_urls.get(project_id, "(issue pending)")
        checklist.append(
            f"- [ ] `{project_id}` - {project.title} ({project.status_folder}) - {issue_url} - doc: `{project.path}`"
        )
        seen.add(project_id)

    for project in project_docs:
        if project.project_id in seen:
            continue
        issue_url = project_issue_urls.get(project.project_id, "(issue pending)")
        checklist.append(
            f"- [ ] `{project.project_id}` - {project.title} ({project.status_folder}) - {issue_url} - doc: `{project.path}`"
        )

    checklist_text = "\n".join(checklist) if checklist else "- [ ] No project docs discovered for sync scope."

    body = "\n".join(
        [
            marker_for_roadmap(),
            "",
            "Source of truth for planning remains repo docs; this issue mirrors execution order into GitHub.",
            f"Roadmap source: `{roadmap_path}`",
            "",
            "Execution Checklist",
            checklist_text,
            "",
            "Sync Rules",
            "- This issue is managed by docs tracking sync automation.",
            "- Edit docs first; rerun sync to reflect changes in GitHub.",
            "- Keep operational ownership in GitHub Issues/Project and policy narrative in docs.",
        ]
    )
    return body


def collect_issue_urls_from_project_items(payload: Any) -> set[str]:
    urls: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, inner in value.items():
                if key == "url" and isinstance(inner, str) and "/issues/" in inner:
                    urls.add(inner)
                walk(inner)
        elif isinstance(value, list):
            for inner in value:
                walk(inner)

    walk(payload)
    return urls


def normalize_projects_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("projects"), list):
        return payload["projects"]
    if isinstance(payload, list):
        return payload
    return []


def normalize_fields_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("fields"), list):
        return payload["fields"]
    if isinstance(payload, list):
        return payload
    return []


def normalize_items_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    if isinstance(payload, list):
        return payload
    return []


def ensure_project_number(
    repo_root: Path,
    owner: str,
    title: str,
    repo_slug: str,
    number: int | None,
    bootstrap_project: bool,
    apply: bool,
    link_repo: bool,
) -> int | None:
    if number:
        return number

    projects_payload = run_cmd_json(["gh", "project", "list", "--owner", owner, "--format", "json"], cwd=repo_root)
    projects = normalize_projects_payload(projects_payload)
    existing = next((item for item in projects if str(item.get("title", "")).lower() == title.lower()), None)
    if existing and existing.get("number"):
        existing_number = int(existing["number"])
        print(f"[project] reusing existing project #{existing_number}: {title}")
        return existing_number

    if not bootstrap_project:
        raise CommandError("project number not found; pass --project-number or set --bootstrap-project")

    if not apply:
        print(f"[dry-run] would create project board: {title}")
        return None

    created = run_cmd_json(["gh", "project", "create", "--owner", owner, "--title", title, "--format", "json"], cwd=repo_root)
    created_number = int(created["number"])
    print(f"[apply] created project #{created_number}: {title}")

    if link_repo:
        run_cmd(["gh", "project", "link", str(created_number), "--owner", owner, "--repo", repo_slug], cwd=repo_root)
        print(f"[apply] linked repository to project: {repo_slug}")

    return created_number


def ensure_project_metadata(repo_root: Path, owner: str, project_number: int, apply: bool) -> None:
    description = (
        "Execution board for incidents, bugs, tasks, and feature roadmap tracking; "
        "DOCS remains governance source of truth."
    )
    readme = (
        "Use this as the execution system of record. Keep Docs Project ID and Incident ID fields "
        "populated and mirror key checkpoints in DOCS."
    )

    if apply:
        run_cmd(
            [
                "gh",
                "project",
                "edit",
                str(project_number),
                "--owner",
                owner,
                "--description",
                description,
                "--readme",
                readme,
            ],
            cwd=repo_root,
        )
        print("[apply] updated project description/readme")
    else:
        print("[dry-run] would update project description/readme")


def ensure_project_fields(repo_root: Path, owner: str, project_number: int, apply: bool) -> None:
    field_payload = run_cmd_json(
        ["gh", "project", "field-list", str(project_number), "--owner", owner, "--format", "json"],
        cwd=repo_root,
    )
    existing = {str(field.get("name", "")).lower() for field in normalize_fields_payload(field_payload)}

    for spec in FIELD_SPECS:
        if spec["name"].lower() in existing:
            print(f"[project] field exists: {spec['name']}")
            continue

        if apply:
            cmd = [
                "gh",
                "project",
                "field-create",
                str(project_number),
                "--owner",
                owner,
                "--name",
                spec["name"],
                "--data-type",
                spec["data_type"],
            ]
            if spec["data_type"] == "SINGLE_SELECT":
                cmd += ["--single-select-options", ",".join(spec["options"])]
            run_cmd(cmd, cwd=repo_root)
            print(f"[apply] created project field: {spec['name']}")
        else:
            print(f"[dry-run] would create project field: {spec['name']}")


def get_project_field_map(repo_root: Path, owner: str, project_number: int) -> ProjectFieldMap:
    project_view = run_cmd_json(
        ["gh", "project", "view", str(project_number), "--owner", owner, "--format", "json"],
        cwd=repo_root,
    )
    field_payload = run_cmd_json(
        ["gh", "project", "field-list", str(project_number), "--owner", owner, "--format", "json"],
        cwd=repo_root,
    )
    fields = normalize_fields_payload(field_payload)

    field_id_by_name: dict[str, str] = {}
    single_select_option_id: dict[str, dict[str, str]] = {}

    for field in fields:
        name = str(field.get("name", "")).strip()
        field_id = str(field.get("id", "")).strip()
        if not name or not field_id:
            continue
        field_id_by_name[name] = field_id

        options = field.get("options")
        if isinstance(options, list):
            option_map: dict[str, str] = {}
            for option in options:
                option_name = str(option.get("name", "")).strip()
                option_id = str(option.get("id", "")).strip()
                if option_name and option_id:
                    option_map[option_name.lower()] = option_id
            single_select_option_id[name] = option_map

    project_id = str(project_view.get("id", "")).strip()
    project_url = str(project_view.get("url", "")).strip()

    if not project_id:
        raise CommandError("could not resolve GitHub project id")

    return ProjectFieldMap(
        project_id=project_id,
        project_url=project_url,
        field_id_by_name=field_id_by_name,
        single_select_option_id=single_select_option_id,
    )


def issue_url_from_project_item(item: dict[str, Any]) -> str | None:
    content = item.get("content")
    if isinstance(content, dict):
        url = content.get("url")
        if isinstance(url, str) and "/issues/" in url:
            return url

    url = item.get("url")
    if isinstance(url, str) and "/issues/" in url:
        return url

    return None


def project_item_map_by_issue_url(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapping: dict[str, dict[str, Any]] = {}
    for item in items:
        url = issue_url_from_project_item(item)
        if url:
            mapping[url] = item
    return mapping


def set_project_item_field(
    repo_root: Path,
    owner: str,
    project_number: int,
    field_map: ProjectFieldMap,
    item_id: str,
    field_name: str,
    value: str | None,
    value_type: str,
    apply: bool,
) -> None:
    field_id = field_map.field_id_by_name.get(field_name)
    if not field_id:
        print(f"[warn] project field not found: {field_name}")
        return

    if value is None or value == "":
        return

    cmd = [
        "gh",
        "project",
        "item-edit",
        "--id",
        item_id,
        "--project-id",
        field_map.project_id,
        "--field-id",
        field_id,
    ]

    if value_type == "single-select":
        option_id = field_map.single_select_option_id.get(field_name, {}).get(value.lower())
        if not option_id:
            print(f"[warn] option not found for {field_name}: {value}")
            return
        cmd += ["--single-select-option-id", option_id]
    elif value_type == "text":
        cmd += ["--text", value]
    elif value_type == "date":
        cmd += ["--date", value]
    else:
        raise CommandError(f"unsupported value_type: {value_type}")

    if apply:
        run_cmd(cmd, cwd=repo_root)
        print(f"[apply] set {field_name}={value} for item {item_id}")
    else:
        print(f"[dry-run] would set {field_name}={value} for item {item_id}")


def sync_project_board(
    repo_root: Path,
    owner: str,
    project_number: int,
    items: list[ProjectItemPayload],
    apply: bool,
    set_project_fields: bool,
) -> None:
    item_payload = run_cmd_json(
        [
            "gh",
            "project",
            "item-list",
            str(project_number),
            "--owner",
            owner,
            "--limit",
            "1000",
            "--format",
            "json",
        ],
        cwd=repo_root,
    )
    existing_items = normalize_items_payload(item_payload)
    existing_by_url = project_item_map_by_issue_url(existing_items)

    for payload in items:
        if payload.issue_url in existing_by_url:
            if apply:
                print(f"[apply] project item already exists for {payload.issue_url}")
            else:
                print(f"[dry-run] project item already exists for {payload.issue_url}")
            continue

        if apply:
            run_cmd(
                [
                    "gh",
                    "project",
                    "item-add",
                    str(project_number),
                    "--owner",
                    owner,
                    "--url",
                    payload.issue_url,
                ],
                cwd=repo_root,
            )
            print(f"[apply] added project item for {payload.issue_url}")
        else:
            print(f"[dry-run] would add project item for {payload.issue_url}")

    if not apply:
        if set_project_fields:
            print("[dry-run] would map project fields after item add")
        return

    if not set_project_fields:
        return

    refreshed_payload = run_cmd_json(
        [
            "gh",
            "project",
            "item-list",
            str(project_number),
            "--owner",
            owner,
            "--limit",
            "1000",
            "--format",
            "json",
        ],
        cwd=repo_root,
    )
    refreshed_items = normalize_items_payload(refreshed_payload)
    item_by_url = project_item_map_by_issue_url(refreshed_items)

    field_map = get_project_field_map(repo_root, owner, project_number)
    print(f"[project] url: {field_map.project_url}")

    for payload in items:
        item = item_by_url.get(payload.issue_url)
        if not item:
            print(f"[warn] project item not found after add: {payload.issue_url}")
            continue

        item_id = str(item.get("id", "")).strip()
        if not item_id:
            print(f"[warn] project item missing id: {payload.issue_url}")
            continue

        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Type", payload.issue_type, "single-select", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Priority", payload.priority, "single-select", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Area", payload.area, "single-select", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Status", payload.status, "single-select", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Docs Project ID", payload.docs_project_id, "text", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Incident ID", payload.incident_id, "text", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Start Date", payload.start_date, "date", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Target Date", payload.target_date, "date", apply)
        set_project_item_field(repo_root, owner, project_number, field_map, item_id, "Completed Date", payload.completed_date, "date", apply)


def marker_incident_id_from_body(body: str) -> str:
    match = re.search(r"^Incident ID:\s*(.+)$", body, flags=re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs-based project tracking to GitHub issues/projects/roadmap.")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--repo", default=None, help="GitHub repo slug OWNER/REPO (auto-detected if omitted)")

    parser.add_argument("--include-completed", action="store_true", help="Include completed project docs")
    parser.add_argument("--backfill-completed", action="store_true", help="Backfill all completed project docs into GitHub issues")
    parser.add_argument("--completed-only", action="store_true", help="Sync only completed project docs")

    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--max-projects", type=int, default=0, help="Limit project docs for testing")

    parser.add_argument("--minimal-labels", action="store_true", help="Only ensure labels referenced by current sync scope")
    parser.add_argument("--install-issue-templates", action="store_true", help="Install 1027 issue templates into .github/ISSUE_TEMPLATE")
    parser.add_argument("--overwrite-issue-templates", action="store_true", help="Overwrite existing issue templates when installing")

    parser.add_argument("--sync-roadmap-issue", action=argparse.BooleanOptionalAction, default=True, help="Create/update the roadmap mirror issue")
    parser.add_argument("--roadmap-title", default="Roadmap Sync", help="GitHub roadmap issue title")

    parser.add_argument("--project-owner", default=None, help="GitHub project owner login/org")
    parser.add_argument("--project-number", type=int, default=None, help="GitHub project number")
    parser.add_argument("--project-title", default="Ops + Delivery", help="Project title when bootstrapping without explicit number")
    parser.add_argument("--bootstrap-project", action="store_true", help="Create/reuse a single execution project board when number is not provided")
    parser.add_argument("--link-project-repo", action=argparse.BooleanOptionalAction, default=True, help="Link repository to bootstrapped project")
    parser.add_argument("--set-project-fields", action=argparse.BooleanOptionalAction, default=True, help="Map Type/Priority/Area/Docs IDs/status/date fields on project items")
    parser.add_argument("--add-roadmap-to-project", action=argparse.BooleanOptionalAction, default=True, help="Add roadmap issue to project board when board sync is enabled")

    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        print(f"repo root not found: {repo_root}", file=sys.stderr)
        return 1

    try:
        require_tool("rg")
        require_tool("gh")

        discovery = discover_repo_inputs(repo_root)
        print("[discovery]")
        print(f"  agents: {discovery['agents'] or 'not found'}")
        print(f"  changelog: {discovery['changelog'] or 'not found'}")
        print(f"  roadmap: {discovery['roadmap'] or 'not found'}")
        print(f"  project root: {discovery['project_root']}")

        if args.completed_only:
            include_statuses = {"completed"}
        else:
            include_statuses = {"active", "backlog", "drafts", "stale"}
            if args.include_completed or args.backfill_completed:
                include_statuses.add("completed")

        docs = [
            parse_project_doc(repo_root, path=file_path, status_folder=status)
            for (file_path, status) in discovery["project_files"]
            if status in include_statuses
        ]
        docs.sort(key=lambda item: (item.project_id, item.path))

        if args.max_projects > 0:
            docs = docs[: args.max_projects]

        if not docs:
            raise CommandError("no project docs discovered after status filtering")

        repo_slug = gh_repo_slug(repo_root, args.repo)
        print(f"  github repo: {repo_slug}")

        gh_auth_status(repo_root)

        if args.minimal_labels:
            label_set = {"type:task", "area:docs", "priority:p2", "status:triaged"}
            for doc in docs:
                label_set.update(
                    {
                        f"type:{doc.issue_type}",
                        doc.priority_label,
                        doc.area_label,
                        STATUS_LABEL_BY_FOLDER.get(doc.status_folder, "status:triaged"),
                    }
                )
        else:
            label_set = set(LABEL_DEFS.keys())

        ensure_labels(repo_root, repo_slug, label_set, apply=args.apply)

        if args.install_issue_templates:
            ensure_issue_templates(
                repo_root=repo_root,
                repo=repo_slug,
                docs_root=discovery["docs_root"],
                apply=args.apply,
                overwrite=args.overwrite_issue_templates,
            )

        issues = gh_list_issues(repo_root, repo_slug)
        existing_by_marker = build_existing_issue_map(issues)

        project_issue_urls: dict[str, str] = {}
        synced_issue_records: list[dict[str, Any]] = []

        for doc in docs:
            title, body, labels = build_project_issue(doc)
            synced = upsert_issue(
                repo_root=repo_root,
                repo=repo_slug,
                existing_by_marker=existing_by_marker,
                marker=marker_for_project(doc),
                title=title,
                body=body,
                desired_labels=labels,
                apply=args.apply,
            )
            synced_issue_records.append(synced)
            existing_by_marker[marker_for_project(doc)] = synced
            project_issue_urls[doc.project_id] = synced.get("url", "")

        roadmap_issue: dict[str, Any] | None = None
        execution_order: list[str] = []

        roadmap_path = discovery["roadmap"]
        if roadmap_path:
            execution_order = parse_active_execution_order((repo_root / roadmap_path).read_text(encoding="utf-8"))

        if args.sync_roadmap_issue:
            roadmap_body = build_roadmap_issue_body(
                roadmap_path=roadmap_path or "ROADMAP.md (not found)",
                project_docs=docs,
                project_issue_urls=project_issue_urls,
                execution_order=execution_order,
            )

            roadmap_issue = upsert_issue(
                repo_root=repo_root,
                repo=repo_slug,
                existing_by_marker=existing_by_marker,
                marker=marker_for_roadmap(),
                title=args.roadmap_title,
                body=roadmap_body,
                desired_labels=["type:task", "area:docs", "priority:p2", "status:triaged"],
                apply=args.apply,
            )

        if args.project_number and not args.project_owner:
            raise CommandError("--project-owner is required when --project-number is provided")

        resolved_project_number: int | None = None

        if args.project_owner:
            project_number = ensure_project_number(
                repo_root=repo_root,
                owner=args.project_owner,
                title=args.project_title,
                repo_slug=repo_slug,
                number=args.project_number,
                bootstrap_project=args.bootstrap_project,
                apply=args.apply,
                link_repo=args.link_project_repo,
            )
            resolved_project_number = project_number

            if project_number is not None:
                if args.bootstrap_project:
                    ensure_project_metadata(repo_root, args.project_owner, project_number, apply=args.apply)
                    ensure_project_fields(repo_root, args.project_owner, project_number, apply=args.apply)

                payloads: list[ProjectItemPayload] = []
                for doc, issue in zip(docs, synced_issue_records):
                    url = issue.get("url", "")
                    if not isinstance(url, str) or not url.startswith("https://github.com/"):
                        continue
                    body = issue.get("body", "")
                    incident_id = marker_incident_id_from_body(body) if doc.issue_type == "incident" else ""
                    payloads.append(
                        ProjectItemPayload(
                            issue_url=url,
                            issue_title=str(issue.get("title", doc.title)),
                            issue_type=doc.issue_type,
                            priority=doc.priority_label.replace("priority:", ""),
                            area=doc.area_label.replace("area:", ""),
                            docs_project_id=doc.project_id if doc.project_id != "unknown" else "",
                            incident_id=incident_id,
                            status=PROJECT_STATUS_BY_FOLDER.get(doc.status_folder, "Triaged"),
                            start_date=normalize_iso_date(doc.last_updated),
                            target_date=doc.target_date,
                            completed_date=normalize_iso_date(doc.last_updated) if doc.status_folder == "completed" else None,
                        )
                    )

                if roadmap_issue and args.add_roadmap_to_project:
                    url = roadmap_issue.get("url", "")
                    if isinstance(url, str) and url.startswith("https://github.com/"):
                        payloads.append(
                            ProjectItemPayload(
                                issue_url=url,
                                issue_title=str(roadmap_issue.get("title", args.roadmap_title)),
                                issue_type="task",
                                priority="p2",
                                area="docs",
                                docs_project_id="",
                                incident_id="",
                                status="Triaged",
                                start_date=None,
                                target_date=None,
                                completed_date=None,
                            )
                        )

                sync_project_board(
                    repo_root=repo_root,
                    owner=args.project_owner,
                    project_number=project_number,
                    items=payloads,
                    apply=args.apply,
                    set_project_fields=args.set_project_fields,
                )
            else:
                print("[dry-run] project number unresolved (would be created). skipping project item sync.")

        mode = "apply" if args.apply else "dry-run"
        print("[summary]")
        print(f"  mode: {mode}")
        print(f"  synced project docs: {len(docs)}")
        print("  statuses in scope: " + ", ".join(sorted(include_statuses)))
        if args.sync_roadmap_issue:
            print(f"  roadmap issue title: {args.roadmap_title}")
        if args.project_owner:
            print(f"  project owner: {args.project_owner}")
            if resolved_project_number is None:
                print("  project number: (would resolve/create during apply)")
            else:
                print(f"  project number: {resolved_project_number}")
        return 0

    except CommandError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
