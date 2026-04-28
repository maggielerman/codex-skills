# Collaborative Walkthrough Question Bank

Use these prompts to keep walkthroughs consistent and decision-oriented.

## 1) Scope And Acceptance

- Is the stated goal fully met, or is anything intentionally deferred?
- Are any success criteria still unproven?
- Do you accept the current warning profile as non-blocking?

## 2) Dependencies And Operations

- Are required environment/deployment dependencies confirmed for steady-state operation?
- Is there any dependency that needs owner assignment before closure?
- Should any open dependency become a follow-up project before sign-off?

## 3) Risk Review

- Which residual risks are accepted at sign-off?
- Which risks require mitigation before moving to completed?
- Are there risks that should be escalated to roadmap immediate priorities?

## 4) Validation And Evidence

- Do current test/audit results satisfy your acceptance threshold?
- Do we need one more verification run on latest commit before closure?
- Is any proof artifact missing from checkpoint logs?

## 5) Lifecycle Decision

- Approve move to `completed` now, or keep in `in-review` for follow-up?
- If approved, should we open a new numbered follow-up stream immediately?
- If not approved, what exact gate must pass before re-walkthrough?
