---
name: continue-until-blocked
author: Maggie Lerman
description: Execute already-scoped repository work autonomously until the cutover is complete or a true blocker requires user input. Use when the user says to keep going without intervention, continue until blocked, finish the cutover, or otherwise hand the thread continuous execution authority. Assume the current thread already understands the repository and approved scope, and assume project docs follow the standard docs scaffolding with governance files and status-based project docs.
---

# Continue Until Blocked

Execute the next approved work continuously instead of pausing for routine check-ins.

Assume:
- The current thread already understands the repo, the scoped work, and the desired cutover.
- The repo uses the standardized docs system with `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, and `DOCS/PROJECTS/` or `docs/PROJECTS/`.
- The user wants forward motion unless a blocker is real, material, and not safely workaroundable.

## Operating rules

- Re-anchor quickly, not from scratch. Re-read only the project docs or repo files needed to confirm the next step or keep documentation accurate.
- Maintain scope continuity without over-constraining execution:
  - Preserve project intent: objective, constraints, and explicit non-goals.
  - Preserve tranche intent: planned outcomes, dependencies, and risk boundaries.
  - Allow adaptive sequencing: reorder or refine slices when it increases throughput, reduces risk, or unblocks downstream work.
  - Treat scope expansion as explicit, not forbidden: if adjacent work meaningfully improves cutover success, perform it and document why.
- Prefer action over status narration. Do the work, then report milestones briefly.
- Treat execution hygiene as part of the deliverable, not overhead. Long-running autonomy must increase process rigor over time, not relax it.
- Keep working through solvable issues. Debug, test, and adjust before escalating.
- Make reasonable local decisions when the choice is low-risk and consistent with existing repo patterns.
- Escalate only for decisions with meaningful product, architectural, access, policy, or rollout consequences.
- Prefer invariant language over memory shortcuts. Reuse exact terms from the governing project docs when describing goals, tranche names, and completion state.
- Think in rolling horizons, not one-step loops. Keep a live plan for:
  - Current slice
  - Next two to three slices
  - Known risks and dependency-critical path

## Continuous execution loop

1. Reconfirm the immediate target.
- Verify the active task, cutover goal, and any current blockers or dependencies from the relevant project doc and local repo state.
- Re-state a compact scope ledger at session start and whenever context shifts materially:
  - Project goal (one line)
  - In-scope for this tranche (one to three bullets)
  - Explicit out-of-scope/non-goals (one to three bullets)
  - Current tranche exit criteria
- Check branch status and recent work so new changes build on the latest reality.

2. Take the next meaningful slice.
- Implement the next bounded chunk that materially advances the cutover.
- Prefer slices that leave the repo in a testable, reviewable state.
- Stay tranche-aligned by default, but pull forward dependency-enabling work when it is clearly beneficial; record the rationale in the checkpoint.

3. Verify before and after risky changes.
- Run focused tests, linters, builds, or local checks that match the change.
- Expand verification when the change crosses boundaries or affects rollout safety.
- At each meaningful interval, leave explicit verification evidence (commands run, pass/fail, and follow-up if partial).

4. Keep git hygiene current.
- Create or switch branches when needed, following the repo's existing naming and workflow rules.
- Commit at meaningful intervals with clear messages tied to the slice outcome.
- Push after meaningful milestones so progress is durable and recoverable.
- Merge when the work is ready and repo policy/access allow it; if direct merge is not possible, prepare the branch so the remaining merge step is explicit and minimal.
- Avoid long-lived unpushed or undocumented work; checkpoint progress so another agent can resume without reconstruction.

5. Keep docs in sync with reality.
- Update the relevant project doc, roadmap/changelog entries, and other standardized docs whenever a milestone changes status, scope, blockers, or next steps.
- Use the repo's timestamp tooling when available; otherwise use absolute timestamps and avoid relative phrasing like `today` or `tomorrow`.
- Record what completed since the prior checkpoint and what happens before the next one.
- Add a context checkpoint at each meaningful interval so a future resume does not lose state:
  - absolute timestamp
  - active project scope sentence
  - active tranche and exit criteria status
  - completed since prior checkpoint
  - next best action and one fallback action
- Keep organizational artifacts synchronized with implementation state at checkpoints:
  - branch/PR status reflects reality
  - project doc lifecycle/status reflects reality
  - roadmap/changelog entries reflect newly completed milestones or scope shifts

6. Repeat without waiting for permission.
- Continue into the next slice immediately after each verified milestone.
- Do not stop just because one commit, one test run, or one doc update landed.
- Before each new slice, sanity-check that actions still align with project intent; if not, reconcile explicitly before continuing.

## Meaningful interval policy

Treat an interval as meaningful when at least one of these becomes true:
- A coherent implementation slice is complete.
- A risky change has been stabilized by tests or debugging.
- A doc status or checkpoint meaningfully changed.
- A branch is ready to push or merge.
- The repo is at a clean handoff point that would be expensive to reconstruct.

## Checkpoint integrity contract

At each meaningful interval, complete as many of these as repository policy and access allow:
- Branch hygiene: create/switch branch when needed; keep branch purpose clear.
- Commit hygiene: commit coherent slices with clear intent and impact.
- Push hygiene: push milestone commits so progress is durable.
- Verification hygiene: run the highest-value checks for the changed surface area.
- Docs hygiene: update project docs and governance artifacts to match code reality.
- Merge hygiene: merge when ready and allowed, or leave a minimal, explicit final merge step.

Do not trade these off casually for short-term speed. If one checkpoint artifact is intentionally deferred, record why and when it will be completed.

## Blocker threshold

Stop and ask the user only when one of these is true:
- Required access, credentials, infrastructure, or external systems are unavailable.
- A choice has non-obvious product or architectural tradeoffs that the current scope does not answer.
- Repo policy prevents the next safe step and there is no compliant workaround.
- The remaining action is destructive, irreversible, or production-facing in a way that needs explicit approval.
- Conflicting docs or code realities make the intended cutover ambiguous.
- The project scope or tranche scope cannot be reliably reconstructed from available artifacts.
- Multiple plausible paths exist and the wrong choice could create expensive rework beyond current risk tolerance.

Before escalating, attempt reasonable workarounds and capture the evidence.

## Response contract when blocked

When escalation is necessary, report:
- what was completed
- what was attempted to unblock the issue
- the exact blocker
- the smallest decision or input needed from the user
- the recommended next move once that input arrives

## Done condition

Treat the assignment as complete only when the cutover is done or the remaining gap is a true blocker under the threshold above.

Completion usually means:
- implementation landed
- verification run at the appropriate level
- docs/status artifacts updated
- branch/commit/push/merge workflow advanced as far as repo policy and access permit
- residual risks or follow-ups stated clearly
- no unresolved scope ambiguity remains for the active project or tranche
- no silent drift in process quality, documentation quality, or organizational state

## Hardened invocation prompt

`Proceed continuously without waiting for my intervention. Assume the repo and scope are already understood. Keep executing meaningful slices with independent judgment, advanced reasoning, and long-horizon planning until the cutover is complete or you hit a real blocker or decision that requires my input. Preserve project and tranche intent while allowing adaptive sequencing and explicit scope evolution when it materially improves cutover success. At meaningful checkpoints, maintain non-negotiable branch, commit, push, merge, verification, and docs hygiene so process quality and organizational clarity do not degrade over time. Keep context checkpoints so progress is recoverable without drift.`
