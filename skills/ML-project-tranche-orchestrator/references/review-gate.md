# Review Gate

Do not advance tranche status just because work landed. A tranche is ready only when the full gate passes.

## Gate checklist

### 1. Doc alignment

- The governing project doc still matches the tranche objective.
- Acceptance or success criteria are explicit rather than implied.
- Dependencies and blockers reflect current reality.
- The next checkpoint action is updated.

### 2. Implementation evidence

- Required implementation work is complete for the tranche scope.
- Verification evidence exists and is summarized.
- Open failures, skipped checks, or partial validations are clearly called out.
- Returned work still matches the approved execution packet, or any scope expansion is explicitly documented and justified.

### 3. Code-review evidence

- No obvious regression risk remains for the touched surfaces.
- Missing tests, incomplete cleanup, or hidden coupling are called out.
- Any residual risks are small enough to justify the intended lifecycle transition.

### 4. Lifecycle readiness

- `active -> in-review`: implementation slice complete and waiting for walkthrough/signoff.
- `in-review -> completed`: walkthrough/signoff criteria satisfied.
- `* -> blocked`: a real dependency, access issue, or decision gate prevents progress.

## Fail conditions

Fail the gate when any of these are true:

- acceptance criteria are vague or absent
- verification evidence is missing
- implementation drifted beyond tranche boundaries without documentation
- dependency state is contradictory
- the proposed lifecycle transition does not match repo governance
- the work no longer aligns with the cited source refs or must-read files that grounded the tranche

## Output when the gate fails

Return:
- what passed
- what failed
- the smallest change needed to pass
- whether the tranche should stay `active`, move to `blocked`, or remain `in-review`
