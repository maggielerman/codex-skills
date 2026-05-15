---
name: ux-ui-bug-intake
description: Use when asked to set up, use, triage, or maintain Context Layer UX/UI bug intake for user, agent, or subagent-detected UI defects.
---

# UX/UI Bug Intake

Use this skill for a lightweight docs-backed UX/UI bug register that complements project docs without becoming a heavyweight issue tracker.

## First Checks

1. Locate `DOCS/`.
2. Look for `DOCS/ux-ui-bugs/`.
3. Read `AGENTS.md` and the active project doc when present.

If `DOCS/` is missing, offer `$context-layer-scaffold`.

## Setup

Preferred folder:

- `DOCS/ux-ui-bugs/README.md`
- `DOCS/ux-ui-bugs/INBOX.md`
- `DOCS/ux-ui-bugs/TRIAGED.md`
- `DOCS/ux-ui-bugs/ARCHIVE.md`

Use lowercase folder naming to match Context Layer conventions. Keep the register lightweight and do not create one file per bug.

## Operating Model

- Users, main agents, and subagents may detect bugs.
- The main agent is the canonical logger/router.
- Subagents report concise bug candidates; the main agent de-duplicates and records canonical entries.

## Entry Fields

- `ID`
- `Reported`
- `Detected by`
- `Actor`
- `Surface`
- `Summary`
- `Severity`
- `Status`
- `Likely owner`
- `Related project`
- `Evidence path`
- `Superseded by migration?`
- `Notes`

## Statuses

- `new`
- `triaged`
- `scheduled`
- `in active slice`
- `fixed`
- `wont-fix`
- `superseded`

## Severities

- `blocker`
- `high`
- `medium`
- `low`

## Evidence

The bug register is an operating workflow, not the evidence store. Screenshots, recordings, audits, or reproduction packets should live under:

`DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`

Link evidence paths from the bug entry and the owning project doc when the bug affects project state or sign-off.
