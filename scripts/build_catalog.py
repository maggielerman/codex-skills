#!/usr/bin/env python3
"""Generate a human-readable index and machine-readable manifest for skills/."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MANIFEST_PATH = SKILLS_DIR / "manifest.json"
INDEX_PATH = SKILLS_DIR / "INDEX.md"
SUITE_LIST_PATH = SKILLS_DIR / "SUITE_SKILLS.txt"
SUITE_METADATA_PATH = SKILLS_DIR / "SUITE_METADATA.json"
ALLOWED_STATUSES = {"active", "experimental", "legacy", "deprecated", "archived"}


@dataclass
class SkillRecord:
    folder: str
    name: str
    description: str
    display_name: str | None
    short_description: str | None
    status: str
    replacement: str | None
    note: str | None
    has_agents_metadata: bool
    has_scripts: bool
    has_references: bool
    has_assets: bool
    file_count: int


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {skill_md}")

    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def parse_openai_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    data: dict[str, str] = {}
    current_section = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" "):
            current_section = raw_line.rstrip(":").strip()
            continue
        if current_section != "interface":
            continue
        stripped = raw_line.strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def load_suite_metadata() -> dict[str, dict[str, str]]:
    if not SUITE_METADATA_PATH.exists():
        return {}
    data = json.loads(SUITE_METADATA_PATH.read_text(encoding="utf-8"))
    return data.get("skills", {})


def validate_metadata(skill_folder: str, metadata: dict[str, str]) -> None:
    status = metadata.get("status", "active")
    if status not in ALLOWED_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_STATUSES))
        raise ValueError(f"{skill_folder}: invalid status '{status}'. Allowed statuses: {allowed}")

    if status == "deprecated" and not metadata.get("replacement"):
        raise ValueError(f"{skill_folder}: deprecated skills must declare a replacement")

    if status == "archived" and not metadata.get("note"):
        raise ValueError(f"{skill_folder}: archived skills must include a note explaining why they are retained")


def collect_skills() -> list[SkillRecord]:
    suite_metadata = load_suite_metadata()

    if SUITE_LIST_PATH.exists():
        allowed = [
            line.strip()
            for line in SUITE_LIST_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        skill_dirs = [SKILLS_DIR / name for name in allowed]
    else:
        skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))

    records: list[SkillRecord] = []
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        frontmatter = parse_frontmatter(skill_md)
        interface = parse_openai_yaml(skill_dir / "agents" / "openai.yaml")
        metadata = suite_metadata.get(skill_dir.name, {})
        validate_metadata(skill_dir.name, metadata)

        records.append(
            SkillRecord(
                folder=skill_dir.name,
                name=frontmatter.get("name", skill_dir.name),
                description=frontmatter.get("description", ""),
                display_name=interface.get("display_name"),
                short_description=interface.get("short_description"),
                status=metadata.get("status", "active"),
                replacement=metadata.get("replacement"),
                note=metadata.get("note"),
                has_agents_metadata=(skill_dir / "agents" / "openai.yaml").exists(),
                has_scripts=(skill_dir / "scripts").is_dir(),
                has_references=(skill_dir / "references").is_dir() or (skill_dir / "reference").is_dir(),
                has_assets=(skill_dir / "assets").is_dir(),
                file_count=sum(1 for p in skill_dir.rglob("*") if p.is_file()),
            )
        )
    return records


def write_manifest(records: list[SkillRecord]) -> None:
    manifest = {
        "generated_by": "scripts/build_catalog.py",
        "skill_count": len(records),
        "skills": [
            {
                "folder": record.folder,
                "name": record.name,
                "display_name": record.display_name,
                "description": record.description,
                "short_description": record.short_description,
                "status": record.status,
                "replacement": record.replacement,
                "note": record.note,
                "path": f"skills/{record.folder}",
                "skill_md": f"skills/{record.folder}/SKILL.md",
                "has_agents_metadata": record.has_agents_metadata,
                "has_scripts": record.has_scripts,
                "has_references": record.has_references,
                "has_assets": record.has_assets,
                "file_count": record.file_count,
            }
            for record in records
        ],
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_index(records: list[SkillRecord]) -> None:
    lines = [
        "# Skills Index",
        "",
        "> This file is generated by `scripts/build_catalog.py`. Do not hand-edit.",
        "",
        f"Total skills: **{len(records)}**",
        "",
        "## Status meanings",
        "",
        "- `active` - supported for normal use",
        "- `experimental` - still evolving; expect changes",
        "- `legacy` - retained for older or transitional scenarios",
        "- `deprecated` - backward-compatibility only; prefer the listed replacement",
        "- `archived` - reference-only; do not use for new work",
        "",
        "| Status | Skill | Summary | Resources | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for record in records:
        label = record.display_name or record.name
        summary = record.short_description or record.description
        resources = []
        if record.has_scripts:
            resources.append("scripts")
        if record.has_references:
            resources.append("references")
        if record.has_assets:
            resources.append("assets")
        resource_text = ", ".join(resources) if resources else "metadata only"
        notes = []
        if record.replacement:
            notes.append(f"Use `{record.replacement}` instead")
        if record.note:
            notes.append(record.note)
        notes_text = " ".join(notes) if notes else ""
        lines.append(
            f"| `{record.status}` | [`{label}`](./{record.folder}/SKILL.md) | {summary.replace('|', '\\|')} | {resource_text} | {notes_text.replace('|', '\\|')} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This catalog is limited to the allowlisted suite in `skills/SUITE_SKILLS.txt`.",
            "- Lifecycle status comes from `skills/SUITE_METADATA.json`.",
            "- Hidden/system skills are intentionally excluded from this catalog.",
            "- Update this file by running `python3 scripts/build_catalog.py` from the repo root.",
        ]
    )

    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    records = collect_skills()
    write_manifest(records)
    write_index(records)
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Wrote {INDEX_PATH}")


if __name__ == "__main__":
    main()
