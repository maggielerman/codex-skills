---
title: Projects Index & Numbering
description: How to create, name, and organize project planning documents
status: stable
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# Projects Directory

Use this directory to track project planning and status.

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
