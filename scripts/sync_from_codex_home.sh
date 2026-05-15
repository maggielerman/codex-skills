#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="${CODEX_HOME:-$HOME/.codex}/skills"
agents_source_root="${AGENTS_HOME:-$HOME/.agents}/skills"
target_root="$repo_root/skills"
suite_list="$target_root/SUITE_SKILLS.txt"
check_only=false
include_system=false
prune_stale=false

usage() {
  cat <<'EOF'
Usage: scripts/sync_from_codex_home.sh [--check] [--prune-stale] [--include-system]

Sync allowlisted skills from ${CODEX_HOME:-$HOME/.codex}/skills and
${AGENTS_HOME:-$HOME/.agents}/skills into this repo.

Options:
  --check          Report curated suite source/repo drift without writing files.
  --prune-stale   Delete stale files inside synced curated suite skill folders.
  --include-system
                   Mirror the full source skills directory, including hidden/system skills.
EOF
}

while (($#)); do
  case "$1" in
    --check)
      check_only=true
      ;;
    --include-system)
      include_system=true
      ;;
    --prune-stale)
      prune_stale=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ "$check_only" == true && "$prune_stale" == true ]]; then
  echo "--check cannot be combined with --prune-stale because --check never writes files." >&2
  exit 2
fi

if [[ "$include_system" == true && "$check_only" == true ]]; then
  echo "--include-system cannot be combined with --check; check mode validates the curated suite only." >&2
  exit 2
fi

if [[ "$include_system" == true && "$prune_stale" == true ]]; then
  echo "--include-system cannot be combined with --prune-stale because full-mirror pruning would delete suite control files." >&2
  exit 2
fi

if [[ ! -d "$source_root" ]]; then
  echo "Source skills directory not found: $source_root" >&2
  exit 1
fi

source_roots=("$source_root")
if [[ -d "$agents_source_root" && "$agents_source_root" != "$source_root" ]]; then
  source_roots+=("$agents_source_root")
fi

mkdir -p "$target_root"

if [[ "$include_system" == true ]]; then
  rsync -a "$source_root"/ "$target_root"/
else
  if [[ ! -f "$suite_list" ]]; then
    echo "Missing suite list: $suite_list" >&2
    exit 1
  fi

  suite_skills=()
  while IFS= read -r skill_name; do
    [[ -z "$skill_name" || "$skill_name" =~ ^# ]] && continue
    suite_skills+=("$skill_name")
  done < "$suite_list"

  in_suite() {
    local candidate="$1"
    local listed_skill
    for listed_skill in "${suite_skills[@]}"; do
      if [[ "$listed_skill" == "$candidate" ]]; then
        return 0
      fi
    done
    return 1
  }

  skill_source_dir() {
    local candidate="$1"
    local root
    for root in "${source_roots[@]}"; do
      if [[ -f "$root/$candidate/SKILL.md" ]]; then
        printf '%s\n' "$root/$candidate"
        return 0
      fi
    done
    return 1
  }

  missing_sources=()
  local_only=()
  stale_files=()
  source_only_files=()
  changed_files=()

  for skill_name in "${suite_skills[@]}"; do
    source_dir="$(skill_source_dir "$skill_name" || true)"
    if [[ -z "$source_dir" ]]; then
      missing_sources+=("$skill_name")
      continue
    fi

    if [[ -d "$target_root/$skill_name" ]]; then
      while IFS= read -r -d '' target_file; do
        relative_path="${target_file#"$target_root/$skill_name/"}"
        if [[ ! -f "$source_dir/$relative_path" ]]; then
          stale_files+=("$skill_name/$relative_path")
        fi
      done < <(find "$target_root/$skill_name" -type f ! -name '.DS_Store' ! -path '*/__pycache__/*' -print0)
    fi

    while IFS= read -r -d '' source_file; do
      relative_path="${source_file#"$source_dir/"}"
      target_file="$target_root/$skill_name/$relative_path"
      if [[ ! -f "$target_file" ]]; then
        source_only_files+=("$skill_name/$relative_path")
      elif ! cmp -s "$source_file" "$target_file"; then
        changed_files+=("$skill_name/$relative_path")
      fi
    done < <(find "$source_dir" -type f ! -name '.DS_Store' ! -path '*/__pycache__/*' -print0)
  done

  for root in "${source_roots[@]}"; do
    while IFS= read -r -d '' source_dir; do
      skill_name="$(basename "$source_dir")"
      if [[ -f "$source_dir/SKILL.md" ]] && ! in_suite "$skill_name"; then
        local_only+=("$skill_name")
      fi
    done < <(find "$root" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 | sort -z)
  done

  failed=false
  if ((${#missing_sources[@]})); then
    failed=true
    echo "Missing allowlisted source skills:" >&2
    printf -- "- %s\n" "${missing_sources[@]}" >&2
  fi

  if ((${#stale_files[@]})) && [[ "$prune_stale" != true ]]; then
    failed=true
    echo "Stale repo-only files detected:" >&2
    printf -- "- %s\n" "${stale_files[@]}" >&2
    echo "Run with --prune-stale to delete these files during sync." >&2
  fi

  if [[ "$check_only" == true ]]; then
    if ((${#source_only_files[@]})); then
      failed=true
      echo "Source-only skill files detected:" >&2
      printf -- "- %s\n" "${source_only_files[@]}" >&2
    fi

    if ((${#changed_files[@]})); then
      failed=true
      echo "Changed skill files detected:" >&2
      printf -- "- %s\n" "${changed_files[@]}" >&2
    fi
  fi

  if ((${#local_only[@]})); then
    echo "Local source skills not listed in suite:" >&2
    printf '%s\n' "${local_only[@]}" | sort -u | sed 's/^/- /' >&2
  fi

  if [[ "$failed" == true ]]; then
    echo "Sync preflight failed; no files were copied." >&2
    exit 1
  fi

  if [[ "$check_only" == true ]]; then
    echo "Sync preflight passed; no files were copied."
    exit 0
  fi

  while IFS= read -r skill_name; do
    [[ -z "$skill_name" || "$skill_name" =~ ^# ]] && continue
    source_dir="$(skill_source_dir "$skill_name" || true)"
    if [[ -z "$source_dir" ]]; then
      echo "Missing source skill: $skill_name" >&2
      exit 1
    fi
    mkdir -p "$target_root/$skill_name"
    rsync_args=(-a --exclude='.DS_Store' --exclude='__pycache__/')
    if [[ "$prune_stale" == true ]]; then
      rsync_args+=(--delete)
    fi
    rsync "${rsync_args[@]}" "$source_dir"/ "$target_root/$skill_name"/
  done < "$suite_list"

  find "$target_root" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 | while IFS= read -r -d '' dir; do
    skill_name="$(basename "$dir")"
    if ! grep -qx "$skill_name" "$suite_list"; then
      rm -rf "$dir"
    fi
  done
fi

echo "Synced skills from ${source_roots[*]} to $target_root"
