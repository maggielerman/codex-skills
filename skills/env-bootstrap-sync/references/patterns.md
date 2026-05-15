# Env Bootstrap Patterns

Use this file when implementing the repo-specific version of the skill.

## Recommended File Responsibilities

- `.env`
  - local live values
  - gitignored
- `.env.example`
  - tracked schema only
- repo config such as `.env-manager.json`
  - managed files
  - root resolution strategy
  - bootstrap runbooks
  - verification commands

## Suggested Commands

- `env:status`
  - compare active worktree vs canonical checkout
- `env:sync`
  - copy configured files to the canonical target
- `env:bootstrap`
  - print or summarize the tracked bootstrap contract

## Suggested Root Strategies

- current worktree <-> main checkout via `git worktree list`
- current checkout <-> named sibling checkout
- repo-only status mode when no worktree sync is needed

## Suggested Runbook Sections

1. Source of truth
2. Managed files
3. Secret-file layout
4. New-machine bootstrap
5. Verification commands
6. Maintenance rules

## Migration Checklist

1. Inventory current env files, docs, and secret locations.
2. Decide which files should sync.
3. Add tracked config for the sync/bootstrap contract.
4. Add package commands.
5. Update `.env.example`.
6. Create or update the environment runbook.
7. Update README and docs indexes.
8. Run env status/sync plus docs checks.
