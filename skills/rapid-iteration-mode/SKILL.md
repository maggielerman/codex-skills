---
name: rapid-iteration-mode
description: Custom skill created by Maggie Lerman. Lightweight working mode for fast product, UI, visual, content, and implementation iteration. Use when the user says "rapid iteration mode", asks for rapid visual iteration, wants quick color/layout/image/copy/UX finetuning, asks to try several small variants, or explicitly wants a tighter loop with lighter verification while preserving branch and change hygiene.
---

# Rapid Iteration Mode

Custom skill created by Maggie Lerman.

## Operating Posture

Move in small, reversible passes. Prefer the fastest useful edit plus a cheap visual or behavioral check over broad planning, full regression, or exhaustive documentation updates.

Use this mode for:

- Visual finetuning: color, spacing, layout rhythm, hierarchy, typography, imagery, responsive polish.
- Product/content iteration: labels, naming, copy, page structure, concept comparisons, information architecture.
- Light implementation iteration: focused component behavior or route tweaks when the change is easy to inspect.

Do not use this mode to weaken safety for destructive operations, production data changes, auth/payment/security work, legal/medical/financial advice, or broad refactors. Escalate back to normal verification when risk rises.

## Entry Check

At mode start, quickly orient without ceremony:

1. Check the current branch and dirty state.
2. Identify the surface under iteration and the fastest useful feedback loop.
3. Ask whether to create a dedicated branch or stay on the current branch when the answer is not already clear.

Use a concise question such as:

`Do you want a dedicated branch for this iteration run, or should I stay on the current branch for now?`

If the user chooses a branch, create or switch to one using the repository's branch naming conventions when available. If they stay on the current branch, continue, but keep watching change size.

## Iteration Loop

For each pass:

1. State the tiny adjustment being made.
2. Patch only the files needed for that adjustment.
3. Run the cheapest check that proves the specific change is visible or functional.
4. Report what changed and ask or infer the next micro-adjustment.

Prefer browser spot checks, screenshots, DOM/text confirmation, narrow tests, or targeted commands. Avoid full builds, full test suites, generated review packets, or documentation sweeps after every small edit unless the user asks or the change affects shared behavior.

For visual iteration, keep screenshots and user-visible evidence central. Compare against the current screen, not an imagined final state.

## Branch And Change Hygiene

Track accumulated change size while the mode stays active.

Prompt the user to branch or checkpoint when one of these happens:

- The worktree grows beyond a small handful of files.
- Untracked files or generated artifacts begin to accumulate.
- The iteration has produced multiple viable variants.
- The user starts asking for a new direction that could overwrite the current direction.
- The current branch contains unrelated user work that could make review or rollback confusing.

Use a light prompt:

`We have a decent stack of local changes now. Want me to branch/checkpoint before the next pass, or keep iterating here?`

Never discard or revert user changes without explicit instruction. If cleaning generated artifacts is useful, name exactly what would be removed and ask before deleting anything non-obvious.

## Verification Gradient

Use the smallest verification tier that matches the risk:

- **Tiny visual/content tweak**: browser refresh or DOM/text check.
- **Interactive UI tweak**: browser interaction plus state check.
- **Shared component or route rename**: targeted search plus focused route check.
- **Data/model/contract touch**: targeted unit test or schema check.
- **Before handoff/commit/publish**: lint/build/relevant tests as appropriate.

If a check fails, fix the immediate cause or clearly name the blocker. Do not quietly expand into a large debugging project unless the user wants that.

## Documentation

Do not update governance docs after every small pass. Update docs or checkpoints when:

- A route, interface, workflow, concept name, public behavior, or source of truth changes.
- The user asks to preserve the decision.
- The iteration reaches a meaningful checkpoint, comparison point, or handoff state.

When docs are required, keep them brief and timestamped if the repository expects checkpoint logs.

## Exit

When the user says to stop, lock, checkpoint, commit, compare, or ship:

1. Summarize the current changes and open questions.
2. Run the appropriate stronger verification tier.
3. Suggest branching, staging, committing, or making a review artifact only if it fits the user's requested next step.
