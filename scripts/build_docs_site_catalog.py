#!/usr/bin/env python3
"""Build the public docs-site catalog from suite and plugin metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "skills" / "manifest.json"
PLUGINS_DIR = REPO_ROOT / "plugins"
OUTPUT_PATH = REPO_ROOT / "docs-site" / "src" / "lib" / "catalog.generated.ts"

CATEGORY_KEYWORDS = [
    ("Storefront and commerce", ("shopify", "catalog", "merchant", "ecommerce")),
    ("Delivery governance", ("tranche", "governance", "walkthrough", "signoff", "continue", "project")),
    ("Documentation systems", ("docs", "documentation", "evidence", "dashboard", "product")),
    ("Repository setup", ("env", "bootstrap", "handoff", "claude", "github")),
    ("Research and review", ("audit", "review", "journey", "cluster")),
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def first_sentence(text: str) -> str:
    match = re.match(r"(.+?[.!?])(?:\s|$)", text.strip())
    return match.group(1) if match else text.strip()


def clean_use_case(piece: str) -> str:
    piece = piece.strip().strip(".;")
    piece = re.sub(r"^(a user asks to|asked to|asks to|wants to|wants)\s+", "", piece, flags=re.IGNORECASE)
    piece = re.sub(r"^(and|or)\s+", "", piece, flags=re.IGNORECASE)
    piece = piece.replace("repo-native", "repo-native")
    if not piece:
        return ""
    return piece[0].upper() + piece[1:]


def extract_use_cases(description: str) -> list[str]:
    marker = "Use when"
    if marker not in description:
        return []
    tail = description.split(marker, 1)[1].strip().rstrip(".")
    pieces = re.split(r",\s+|\s+or\s+", tail)
    cleaned = [clean_use_case(piece) for piece in pieces]
    return [piece for piece in cleaned if piece][:5]


def category_for(text: str) -> str:
    haystack = text.lower()
    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "Agent workflow accelerators"


def resource_labels(skill: dict) -> list[str]:
    labels: list[str] = []
    if skill.get("has_scripts"):
        labels.append("bundled scripts")
    if skill.get("has_references"):
        labels.append("reference guides")
    if skill.get("has_assets"):
        labels.append("starter assets")
    if skill.get("has_agents_metadata"):
        labels.append("agent metadata")
    return labels or ["portable skill instructions"]


def skill_doc(skill: dict) -> dict:
    label = skill.get("display_name") or skill.get("name") or skill["folder"]
    description = skill.get("description") or ""
    summary = skill.get("short_description") or first_sentence(description)
    use_cases = extract_use_cases(description)
    if not use_cases:
        use_cases = [
            f"Run {label} when its workflow matches the repo outcome you need.",
            "Use it after the target repo has enough context for Codex to act safely.",
        ]
    resources = resource_labels(skill)
    return {
        "slug": slugify(skill["folder"]),
        "kind": "skill",
        "title": label,
        "folder": skill["folder"],
        "status": skill.get("status", "active"),
        "summary": summary,
        "description": description,
        "category": category_for(f"{label} {description}"),
        "path": skill.get("path"),
        "resources": resources,
        "useCases": use_cases,
        "gettingStarted": [
            "Copy or install the complete skill folder so scripts, references, assets, and metadata stay together.",
            "Open the target repo and read its local agent instructions before invoking the skill.",
            "Name the outcome you want, the repo constraints, and any files or routes Codex should avoid.",
            "Review generated scripts, docs, or code before adopting the result into your workflow.",
        ],
        "troubleshooting": [
            "If Codex does not trigger the skill, invoke it by name and include the target repo outcome.",
            "If the output has the wrong audience, explicitly say whether the deliverable is public, personal, team-facing, or repo-internal.",
            "If a bundled script fails, run it from the target repo root and confirm the full skill folder was copied intact.",
        ],
    }


def plugin_doc(plugin_json: Path) -> dict:
    data = json.loads(plugin_json.read_text(encoding="utf-8"))
    interface = data.get("interface", {})
    name = data.get("name", plugin_json.parent.parent.name)
    title = interface.get("displayName") or name.replace("-", " ").title()
    description = interface.get("longDescription") or data.get("description") or ""
    prompts = interface.get("defaultPrompt") or []
    capabilities = interface.get("capabilities") or []
    return {
        "slug": slugify(name),
        "kind": "plugin",
        "title": title,
        "folder": name,
        "status": "available",
        "summary": interface.get("shortDescription") or first_sentence(description),
        "description": description,
        "category": interface.get("category") or category_for(f"{title} {description}"),
        "path": str(plugin_json.parent.parent.relative_to(REPO_ROOT)),
        "resources": [f"{capability} capability" for capability in capabilities] or ["plugin package"],
        "useCases": prompts[:5] or [data.get("description", "Use this plugin when its workflow matches your target repo.")],
        "gettingStarted": [
            "Install the complete plugin folder from the public repo or local checkout.",
            "Refresh Codex so plugin skills, metadata, assets, and default prompts are visible.",
            "Start from one suggested prompt, then add the target repo path and desired deliverable.",
        ],
        "troubleshooting": [
            "If the plugin does not appear, confirm .codex-plugin/plugin.json is present and the plugin registry points to the folder.",
            "If a plugin skill cannot find scripts or assets, the plugin folder was likely flattened or partially copied.",
            "If the workflow is too broad, rerun with a narrower deliverable and explicit no-touch files.",
        ],
    }


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    skills = [skill_doc(skill) for skill in manifest.get("skills", [])]
    plugins = [plugin_doc(path) for path in sorted(PLUGINS_DIR.glob("*/.codex-plugin/plugin.json"))]
    payload = {
        "generatedBy": "scripts/build_docs_site_catalog.py",
        "skillCount": len(skills),
        "pluginCount": len(plugins),
        "items": skills + plugins,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        "// This file is generated by scripts/build_docs_site_catalog.py. Do not hand-edit.\n"
        "import type { CatalogItem } from './catalog-types';\n\n"
        f"export const catalog = {json.dumps(payload, indent=2)} as const satisfies {{\n"
        "  generatedBy: string;\n"
        "  skillCount: number;\n"
        "  pluginCount: number;\n"
        "  items: readonly CatalogItem[];\n"
        "};\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
