#!/usr/bin/env python3
"""Create a Hyphenomenon intake scaffold in a target repository."""

from __future__ import annotations

import argparse
from pathlib import Path


def link(url: str) -> str:
    return f"[{url}]({url})"


def build_markdown(
    project_name: str,
    repo_url: str,
    live_urls: list[str],
    source_repo_path: str,
    output_rel_path: str,
    screenshots_rel_dir: str,
) -> str:
    live_links = ", ".join(link(url) for url in live_urls)
    live_plain = ", ".join(live_urls)
    headers = [
        f"# Project Intake - {project_name}",
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

    return f"""{headers[0]}

**Project Name:** {project_name}  
**Repository:** {link(repo_url)}  
**Live URL(s):** {live_links}  
**Source Repo Path:** `{source_repo_path}`

{headers[1]}
- TODO: Add concise project-level summary and current state.

{headers[2]}
- TODO: Identify project category, domain, and user groups.

{headers[3]}
- Repo: {link(repo_url)}
- Live URLs: {live_plain}

{headers[4]}
- TODO: Summarize public and authenticated user journeys.

{headers[5]}
- TODO: Summarize frontend/backend/data/tooling stack from source files.

{headers[6]}
- TODO: Summarize build, test, deploy, admin/content, and operational flows.

{headers[7]}
- TODO: Capture prompts/agent workflows/rules found in repo docs and configs.

{headers[8]}
- TODO: Add internal/external links with source-backed context.

### Hydration Source Artifacts
| Artifact (relative repo path) | Canonical URL | Type | Why hydrate this into note body |
|---|---|---|---|
| `TODO` | `TODO` | markdown | `TODO` |
| `TODO` | `TODO` | text | `TODO` |
| `TODO` | `TODO` | image | `TODO` |
| `TODO` | `Unknown` | pdf | `Set to Unknown if absent in repo` |

{headers[9]}
1. Home/Landing: [`./screenshots/01-home.png`](./screenshots/01-home.png) - TODO caption
2. Primary Workflow: [`./screenshots/02-primary-workflow.png`](./screenshots/02-primary-workflow.png) - TODO caption
3. Key Feature: [`./screenshots/03-key-feature.png`](./screenshots/03-key-feature.png) - TODO caption
4. Admin/Settings Equivalent: [`./screenshots/04-admin-or-settings.png`](./screenshots/04-admin-or-settings.png) - TODO caption

{headers[10]}
- TODO: Propose project supernode label + slug.
- TODO: List major nodes (repo, product, docs, workflows, prompts/chats).
- TODO: Define likely relationships/edges.

{headers[11]}
- TODO: List missing URLs/docs/screenshots and uncertain assumptions.

{headers[12]}
- [ ] Confirm dossier sections complete and source-backed
- [ ] Confirm screenshot files exist in `{screenshots_rel_dir}`
- [ ] Confirm screenshot links render from `{output_rel_path}`
- [ ] Confirm Unknowns are explicit (no fabricated details)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--repo-url", required=True)
    parser.add_argument("--live-url", action="append", dest="live_urls", required=True)
    parser.add_argument("--source-repo-path", required=True)
    parser.add_argument("--repo-root", required=True, help="Absolute path to repo root")
    parser.add_argument(
        "--output",
        default="docs/intake/ML-hyphenomenon-project-intake.md",
        help="Path relative to repo root",
    )
    parser.add_argument(
        "--screenshots-dir",
        default="docs/intake/screenshots",
        help="Path relative to repo root",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite output file if it exists")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    output = repo_root / args.output
    screenshots_dir = repo_root / args.screenshots_dir

    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output} (use --force)")

    screenshots_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    md = build_markdown(
        project_name=args.project_name,
        repo_url=args.repo_url,
        live_urls=args.live_urls,
        source_repo_path=args.source_repo_path,
        output_rel_path=args.output,
        screenshots_rel_dir=args.screenshots_dir,
    )
    output.write_text(md, encoding="utf-8")

    print(f"Created dossier scaffold: {output}")
    print(f"Ensured screenshot dir: {screenshots_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
