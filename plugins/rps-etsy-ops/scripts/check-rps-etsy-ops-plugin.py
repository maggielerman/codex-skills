#!/usr/bin/env python3
"""Validate the local RPS Etsy Ops plugin structure and registrations."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PLUGIN_NAME = "rps-etsy-ops"
REQUIRED_SKILLS = {
    "rps-wall-art-mockup-workflow",
    "rps-etsy-shop-uploader-listing-workflow",
    "rps-etsy-media-hosting-workflow",
    "rps-etsy-digital-product-packet-workflow",
}
def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_plugin(plugin_root: Path) -> None:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        fail(f"missing manifest: {manifest_path}")

    manifest = load_json(manifest_path)
    if manifest.get("name") != PLUGIN_NAME:
        fail("plugin manifest name mismatch")
    if manifest.get("skills") != "./skills/":
        fail("plugin manifest must point skills to ./skills/")
    placeholder = "[" + "TODO:"
    if placeholder in json.dumps(manifest):
        fail("plugin manifest still contains TODO placeholders")
    for unsupported in ("hooks", "mcpServers", "apps"):
        if unsupported in manifest:
            fail(f"manifest declares unused {unsupported}")

    for skill in REQUIRED_SKILLS:
        skill_path = plugin_root / "skills" / skill / "SKILL.md"
        if not skill_path.is_file():
            fail(f"missing required skill: {skill_path}")


def check_marketplace(marketplace_path: Path) -> None:
    marketplace = load_json(marketplace_path)
    entries = [p for p in marketplace.get("plugins", []) if p.get("name") == PLUGIN_NAME]
    if len(entries) != 1:
        fail(f"expected exactly one marketplace entry in {marketplace_path}, found {len(entries)}")
    entry = entries[0]
    if entry.get("source", {}).get("path") != f"./plugins/{PLUGIN_NAME}":
        fail(f"marketplace source path mismatch in {marketplace_path}")
    if entry.get("policy", {}).get("installation") != "INSTALLED_BY_DEFAULT":
        fail(f"marketplace install policy mismatch in {marketplace_path}")
    if entry.get("policy", {}).get("authentication") != "ON_INSTALL":
        fail(f"marketplace auth policy mismatch in {marketplace_path}")


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: check-rps-etsy-ops-plugin.py <plugin-root> <marketplace-json>",
            file=sys.stderr,
        )
        return 2

    check_plugin(Path(sys.argv[1]).resolve())
    check_marketplace(Path(sys.argv[2]).resolve())
    print("OK: RPS Etsy Ops plugin checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
