---
name: ux-ui-bug-intake
author: Maggie Lerman
description: Set up a lightweight UX/UI bug intake system with lifecycle docs, routing rules, and routines. Use when starting a new project stream, standardizing repo operations, or replacing ad hoc bug tracking with a simple docs-backed workflow.
---

# UX/UI Bug Intake

## Overview

Use this skill when a repository needs a lightweight, docs-backed UX/UI bug intake system that works during active implementation without turning into a heavyweight issue tracker.

This skill helps Codex:

- scaffold a dedicated UX/UI bug lifecycle folder
- define the intake schema, severity/status vocabulary, and routing defaults
- document the user/main-agent/subagent operating model
- wire the bug system into the repo's governance docs so it becomes part of normal execution

## When To Use

Use this skill when the user asks to:

- create a UX/UI bug inbox or bug tracking system
- standardize how design and workflow bugs are captured
- make bug intake part of project startup or docs scaffolding
- set up a lightweight alternative to GitHub issues for UI/UX defects
- add routines so user-, agent-, and subagent-detected bugs do not get lost in chat

Do not use this skill for:

- backend-only bug tracking
- test-harness-only defect management
- a full issue-management migration to GitHub/Jira/Linear
- per-bug longform investigation docs

## Workflow

### 1. Audit The Repo's Existing Docs Shape

Before creating anything:

- check whether the repo uses `DOCS/` or `docs/`
- check whether current governance lives in files like `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, `DOCS/README.md`, or equivalents
- look for any existing bug capture files so you can preserve or link them instead of silently replacing them

If the repo already has a lightweight bug intake system, prefer standardizing or extending it rather than creating a competing structure.

### 2. Scaffold The Lifecycle Folder

Preferred structure:

- `DOCS/UX_UI_BUGS/README.md`
- `DOCS/UX_UI_BUGS/INBOX.md`
- `DOCS/UX_UI_BUGS/TRIAGED.md`
- `DOCS/UX_UI_BUGS/ARCHIVE.md`

If the repo uses `docs/`, adapt the casing accordingly.

Use the helper script when it fits:

```bash
python3 /Users/maggielerman/.codex/skills/ux-ui-bug-intake/scripts/setup_bug_intake.py --root /path/to/repo
```

The script will:

- detect `DOCS/` or `docs/`
- create the `UX_UI_BUGS/` folder if needed
- scaffold the four lifecycle docs with generic starter content

After running it, adjust wording and timestamps to match repo conventions.

### 3. Establish The Operating Model

The default model should be:

- user detects bugs
- main agent detects bugs
- subagents detect bugs
- main agent is the canonical logger/router

This keeps detection broad while avoiding duplicate or conflicting bug records.

### 4. Define The Schema And Vocabulary

Every repo should define:

- entry fields
- severity vocabulary
- status vocabulary
- fix-now vs defer rules
- owner-routing defaults

Use the reference docs in `references/` as the default baseline, then adapt naming to the repo's project system.

### 5. Wire Governance Notes

The lifecycle folder is not enough on its own. Update the repo's current operating docs so the bug system becomes part of normal execution.

Typical files to update:

- `AGENTS.md`
- `ROADMAP.md`
- docs index / docs README
- current-state or status summary doc
- changelog

The goal is to make bug capture part of the repo's operating system, not just a hidden folder.

### 6. Keep It Lightweight

Bias toward:

- one lifecycle folder
- short normalized entries
- tranche-boundary review and clustering

Avoid:

- one file per bug
- heavyweight review states unless the repo truly needs them
- splitting intake across multiple competing sources of truth

## Recommended Defaults

### Lifecycle Roles

- `INBOX.md`
  - fast capture
  - append-first
  - low-friction notes
- `TRIAGED.md`
  - curated working queue
  - normalized entries
  - owner-routing and decision state
- `ARCHIVE.md`
  - fixed, superseded, or rejected items
- `README.md`
  - rules, schema, routing, routines

### Standard Entry Fields

- `ID`
- `Reported`
- `Detected by`
- `Actor`
- `Surface`
- `Summary`
- `Severity`
- `Status`
- `Likely owner`
- `Superseded by migration?`
- `Notes`

### Standard Statuses

- `new`
- `triaged`
- `scheduled`
- `in active slice`
- `fixed`
- `wont-fix`
- `superseded`

### Standard Severities

- `blocker`
- `high`
- `medium`
- `low`

## Subagent Guidance

Subagents should report UX/UI bugs they find, but they should not directly own the repo-wide bug register by default.

Ask subagents to return:

- short bug summary
- actor/surface
- likely owner stream
- blocker vs defer recommendation
- whether the bug is likely to be superseded by upcoming migration work

Then convert that into the canonical inbox/triaged entry in the main thread.

## Resources

### `scripts/setup_bug_intake.py`

Bootstrap a generic `UX_UI_BUGS/` lifecycle folder inside a repo that uses `DOCS/` or `docs/`.

### `references/structure.md`

Generic folder structure, schema, and lifecycle rules.

### `references/governance-checklist.md`

Checklist for wiring the new bug system into a repo's existing docs/governance stack.
