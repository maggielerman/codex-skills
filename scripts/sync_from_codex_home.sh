#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="${CODEX_HOME:-$HOME/.codex}/skills"
target_root="$repo_root/skills"
include_system="${1:-}"

if [[ ! -d "$source_root" ]]; then
  echo "Source skills directory not found: $source_root" >&2
  exit 1
fi

mkdir -p "$target_root"

if [[ "$include_system" == "--include-system" ]]; then
  rsync -a "$source_root"/ "$target_root"/
else
  find "$source_root" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 \
    | xargs -0 -I{} rsync -a "{}" "$target_root"/
fi

echo "Synced skills from $source_root to $target_root"
