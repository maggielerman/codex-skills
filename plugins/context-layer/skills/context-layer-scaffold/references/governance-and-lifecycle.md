# Governance And Lifecycle

## Governance Files

Create or update these repo-root files from `assets/templates/governance/`:

- `AGENTS.md`
- `ROADMAP.md`
- `CHANGELOG.md`

Also append docs-root links to existing agent instruction files when present:

- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `.cursor/rules/*`

## Lifecycle Lanes

Project docs move through:

- `active/` while implementation is in progress
- `in-review/` when implementation is complete and awaiting walkthrough/sign-off
- `blocked/` when work needs a decision, permission, access, manual input, or external dependency
- `completed/` only after walkthrough/sign-off
- `backlog/` for queued work
- `stale/` for paused or deprecated streams

While one stream is `in-review` or `blocked`, agents may continue autonomous work from `backlog/` or `stale/` when appropriate.

## Checkpoint Model

Use checkpoint-based updates instead of `today/tomorrow` sections.

Each checkpoint should include:

- absolute timestamp from `node scripts/docs/timestamp-et.mjs --json`
- completed since prior checkpoint
- next checkpoint targets
- risks, questions, evidence paths, or `MAGGIE TODO:` items when relevant

## Visual Design Gate

For significant user-facing UI, redesign, restyle, dashboard, app, website, form, screenshot-route, or visual QA work, require a `$visual-design-critique` checkpoint before implementation sign-off or movement to `in-review/`.

Record the verdict, evidence paths, must-fix issues, approved deviations, and follow-up verification in the owning project doc.
