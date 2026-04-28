#!/usr/bin/env python3
"""Validate a Hyphenomenon intake dossier and screenshot pack."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADERS = [
    "# Project Intake - ",
    "## 1) Executive Summary",
    "## 2) Project Type and Domain",
    "## 3) Repository and Live URLs",
    "## 4) Product/User Journey Summary",
    "## 5) Architecture and Stack Summary",
    "## 6) Key Workflows and Operational Flows",
    "## 7) AI Context: Prompts, Chats, Agent Workflows",
    "## 8) Supporting Docs and External Resources",
    "## 9) Screenshot Gallery (with relative links + captions)",
    "## 10) Candidate Import Nodes and Relationships",
    "## 11) Risks, Gaps, and Unknowns",
    "## 12) Handoff Checklist for Hyphenomenon Import",
]

CATEGORY_PATTERNS = {
    "home/landing": re.compile(r"(home|landing)"),
    "primary workflow": re.compile(r"(primary|workflow|get-started|onboarding)"),
    "key feature/detail": re.compile(r"(key|feature|detail|donor|clinic|cryobank)"),
    "admin/settings equivalent": re.compile(r"(admin|settings|auth|dashboard)"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, help="Absolute path to repo root")
    parser.add_argument(
        "--dossier",
        default="docs/intake/ML-hyphenomenon-project-intake.md",
        help="Path relative to repo root",
    )
    parser.add_argument(
        "--screenshots-dir",
        default="docs/intake/screenshots",
        help="Path relative to repo root",
    )
    parser.add_argument("--repo-url", required=True)
    parser.add_argument("--live-url", action="append", dest="live_urls", required=True)
    return parser.parse_args()


def find_missing_headers(text: str) -> list[str]:
    missing: list[str] = []
    for header in REQUIRED_HEADERS:
        if header not in text:
            missing.append(header)
    return missing


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    dossier = repo_root / args.dossier
    screenshots_dir = repo_root / args.screenshots_dir

    errors: list[str] = []
    warnings: list[str] = []

    if not dossier.exists():
        errors.append(f"Missing dossier file: {dossier}")
        report(errors, warnings)
        return 1

    text = dossier.read_text(encoding="utf-8")

    missing_headers = find_missing_headers(text)
    if missing_headers:
        errors.append("Missing required section headers:")
        errors.extend([f"  - {h}" for h in missing_headers])

    if "### Hydration Source Artifacts" not in text:
        errors.append("Missing subsection: ### Hydration Source Artifacts")

    if args.repo_url not in text:
        warnings.append(f"Repo URL not found in dossier body: {args.repo_url}")

    for live_url in args.live_urls:
        if live_url not in text:
            warnings.append(f"Live URL not found in dossier body: {live_url}")

    if not screenshots_dir.exists():
        errors.append(f"Missing screenshots directory: {screenshots_dir}")
    else:
        pngs = sorted(p.name for p in screenshots_dir.glob("*.png"))
        if not (4 <= len(pngs) <= 8):
            errors.append(f"Screenshot count must be 4-8 PNGs. Found {len(pngs)}.")

        names_lower = [name.lower() for name in pngs]
        for label, pattern in CATEGORY_PATTERNS.items():
            if not any(pattern.search(name) for name in names_lower):
                warnings.append(
                    f"No screenshot filename clearly matches required category: {label}."
                )

    gallery_links = sorted(set(re.findall(r"\]\((\./screenshots/[^)]+)\)", text)))
    for rel in gallery_links:
        rel_clean = rel.replace("./", "", 1)
        target = dossier.parent / rel_clean
        if not target.exists():
            errors.append(f"Dossier link points to missing file: {rel}")

    if "files created/updated" not in text:
        warnings.append("The final completion phrase check applies to chat response, not dossier content.")

    report(errors, warnings)
    return 1 if errors else 0


def report(errors: list[str], warnings: list[str]) -> None:
    if errors:
        print("ERRORS:")
        for item in errors:
            print(item)
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(item)
    if not errors and not warnings:
        print("OK: Intake dossier and screenshots passed validation checks.")
    elif not errors:
        print("OK: Validation passed with warnings.")


if __name__ == "__main__":
    sys.exit(main())
