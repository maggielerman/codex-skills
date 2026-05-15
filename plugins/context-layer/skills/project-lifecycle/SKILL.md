---
name: project-lifecycle
description: Use when asked to create, open, inspect, or move Context Layer project docs across active, in-review, blocked, completed, backlog, or stale.
---

# Project Lifecycle

Use this skill for repo-native project state under `DOCS/PROJECTS/`.

## First Checks

1. Locate `DOCS/PROJECTS/`.
2. Read `DOCS/PROJECTS/README.md`.
3. Identify the project doc by number, title, filename, or current work context.

If the repo is not scaffolded, offer to run `$context-layer-scaffold`.

## Lifecycle Lanes

- `active/`: implementation in progress
- `in-review/`: implementation complete, waiting for walkthrough/sign-off
- `blocked/`: waiting on user decision, permission, access, manual input, or external dependency
- `completed/`: delivered after walkthrough/sign-off
- `backlog/`: queued
- `stale/`: paused or deprecated

## Transition Rules

- Move to `in-review/` only after end-to-end execution is done.
- Move to `blocked/` when progress requires Maggie or an external dependency.
- Move to `completed/` only after walkthrough/sign-off.
- Update frontmatter `status` to match the lifecycle folder.
- Add a timestamped checkpoint for every lifecycle move.
- Reference project numbers in roadmap/changelog entries when the transition matters outside the project doc.

## Parent And Child Projects

Use `projectType`, `parentProject`, and `programTrack` frontmatter to preserve hierarchy. Child projects may move independently through lifecycle lanes.
