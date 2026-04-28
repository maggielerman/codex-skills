#!/usr/bin/env python3
"""Build the customer-facing docs-site catalog from suite and plugin metadata."""

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


def extract_use_cases(description: str) -> list[str]:
    marker = "Use when"
    if marker not in description:
        return []
    tail = description.split(marker, 1)[1].strip().rstrip(".")
    tail = re.sub(r"^a user asks to\s+", "", tail, flags=re.IGNORECASE)
    pieces = re.split(r",\s+|\s+or\s+", tail)
    return [piece.strip() for piece in pieces if piece.strip()][:5]


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
            f"Use {label} when this workflow matches the repository outcome you want.",
            "Bring it in after the target repo has a clear goal, a current branch, and enough context for Codex to act safely.",
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
            "Install or copy the skill folder into the Codex skills location used by your team.",
            "Open the target repo, read its local AGENTS.md or equivalent agent instructions, then invoke the skill by name.",
            "Give Codex the business goal, the repo constraints, and any files or routes that should stay untouched.",
            "Review generated scripts, docs, or code changes before committing them to your own workflow.",
        ],
        "troubleshooting": [
            "If Codex does not trigger the skill, invoke it explicitly with the skill name and a concrete target repo outcome.",
            "If generated docs feel repo-internal instead of customer-facing, restate the intended audience before rerunning the workflow.",
            "If a bundled script fails, run it from the target repo root and confirm any expected docs folders or credentials exist.",
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
            "Install the plugin from the delivered pack or repo-local plugin backup.",
            "Restart or refresh Codex so the plugin skills and interface metadata are visible.",
            "Invoke one of the suggested prompts, then point Codex at the target repo and desired outcome.",
        ],
        "troubleshooting": [
            "If the plugin does not appear, verify its .codex-plugin/plugin.json file is present and the plugin registry points to the folder.",
            "If a plugin skill cannot find its scripts, keep the plugin folder self-contained when copying it into your environment.",
            "If workflow output is too broad, rerun with the target repo path, desired deliverable, and any no-touch files listed explicitly.",
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
