#!/usr/bin/env python3
"""Generate a human-readable index and machine-readable manifest for skills/."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
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


@dataclass
class SuiteDriftReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    def format(self) -> str:
        lines: list[str] = []
        if self.errors:
            lines.append("Catalog drift detected:")
            lines.extend(f"- {error}" for error in self.errors)
        if self.warnings:
            if lines:
                lines.append("")
            lines.append("Catalog drift warnings:")
            lines.extend(f"- {warning}" for warning in self.warnings)
        return "\n".join(lines) if lines else "No catalog drift detected."


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


def load_suite_list() -> list[str]:
    if not SUITE_LIST_PATH.exists():
        return []
    return [
        line.strip()
        for line in SUITE_LIST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def load_suite_metadata() -> dict[str, dict[str, str]]:
    if not SUITE_METADATA_PATH.exists():
        return {}
    data = json.loads(SUITE_METADATA_PATH.read_text(encoding="utf-8"))
    skills = data.get("skills", {})
    if not isinstance(skills, dict):
        raise ValueError(f"{SUITE_METADATA_PATH}: expected top-level 'skills' object")
    return skills


def discover_skill_dirs() -> list[str]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        p.name
        for p in SKILLS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").exists()
    )


def discover_non_skill_dirs() -> list[str]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        p.name
        for p in SKILLS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".") and not (p / "SKILL.md").exists()
    )


def validate_metadata(skill_folder: str, metadata: dict[str, str]) -> None:
    status = metadata.get("status", "active")
    if status not in ALLOWED_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_STATUSES))
        raise ValueError(f"{skill_folder}: invalid status '{status}'. Allowed statuses: {allowed}")

    if status == "deprecated" and not metadata.get("replacement"):
        raise ValueError(f"{skill_folder}: deprecated skills must declare a replacement")

    if status == "archived" and not metadata.get("note"):
        raise ValueError(f"{skill_folder}: archived skills must include a note explaining why they are retained")


def detect_suite_drift() -> SuiteDriftReport:
    suite_list = load_suite_list()
    suite_counts = Counter(suite_list)
    suite_set = set(suite_list)
    skill_dirs = set(discover_skill_dirs())
    non_skill_dirs = discover_non_skill_dirs()
    metadata = load_suite_metadata()
    metadata_set = set(metadata)

    report = SuiteDriftReport()

    if not SUITE_LIST_PATH.exists():
        report.errors.append(f"Missing suite allowlist: {SUITE_LIST_PATH.relative_to(REPO_ROOT)}")
    if not SUITE_METADATA_PATH.exists():
        report.errors.append(f"Missing lifecycle metadata file: {SUITE_METADATA_PATH.relative_to(REPO_ROOT)}")

    duplicates = sorted(name for name, count in suite_counts.items() if count > 1)
    if duplicates:
        report.errors.append(
            "Duplicate entries in skills/SUITE_SKILLS.txt: " + ", ".join(duplicates)
        )

    missing_from_disk = sorted(suite_set - skill_dirs)
    if missing_from_disk:
        report.errors.append(
            "Listed in skills/SUITE_SKILLS.txt but missing a skills/<name>/SKILL.md folder: "
            + ", ".join(missing_from_disk)
        )

    missing_from_suite = sorted(skill_dirs - suite_set)
    if missing_from_suite:
        report.errors.append(
            "Present in skills/ with SKILL.md but missing from skills/SUITE_SKILLS.txt: "
            + ", ".join(missing_from_suite)
        )

    metadata_not_in_suite = sorted(metadata_set - suite_set)
    if metadata_not_in_suite:
        report.errors.append(
            "Present in skills/SUITE_METADATA.json but missing from skills/SUITE_SKILLS.txt: "
            + ", ".join(metadata_not_in_suite)
        )

    metadata_missing_from_disk = sorted(metadata_set - skill_dirs)
    if metadata_missing_from_disk:
        report.errors.append(
            "Present in skills/SUITE_METADATA.json but missing a skills/<name>/SKILL.md folder: "
            + ", ".join(metadata_missing_from_disk)
        )

    if non_skill_dirs:
        report.warnings.append(
            "Directories under skills/ without SKILL.md are ignored by the catalog: "
            + ", ".join(non_skill_dirs)
        )

    for skill_folder, skill_metadata in metadata.items():
        try:
            validate_metadata(skill_folder, skill_metadata)
        except ValueError as exc:
            report.errors.append(str(exc))

    return report


def collect_skills() -> list[SkillRecord]:
    suite_metadata = load_suite_metadata()
    allowed = load_suite_list()

    if allowed:
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
        escaped_summary = summary.replace("|", "\\|")
        escaped_notes = notes_text.replace("|", "\\|")
        lines.append(
            f"| `{record.status}` | [`{label}`](./{record.folder}/SKILL.md) | {escaped_summary} | {resource_text} | {escaped_notes} |"
        )

    lines.extend(
        [
            "",
            "## Audit guardrails",
            "",
            "- Catalog generation fails before writing files when `skills/`, `skills/SUITE_SKILLS.txt`, and `skills/SUITE_METADATA.json` drift out of sync.",
            "- Run `python3 scripts/build_catalog.py --check` to audit suite membership and lifecycle metadata without regenerating files.",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the curated skills suite, then regenerate skills/manifest.json and skills/INDEX.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="only validate drift between skills/, SUITE_SKILLS.txt, and SUITE_METADATA.json; do not write generated files",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    drift_report = detect_suite_drift()
    if drift_report.has_errors:
        print(drift_report.format(), file=sys.stderr)
        return 1

    if args.check:
        print(drift_report.format())
        return 0

    if drift_report.has_warnings:
        print(drift_report.format(), file=sys.stderr)

    records = collect_skills()
    write_manifest(records)
    write_index(records)
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Wrote {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
