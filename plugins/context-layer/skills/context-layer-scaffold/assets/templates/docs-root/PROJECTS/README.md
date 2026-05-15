---
title: Projects Index & Numbering
description: How to create, name, and organize project planning documents
status: stable
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# Projects Directory

Use this directory to track project planning and status.

- Template:
  - `NNNN_project_template.md` - reusable project template; copy this into a lifecycle folder for real work
- Subfolders:
  - `active/` – in progress
  - `in-review/` – implementation complete, waiting for walkthrough/sign-off
  - `blocked/` – waiting for user decisions/permissions/input
  - `completed/` – delivered
  - `backlog/` – queued
  - `stale/` – paused or deprecated

## Numbering Scheme

- Every project gets a unique 4+ digit number prefix.
- Filenames must start with the number, then an underscore, then a short slug.
  - Example: `1001_feature_plan.md`
- Reference the number in roadmap entries and changelog notes.
- Parent and child projects both use independent numeric prefixes.
- Represent hierarchy with frontmatter fields such as `parentProject`, `programTrack`, and `projectType`, not nested lifecycle folders.

## Parent And Child Projects

- Use `projectType: parent` for broad programs with multiple independently trackable streams.
- Use `projectType: child` when work has separate scope, lifecycle state, evidence, owner, risk, or review path.
- Set `parentProject` on child projects to the parent project id or filename stem.
- Set `programTrack` when related work should roll up in the dashboard even without a direct parent.
- Child projects move through lifecycle folders independently.
- Store durable supporting artifacts under `{{DOCS_ROOT}}/evidence/{active|archive}/<project-id>/`, not inside lifecycle folders.

## Capitalization Standard

- Use `DOCS/` as the canonical docs root for all new and retrofitted scaffolds.
- Keep `PROJECTS/` uppercase as the reserved planning-system root.
- Keep lifecycle folders lowercase: `active/`, `in-review/`, `blocked/`, `completed/`, `backlog/`, `stale/`.
- Keep repo-level governance and entrypoint docs uppercase: `README.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Keep content pages lowercase unless they are reserved entrypoints. Examples: `index.md`, `checkpoint-workflow.md`, `1001_feature_plan.md`.

## Checkpoint Standard

Use checkpoint logs for progress reporting in project docs.

- Do not use `today/tomorrow` handoff sections.
- Add a new checkpoint entry for each major implementation step, decision, or scope update.
- Generate timestamps with `node scripts/docs/timestamp-et.mjs --json` (never hand-type them).
- Every checkpoint entry should include:
  - absolute timestamp (`YYYY-MM-DD HH:MM ET (America/New_York)`)
  - completed since prior checkpoint
  - next checkpoint targets

## Lifecycle Transition Rules

1. Start implementation in `active/` with `status: active`.
2. Move to `in-review/` with `status: in-review` after end-to-end execution is done and before walkthrough/sign-off.
3. Move to `blocked/` with `status: blocked` when progress requires user decisions, permissions, access, or inputs.
4. Move to `completed/` only after walkthrough/sign-off.
5. Continue autonomous execution from backlog/stale while projects are in `in-review/` or `blocked`.

## Visual/UX Quality Gate

- For significant user-facing UI work, run `$visual-design-critique` before moving to `in-review/`.
- Record the critique verdict, evidence paths, must-fix issues, approved deviations, and follow-up verification in the owning project doc.
- Use `{{DOCS_ROOT}}/development/visual-design-quality-gate.md` as the repo-local standard.

## Dashboard

- `dashboard.html` is generated output and should be regenerated from project docs.
- The markdown project docs remain the source of truth.
- The dashboard surfaces lifecycle lanes, parent/child grouping, status drift, and unresolved `MAGGIE TODO:` items.

## MAGGIE TODO Standard

- Whenever work depends on Maggie's manual input, evidence gathering, manual testing, approval, or an external workstream, add a literal `MAGGIE TODO:` callout in the project doc.
- Prefer bullet lines such as `- MAGGIE TODO: Confirm production credentials for final verification.`
- Keep unresolved items together in a dedicated `## MAGGIE TODO` section.
- If those items block progress, move the project doc to `blocked/`.
