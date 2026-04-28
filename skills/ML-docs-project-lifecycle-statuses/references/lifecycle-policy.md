# Lifecycle Policy Reference

Use this policy when a repo already has ML-docs-system-scaffold governance and project tracking under `docs/PROJECTS/` or `DOCS/PROJECTS/`.
Use this skill only for repositories scaffolded before `ML-docs-system-scaffold` included `in-review` and `blocked` by default.

Path-resolution requirement: resolve folder and file names case-insensitively (for example `docs` vs `DOCS`, `projects` vs `PROJECTS`, `readme.md` vs `README.md`) and preserve the repo's actual casing when writing paths into docs.

## Status Folder Model

Required folders:
- `active/` - in progress
- `in-review/` - implementation complete, waiting for user walkthrough/sign-off
- `blocked/` - paused for user decision/permission/input/access
- `completed/` - delivered and reviewed
- `backlog/` - queued
- `stale/` - paused or deprecated

## Transition Rules

1. `backlog -> active`
- Start implementation and keep checkpoint cadence.

2. `active -> in-review`
- Move only when implementation and verification are done end to end.
- Set frontmatter `status: in-review`.
- Add checkpoint summary of completed work and review agenda.

3. `active|in-review -> blocked`
- Move when progress requires user input or permissions.
- Set frontmatter `status: blocked`.
- Add checkpoint with exact blocker and required unblock action.

4. `in-review -> completed`
- Move only after user walkthrough/collaborative sign-off.
- Set frontmatter `status: completed`.

5. `blocked -> active|in-review`
- Resume after unblock.
- Add checkpoint documenting unblock decision and immediate next target.

## Checkpoint Requirements (Unchanged)

Every checkpoint entry should include:
- absolute timestamp (`YYYY-MM-DD HH:MM ET (America/New_York)`)
- completed since prior checkpoint
- next checkpoint targets

Always generate timestamps using `node scripts/docs/timestamp-et.mjs --json`.

## Instruction Surfaces To Keep Synced

Required:
- `AGENTS.md`
- docs root index files (`<docs_root>/README.md`, `<docs_root>/index.md`)
- `<docs_root>/PROJECTS/README.md`

Optional if present:
- `README.md`
- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `.cursor/rules/*`
- root-level LLM instruction docs (`llms*.txt|md`)
