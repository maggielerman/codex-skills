# Lifecycle Rules

These rules mirror the standard docs scaffold and keep the orchestrator from inventing a parallel state machine.

## Default statuses

- `active`
- `in-review`
- `blocked`
- `completed`
- `backlog`
- `stale`

## Selection guidance

- Prefer `active` for the next executable tranche.
- Treat `in-review` as a review/closeout target, not a new implementation queue.
- Treat `blocked` as informational unless the work is specifically to unblock it.
- Pull from `backlog` or `stale` only when dependency order makes it the next safe move.

## Transition guidance

- `active -> in-review` when the tranche implementation is done and awaiting signoff.
- `in-review -> completed` only after the review gate passes.
- `* -> blocked` when a real decision, dependency, or access issue prevents forward motion.
- `blocked -> active` only when the stated blocker is cleared.

## Source-of-truth rule

The project docs and governance files remain canonical. The execution packet is a working control surface for the primary agent, not a competing tracker.
