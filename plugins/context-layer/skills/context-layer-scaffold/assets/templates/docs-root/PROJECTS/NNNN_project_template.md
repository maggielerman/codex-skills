---
title: NNNN – Project Title
description: Short project summary
status: active
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
priority: normal
projectType: standalone
parentProject:
programTrack:
---

# NNNN – Project Title

## Lifecycle Status Handling
- Keep project docs in `active/` with `status: active` while implementation is in progress.
- Move docs to `in-review/` with `status: in-review` when implementation is complete and awaiting walkthrough/sign-off.
- Move docs to `blocked/` with `status: blocked` when waiting on user decisions, permissions, access, or inputs.
- Move docs to `completed/` with `status: completed` only after walkthrough/sign-off.

## Project Hierarchy
- Use `projectType: standalone` for single-stream work.
- Use `projectType: parent` when this project coordinates multiple child streams.
- Use `projectType: child` when this work belongs to a parent project but has separate scope, lifecycle state, evidence, risk, or review.
- For child projects, set `parentProject` to the parent project id or filename stem.
- Use `programTrack` to group related work in the dashboard.

## Goals
- Goal 1
- Goal 2

## Scope
### In Scope
- Item 1

### Out of Scope
- Item 1

## Success Criteria
- Metric 1
- Metric 2

## Supporting Docs And Evidence
- Durable evidence path:
- Review packet paths:
- Audit/report paths:
- Related child projects:

## Visual/UX Quality Gate
For significant user-facing UI work, use `$visual-design-critique` before implementation sign-off or movement to `in-review`.

- Critique verdict:
- Evidence paths:
- Must-fix issues:
- Approved deviations:
- Follow-up verification:

## Milestones
- Milestone 1
- Milestone 2

## Checkpoint Log

### Checkpoint 01 - {{LAST_UPDATED_TS_ET}}
#### Completed Since Prior Checkpoint
- Initial project setup completed.
- Scope and success criteria documented.

#### Next Checkpoint Targets
- Deliver first implementation milestone.
- Record validation outcomes and open risks.

#### Notes
- Optional context, decisions, or links.

## Risks
- Risk 1

## Open Questions
- Question 1

## MAGGIE TODO
Use a literal `MAGGIE TODO:` callout for any work that needs Maggie's manual input, manual testing, evidence gathering, approval, or an external workstream.

- MAGGIE TODO: Capture the missing manual task, evidence request, or external dependency here.
- Remove resolved items so this section only reflects active follow-up.
