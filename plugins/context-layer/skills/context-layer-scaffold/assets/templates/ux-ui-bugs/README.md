---
title: UX/UI Bug Intake
description: Lightweight register for user, agent, and subagent-detected UX/UI bugs
status: active
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# UX/UI Bug Intake

Use this folder for lightweight UX/UI bug intake during active implementation.

## Files

- `INBOX.md` - fast capture for new bug candidates
- `TRIAGED.md` - normalized working queue
- `ARCHIVE.md` - fixed, rejected, superseded, or historical items

## Operating Model

- Users, main agents, and subagents may detect bugs.
- The main agent is the canonical logger/router.
- Subagents should report concise bug candidates rather than directly owning the register.

## Evidence

Keep durable screenshots, recordings, reproduction packets, or audits under:

`{{DOCS_ROOT}}/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`

Link evidence paths from bug entries and owning project docs when bugs affect project state or sign-off.
