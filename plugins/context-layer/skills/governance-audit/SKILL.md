---
name: governance-audit
description: "Use when asked to audit Context Layer governance: blockers, dependencies, roadmap order, checkpoints, lifecycle drift, parent/child consistency, dashboard/evidence gaps."
---

# Governance Audit

Audit non-completed Context Layer project streams and roadmap sequencing with file-backed evidence.

## First Checks

1. Locate `DOCS/`, `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md`.
2. Confirm `DOCS/PROJECTS/` exists with lifecycle folders.
3. Read `DOCS/project-master.md` when present.
4. Include all lifecycle folders except `completed/` unless the user asks for completed streams too.

If `DOCS/PROJECTS/` is missing, tell the user the repo does not appear to have Context Layer installed and offer `$context-layer-scaffold`.

## Audit Register

For each in-scope project capture:

- id and title
- lifecycle folder and frontmatter `status`
- `projectType`, `parentProject`, and `programTrack`
- explicit blockers, dependencies, gates, risks, and open questions
- latest checkpoint timestamp
- next checkpoint targets
- evidence paths and missing evidence references
- dashboard/status drift when visible

## Checks

- Flag missing absolute ET timestamps or relative time phrasing.
- Flag missing completed-since-prior-checkpoint or next-checkpoint targets.
- Flag folder/frontmatter status drift.
- Flag orphaned child projects and unclear parent rollups.
- Flag roadmap order that contradicts dependencies or blockers.
- Flag stale `AGENTS.md`, `ROADMAP.md`, or `CHANGELOG.md` references.
- Flag work marked ready without evidence, sign-off, or unresolved `MAGGIE TODO:` handling.

## Output Contract

Return sections in this order:

1. `Critical Blockers`
2. `Conflicts And Drift`
3. `Roadmap Order Recommendations`
4. `Amendments To Apply`
5. `Next Checkpoint Plan`

For each finding include severity, file-backed evidence, impact, and one concrete corrective action.

When the audit produces a durable report, store it under:

`DOCS/evidence/active/context-layer-audits/<run-name>/`
