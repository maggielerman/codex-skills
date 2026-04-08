---
name: project-tranche-orchestrator
description: Act as the primary project manager and agent orchestrator for repos using the standard docs scaffold. Use when the user wants one primary agent to read project docs, derive the next tranche, delegate bounded work to subagents, manage handoffs, review completion, and write status updates back into the existing docs without creating a second source of truth.
metadata:
  short-description: Primary-agent tranche orchestration for docs-scaffold repos
---

# Project Tranche Orchestrator

Treat the primary agent as the only interface the user needs to manage. The primary agent owns tranche selection, subagent delegation, review synthesis, and docs writeback.

## Modes

- `collaborative`: default for a fresh tranche selection. Build a draft execution packet, show it to the user, and wait for approval or edits before spawning subagents.
- `autonomous`: skip the initial approval pause and proceed to delegation once the packet is internally consistent.

Mode selection rule:
- default to `collaborative` when reconstructing a tranche from repo docs for the first time in a thread
- use `autonomous` when the user explicitly asks for it or when working from an already approved packet/current tranche
- switch back to `collaborative` if docs are contradictory, tranche boundaries feel soft, or the primary agent detects drift risk

## Assumptions

- The target repo uses the standard docs scaffold with `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, and `DOCS/PROJECTS/` or `docs/PROJECTS/`.
- The docs remain the source of truth. Do not create a persistent queue or a standalone execution-packet file unless the user explicitly asks.
- The default unit of work is one executable tranche, not a backlog refresh.
- Subagents are used only for bounded slices with clear ownership and acceptance criteria.

## Required behavior

- Reconstruct repo state from docs before deciding what to do.
- Prefer one current tranche packet over a standing queue or kanban board.
- Keep the execution packet ephemeral by default: return it in the primary response and use it to guide delegation, review, and writeback.
- Update existing project docs and governance docs when reality changes.
- Escalate only for real blockers, permissions, or high-impact tradeoffs.
- Do not advance lifecycle state unless the review gate passes.
- Treat guardrails as graduated rather than absolute. Be strict about scope clarity and ownership boundaries, but flexible about implementation details inside a bounded slice.

## Helper files

Resolve these relative to this skill directory:

- `../../scripts/discover_project_context.py`
- `../../scripts/validate_execution_packet.py`
- `references/execution-packet-schema.md`
- `references/review-gate.md`
- `references/lifecycle-rules.md`
- `references/subagent-prompt-template.md`

## Workflow

### 1. Discover repo context

Run the discovery helper first:

```bash
python3 ../../scripts/discover_project_context.py --repo .
```

Use the result to identify:
- docs root and `PROJECTS` directory
- non-completed project docs by lifecycle status
- missing governance inputs
- candidate target project/tranche
- whether blockers or weak acceptance criteria already prevent safe orchestration

If the repo does not match the scaffold assumptions, stop and report the exact blocker rather than inventing state.

### 2. Select the target tranche

Default target selection order:
1. Unblocked `active` project with a meaningful next step
2. `in-review` project that needs tranche review or closeout
3. `backlog` or `stale` project only when it is clearly the next dependency-safe move
4. `blocked` only to explain or prepare the unblock path

When several candidates exist, prefer the one with:
- explicit dependencies already satisfied
- explicit acceptance or exit criteria
- the clearest next checkpoint action
- the lowest cross-stream file collision risk

### 3. Build one execution packet

Use the execution packet contract in `references/execution-packet-schema.md`.

The packet must include:
- orchestration mode and approval behavior
- project identifier and source doc
- tranche id/name and objective
- explicit in-scope items
- explicit non-goals
- dependencies and blockers
- source-of-truth refs and must-read files
- drift triggers that force reassessment or escalation
- subagent assignments with role-based prompts
- required verification evidence
- review criteria
- exit criteria
- escalation conditions
- lifecycle target after review

Keep the packet in the response unless the user explicitly asks for a file.

Always-on packet guardrails:
- `source_refs`: point each major decision back to the governing docs or repo files
- `must_read_files`: list the docs/code files the primary agent or subagent must read before acting
- `write_paths`: bound where delegated work may land
- `drift_triggers`: name the conditions that require re-read, regroup, or escalation

Mode-dependent packet guardrails:
- `collaborative`: `user_approval_required` should be `true` before delegation
- `autonomous`: `user_approval_required` may be `false`, but the packet still needs the always-on guardrails

If the user wants to guide or sanity-check the tranche logic, stay in `collaborative` mode until the packet is approved.

### 4. Delegate bounded work

The primary agent owns the orchestration loop. Subagents handle bounded slices only.

When creating assignments:
- keep each assignment narrow and decision-light
- define explicit write paths or owned surfaces when possible
- attach source refs and must-read files so the subagent can re-anchor against the real repo state
- include acceptance criteria and verification expectations
- include one handoff prompt using `references/subagent-prompt-template.md`
- avoid parallel delegation when write paths overlap or sequencing is sensitive

Default to 1-3 assignments. More than 3 requires clear evidence that the work is independent.

If subagent tooling is unavailable, stay single-agent but preserve the same packet structure and ownership boundaries.

Subagent context guardrails:
- include a scope ledger: project goal, tranche objective, owned scope, non-goals, exit criteria, blockers
- include the smallest useful must-read list instead of a compressed paraphrase alone
- require source refs for tranche objective and acceptance criteria
- set `quote_back_required` when the task is risky, multi-step, or easy to drift on

Use quote-back as a light anti-drift tool, not a mandatory ceremony for every trivial slice. Prefer it when:
- the tranche was reconstructed from several docs
- the assignment touches multiple surfaces
- acceptance criteria are easy to misread
- the repo is in a sensitive or high-rework area

### 5. Review tranche completion

Run the review gate from `references/review-gate.md`.

A tranche is not ready to advance just because implementation happened. The gate requires:
- project-doc acceptance criteria satisfied
- dependencies and blockers reconciled
- verification evidence present
- code-review pass for regressions, risks, and missing tests
- lifecycle transition justified by repo governance
- returned work still matches the approved execution packet or documented scope change

When useful, validate the structured packet before or after delegation:

```bash
python3 ../../scripts/validate_execution_packet.py packet.json
```

### 6. Write back to docs

Default writeback targets:
- the relevant project doc
- `ROADMAP.md` when sequencing or milestone reality changed
- `CHANGELOG.md` when completed work or status materially changed

Writeback rules:
- use absolute timestamps
- respect the repo's timestamp tooling when available
- record what completed since the prior checkpoint
- record what happens before the next checkpoint
- do not create a separate queue artifact

## Output contract

Return sections in this order:

1. `Target tranche`
2. `Execution packet`
3. `Delegation plan`
4. `Review gate`
5. `Docs writeback`
6. `Blockers or escalations`

In `collaborative` mode, the first response should return a draft packet and pause before delegation.
In `autonomous` mode, return a concise packet summary and proceed unless a blocker threshold is hit.

## Blocker threshold

Stop and ask the user only when:
- required docs inputs are missing or contradictory
- the target tranche cannot be selected safely
- the next step needs policy, architectural, or product direction
- access, credentials, or external systems are unavailable
- safe delegation boundaries cannot be established

## Hardened invocation prompt

`Use $project-tranche-orchestrator to read the repo's docs-scaffold project state, select the next safe tranche, build one execution packet with source refs, must-read files, write-path boundaries, and drift triggers, then either pause for my approval in collaborative mode or proceed in autonomous mode. Keep subagents tightly scoped, prevent overlap when possible, review whether the tranche is actually ready to advance, and write any needed status updates back into the existing project docs and governance files. Keep me interacting only with the primary agent unless a real blocker or high-impact tradeoff requires my input.`
