#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "$0")/.." && pwd)"

if rg -q 'Default recommendation is option `B`' "$skill_dir/SKILL.md"; then
  echo "FAIL: the skill still infers option B"
  exit 1
fi

if ! rg -q 'No recommendation is inferred' "$skill_dir/SKILL.md"; then
  echo "FAIL: the skill does not explicitly forbid inferred recommendations"
  exit 1
fi

if ! rg -q 'clear the placeholder stroke' "$skill_dir/SKILL.md"; then
  echo "FAIL: the skill does not clear placeholder strokes after upload"
  exit 1
fi

python3 - "$skill_dir/templates/deck-data.example.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)

artwork = data["artworks"][0]
assert "recommended_front" not in artwork, "singular recommended_front is obsolete"
assert artwork.get("recommended_fronts") == ["A", "C"], (
    "Waters must preserve the approved A/C recommendations"
)
print("PASS: explicit multi-recommendation contract")
PY
