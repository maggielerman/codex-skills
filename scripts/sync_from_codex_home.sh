#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="${CODEX_HOME:-$HOME/.codex}/skills"
target_root="$repo_root/skills"
suite_list="$target_root/SUITE_SKILLS.txt"
include_system="${1:-}"

if [[ ! -d "$source_root" ]]; then
  echo "Source skills directory not found: $source_root" >&2
  exit 1
fi

mkdir -p "$target_root"

if [[ "$include_system" == "--include-system" ]]; then
  rsync -a "$source_root"/ "$target_root"/
else
  if [[ ! -f "$suite_list" ]]; then
    echo "Missing suite list: $suite_list" >&2
    exit 1
  fi

  while IFS= read -r skill_name; do
    [[ -z "$skill_name" || "$skill_name" =~ ^# ]] && continue
    if [[ ! -d "$source_root/$skill_name" ]]; then
      echo "Missing source skill: $source_root/$skill_name" >&2
      exit 1
    fi
    rsync -a "$source_root/$skill_name" "$target_root"/
  done < "$suite_list"

  find "$target_root" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 | while IFS= read -r -d '' dir; do
    skill_name="$(basename "$dir")"
    if ! grep -qx "$skill_name" "$suite_list"; then
      rm -rf "$dir"
    fi
  done
fi

echo "Synced skills from $source_root to $target_root"
