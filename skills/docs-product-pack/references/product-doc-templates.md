# Product Doc Templates

Use these templates when creating missing docs in a product docs retrofit/scaffold workflow.
Keep changes minimal when existing files already have structure.

## `README.md` (product docs folder)

```md
# Product docs

This folder contains lightweight product documentation kept alongside the code.

## Files
- **Product brief** (`product-brief.md`): one-page overview with problem, user, MVP scope, and success criteria.
- **Lean canvas** (`lean-canvas.md` or `lean-canvas.pdf/png`): business model snapshot.
- **PRD** (`prd.md`): requirements-level detail kept lean.
- **Decision log** (`decision-log.md`): non-trivial decisions and rationale.

## Update cadence
- Update the brief when scope or target user changes.
- Update the PRD when implementation scope changes materially.
- Add a decision log entry when making non-trivial tradeoffs.

## Status
- Last updated: {{DATE}}
- Owner: {{OWNER_OR_TEAM}}
```

## `product-brief.md`

```md
# Product brief: {{PRODUCT_NAME}}

## 1) Problem
**Who is the user?**
- {{PRIMARY_USER}}

**What pain are we solving?**
- {{PROBLEM_STATEMENT}}

## 2) Why now
- {{WHY_NOW}}

## 3) Solution (MVP)
**One-sentence pitch:** {{PITCH}}

### MVP scope (in)
- {{MVP_IN_1}}
- {{MVP_IN_2}}

### Out of scope (v1)
- {{OUT_1}}
- {{OUT_2}}

## 4) Success metrics
- **Activation:** {{METRIC}}
- **Retention:** {{METRIC}}
- **Revenue (if applicable):** {{METRIC}}

## 5) Assumptions and risks
| Assumption | Risk if false | Validation plan |
|---|---|---|
| {{ASSUMPTION}} | {{RISK}} | {{TEST}} |

## 6) Open questions
- {{QUESTION_1}}
- {{QUESTION_2}}
```

## `lean-canvas.md`

```md
# Lean Canvas: {{PRODUCT_NAME}}

> If you maintain this elsewhere (Notion/Figma), store a dated export in `snapshots/` and keep this page as the index.

## Problem
- {{PROBLEM_1}}
- {{PROBLEM_2}}

## Customer segments
- {{SEGMENT_1}}

## Unique value proposition
- {{UVP}}

## Solution
- {{SOLUTION_1}}
- {{SOLUTION_2}}

## Channels
- {{CHANNELS}}

## Revenue streams
- {{REVENUE}}

## Cost structure
- {{COSTS}}

## Key metrics
- {{KEY_METRICS}}

## Unfair advantage
- {{ADVANTAGE}}
```

## `prd.md` (lean PRD)

```md
# PRD: {{PRODUCT_NAME}} (MVP)

## Goals
- {{GOAL_1}}
- {{GOAL_2}}

## Non-goals
- {{NON_GOAL_1}}

## Users and primary use cases
- {{USE_CASE_1}}
- {{USE_CASE_2}}

## Requirements (high level)
### Must-have
- {{REQ_1}}
- {{REQ_2}}

### Nice-to-have
- {{NICE_1}}

## Constraints
- Tech: {{TECH_CONSTRAINTS}}
- Legal/compliance: {{LEGAL_CONSTRAINTS}}
- Data/privacy: {{DATA_CONSTRAINTS}}

## Analytics and measurement
- Events: {{EVENTS}}
- Dashboards: {{DASHBOARDS}}

## Open questions
- {{OPEN_QUESTION_1}}
```

## `decision-log.md`

```md
# Decision log

Use this log for decisions that change scope, architecture, pricing, user flow, or core constraints.

## Template
### {{DATE}}: {{DECISION_TITLE}}
**Context:** {{CONTEXT}}
**Decision:** {{DECISION}}
**Alternatives considered:** {{ALTS}}
**Tradeoffs:** {{TRADEOFFS}}
**Follow-ups:** {{FOLLOWUPS}}
**Links:** {{LINKS}}
```

