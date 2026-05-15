---
name: maggie-todo
description: Use when asked about MAGGIE TODOs, Maggie-owned follow-ups, blocked-on-Maggie items, manual approvals, or clearing resolved Maggie TODOs.
---

# MAGGIE TODO

`MAGGIE TODO:` is a literal callout for Maggie-owned manual work, approvals, evidence gathering, manual testing, external dependencies, access, credentials, or missing decisions.

## First Checks

1. Locate `DOCS/`.
2. Read `DOCS/PROJECTS/README.md` if present.
3. Search project docs for `MAGGIE TODO:`.

If `DOCS/` is missing, tell the user the repo does not appear scaffolded and offer to run `$context-layer-scaffold`.

## Workflow

Use this skill to:

- add new `MAGGIE TODO:` callouts to the relevant project doc
- keep unresolved items in a dedicated `## MAGGIE TODO` section
- de-duplicate repeated callouts
- mark work blocked when unresolved Maggie-owned items gate progress
- remove or archive resolved callouts only when the user confirms they are resolved
- regenerate the project dashboard when available

## Rules

- Use one unresolved item per line.
- Preserve exact wording if the user provides it.
- If an item blocks progress, move the owning project to `DOCS/PROJECTS/blocked/` and set `status: blocked`.
- If an item is informational but not blocking, leave the project in its current lifecycle lane and record the dependency in the checkpoint log.
