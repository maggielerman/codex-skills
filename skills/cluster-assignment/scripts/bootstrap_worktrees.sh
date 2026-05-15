#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bootstrap_worktrees.sh --repo <repo_root> --worktrees <worktrees_root> --plan <csv_plan> [--remote <name>] [--push]

CSV format (simple comma-separated; no embedded commas):
  cluster,branch,base,worktree,push

Rules:
- branch: if blank, generated as codex/<slug(cluster)>
- base: defaults to main
- worktree: if blank, uses <slug(cluster)>; relative paths are resolved under --worktrees
- push: true/false (optional per-row override)

Example:
  bootstrap_worktrees.sh \
    --repo /Users/me/Github/my-repo \
    --worktrees /Users/me/Github/my-repo-worktrees \
    --plan ./references/cluster-plan.csv \
    --push
USAGE
}

trim() {
  local value="$*"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

to_lower() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

slugify() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g'
}

is_truthy() {
  case "$(to_lower "$1")" in
    1|true|yes|y) return 0 ;;
    *) return 1 ;;
  esac
}

REPO=""
WORKTREES=""
PLAN=""
REMOTE="origin"
PUSH_ALL="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --worktrees)
      WORKTREES="${2:-}"
      shift 2
      ;;
    --plan)
      PLAN="${2:-}"
      shift 2
      ;;
    --remote)
      REMOTE="${2:-}"
      shift 2
      ;;
    --push)
      PUSH_ALL="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$REPO" || -z "$WORKTREES" || -z "$PLAN" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

if [[ ! -d "$REPO/.git" ]]; then
  echo "Repo path is not a git repository: $REPO" >&2
  exit 1
fi

if [[ ! -f "$PLAN" ]]; then
  echo "Plan file not found: $PLAN" >&2
  exit 1
fi

mkdir -p "$WORKTREES"

line_no=0
while IFS=',' read -r raw_cluster raw_branch raw_base raw_worktree raw_push; do
  line_no=$((line_no + 1))

  raw_cluster="${raw_cluster%$'\r'}"
  raw_branch="${raw_branch%$'\r'}"
  raw_base="${raw_base%$'\r'}"
  raw_worktree="${raw_worktree%$'\r'}"
  raw_push="${raw_push%$'\r'}"

  cluster="$(trim "$raw_cluster")"
  branch="$(trim "$raw_branch")"
  base="$(trim "$raw_base")"
  wt_value="$(trim "$raw_worktree")"
  row_push="$(trim "$raw_push")"

  if [[ $line_no -eq 1 && "$(to_lower "$cluster")" == "cluster" ]]; then
    continue
  fi

  if [[ -z "$cluster" || "$cluster" == \#* ]]; then
    continue
  fi

  slug="$(slugify "$cluster")"
  if [[ -z "$slug" ]]; then
    echo "Line $line_no: unable to derive slug from cluster '$cluster'" >&2
    exit 1
  fi

  if [[ -z "$branch" ]]; then
    branch="codex/$slug"
  elif [[ "$branch" != codex/* ]]; then
    branch="codex/$branch"
  fi

  if [[ -z "$base" ]]; then
    base="main"
  fi

  if [[ -z "$wt_value" ]]; then
    wt_value="$slug"
  fi

  if [[ "$wt_value" = /* ]]; then
    wt_path="$wt_value"
  else
    wt_path="$WORKTREES/$wt_value"
  fi

  if ! git -C "$REPO" rev-parse --verify --quiet "$base" >/dev/null; then
    echo "Line $line_no: base ref not found: $base" >&2
    exit 1
  fi

  if [[ -e "$wt_path" ]]; then
    echo "Line $line_no: worktree path exists, skipping: $wt_path"
    continue
  fi

  if git -C "$REPO" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$REPO" worktree add "$wt_path" "$branch"
    echo "Attached existing branch $branch -> $wt_path"
  else
    git -C "$REPO" worktree add -b "$branch" "$wt_path" "$base"
    echo "Created branch $branch from $base -> $wt_path"
  fi

  push_this="false"
  if [[ "$PUSH_ALL" == "true" ]] || is_truthy "$row_push"; then
    push_this="true"
  fi

  if [[ "$push_this" == "true" ]]; then
    git -C "$wt_path" push -u "$REMOTE" "$branch"
    echo "Pushed $branch to $REMOTE"
  fi

done < "$PLAN"
