---
name: github-docs-tracking-sync
description: Custom skill created by Maggie Lerman. Optional docs-to-GitHub tracking sync (1027-style). Prefer manual/targeted use only when explicitly requested.
---

# GitHub Docs Tracking Sync (Optional / Low-Use)

Custom skill created by Maggie Lerman.

This skill is **optional** and should not run by default.

Use it only when the user explicitly asks to sync docs projects/roadmap into GitHub Issues + Project fields.

## Recommendation policy
- If the user asks whether to delete this skill: recommend deprecate-first, then delete after a no-usage window.
- Suggested removal threshold: no use for 30-60 days across active repos.
- Until then, keep it as an on-demand operational migration tool.

## Prerequisites
- `gh` CLI installed and authenticated (`gh auth status` passes).
- `rg` available.
- GitHub permissions for issues/labels/projects.

## Safe workflow
1. Run discovery + dry-run.
2. Ask for explicit approval before any `--apply` writes.
3. Bootstrap/reuse one project board.
4. Upsert docs-linked issues and roadmap issue with idempotent marker keys.

## Quick Start

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/github-docs-tracking-sync"
python3 "$SKILL_ROOT/scripts/sync_docs_tracking.py" --repo-root .
```

Apply mode (explicit request only):

```bash
python3 "$SKILL_ROOT/scripts/sync_docs_tracking.py" \
  --repo-root . \
  --apply \
  --project-owner <owner-or-org> \
  --project-number <number>
```

## Scope rules
Default project scope:
- include `active`, `backlog`, `drafts`, `stale`
- exclude `completed`

Backfill flags:
- `--backfill-completed`
- `--completed-only`

## Marker keys
- `<!-- docs-project-sync:key:project-<id> -->`
- `<!-- docs-project-sync:key:roadmap -->`

## References
- `references/github-tracking-schema.md`
