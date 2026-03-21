---
name: continue-until-blocked
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
- Prefer action over status narration. Do the work, then report milestones briefly.
- Keep working through solvable issues. Debug, test, and adjust before escalating.
- Make reasonable local decisions when the choice is low-risk and consistent with existing repo patterns.
- Escalate only for decisions with meaningful product, architectural, access, policy, or rollout consequences.

## Continuous execution loop

1. Reconfirm the immediate target.
- Verify the active task, cutover goal, and any current blockers or dependencies from the relevant project doc and local repo state.
- Check branch status and recent work so new changes build on the latest reality.

2. Take the next meaningful slice.
- Implement the next bounded chunk that materially advances the cutover.
- Prefer slices that leave the repo in a testable, reviewable state.

3. Verify before and after risky changes.
- Run focused tests, linters, builds, or local checks that match the change.
- Expand verification when the change crosses boundaries or affects rollout safety.

4. Keep git hygiene current.
- Create or switch branches when needed, following the repo's existing naming and workflow rules.
- Commit at meaningful intervals with clear messages.
- Push after meaningful milestones so progress is durable and recoverable.
- Merge when the work is ready and repo policy/access allow it; if direct merge is not possible, prepare the branch so the remaining merge step is explicit and minimal.

5. Keep docs in sync with reality.
- Update the relevant project doc, roadmap/changelog entries, and other standardized docs whenever a milestone changes status, scope, blockers, or next steps.
- Use the repo's timestamp tooling when available; otherwise use absolute timestamps and avoid relative phrasing like `today` or `tomorrow`.
- Record what completed since the prior checkpoint and what happens before the next one.

6. Repeat without waiting for permission.
- Continue into the next slice immediately after each verified milestone.
- Do not stop just because one commit, one test run, or one doc update landed.

## Meaningful interval policy

Treat an interval as meaningful when at least one of these becomes true:
- A coherent implementation slice is complete.
- A risky change has been stabilized by tests or debugging.
- A doc status or checkpoint meaningfully changed.
- A branch is ready to push or merge.
- The repo is at a clean handoff point that would be expensive to reconstruct.

## Blocker threshold

Stop and ask the user only when one of these is true:
- Required access, credentials, infrastructure, or external systems are unavailable.
- A choice has non-obvious product or architectural tradeoffs that the current scope does not answer.
- Repo policy prevents the next safe step and there is no compliant workaround.
- The remaining action is destructive, irreversible, or production-facing in a way that needs explicit approval.
- Conflicting docs or code realities make the intended cutover ambiguous.

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

## Hardened invocation prompt

`Proceed continuously without waiting for my intervention. Assume the repo and scope are already understood. Keep executing meaningful slices until the cutover is complete or you hit a real blocker or decision that requires my input. Maintain branch, commit, push, merge, testing, and docs hygiene at meaningful intervals, and keep the standardized project docs current as the work advances.`
