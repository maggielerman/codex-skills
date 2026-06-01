---
name: env-bootstrap-sync
description: Custom skill created by Maggie Lerman. Create or upgrade a repo-owned environment bootstrap workflow with reproducible `.env` handling, worktree sync, required-variable documentation, secret-file layout, and new-machine runbooks. Use when a repo has drifting `.env` files, unclear setup requirements, worktree-specific config loss, or scattered credential/bootstrap instructions.
---

# Env Bootstrap Sync

Custom skill created by Maggie Lerman.

Use this skill when a repo needs a durable environment-management pattern instead of ad hoc local setup.

Typical triggers:

- “keep `.env` files in sync across worktrees”
- “make this setup reproducible on another machine”
- “document all required env vars and credential locations”
- “turn this repo-specific env helper into a reusable pattern”
- “we can’t commit `.env`, so how do we keep track of everything?”

## Outcome

The target model should make these boundaries explicit:

- `.env`
  - local live values
  - gitignored
- `.env.example`
  - tracked variable schema
- repo-owned env config
  - tracked sync/bootstrap behavior
- external secret-file storage
  - raw credential files outside the repo
- tracked runbooks
  - setup, sync, and verification instructions

## Workflow

### 1. Discover the current setup

Before editing, inspect:

- `.env.example`
- existing env-sync scripts or package commands
- README and docs runbooks
- whether the repo uses `git worktree`
- where secrets currently live

Questions to answer:

- Is there already a narrow helper that should be generalized instead of replaced?
- Which files need to stay synchronized?
- Which docs currently mention env/bootstrap requirements?
- Which paths are truly local-only and should never be tracked?

### 2. Define the repo contract

Implement one tracked contract for the repo:

- config file for env sync/bootstrap behavior
- package commands for:
  - status
  - sync
  - bootstrap summary

Prefer a config-driven tool over hard-coded repo logic.

If the repo already has a command users know, keep a compatibility alias when practical.

### 3. Document the source of truth

Create or update one repo-owned runbook that explains:

- what belongs in `.env`
- what belongs in `.env.example`
- where secret files should live
- how worktree sync works
- how a new machine should be bootstrapped
- how to verify the setup after bootstrap

Also update:

- main `README.md`
- docs index pages
- subsystem runbooks that depend on the env vars

### 4. Normalize required-variable tracking

When new variables are introduced:

- add them to `.env.example`
- describe them in the main README or the relevant runbook
- keep local values only in `.env`

Do not put real secrets in tracked files.

### 5. Keep secret files out of the repo

Prefer a stable machine-level directory outside the repo, for example:

- `~/.config/<project>/...`

The runbook should explain:

- file purpose
- expected local path pattern
- which env var points at each file
- how to restore them from secure storage on a new machine

### 6. Verify the workflow end to end

Minimum validation:

- env status command reports current drift or sync state
- env sync command copies the intended files
- docs checks still pass
- runbook references are valid

If the repo has subsystem verification commands, include them in the bootstrap workflow.

## Implementation Rules

- Generalize existing working behavior rather than discarding it.
- Keep the skill repo-agnostic: move repo-specific decisions into config and docs.
- Prefer a small CLI plus tracked config over embedding logic in documentation only.
- Keep the runbook concise and operator-facing.
- Avoid inventing a second source of truth outside the repo docs.

## Suggested Deliverables

- tracked env-manager config such as `.env-manager.json`
- repo helper script such as `scripts/env/env-manager.mjs`
- package commands:
  - `env:status`
  - `env:sync`
  - `env:bootstrap`
- compatibility alias if needed
- dedicated environment/bootstrap runbook
- README and docs-index links

## References

When designing the repo pattern, read:

- [references/patterns.md](references/patterns.md)

Load it when you need example config structure, folder layout guidance, or a migration checklist.
