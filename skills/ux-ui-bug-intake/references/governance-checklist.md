# Governance Checklist For UX/UI Bug Intake

After scaffolding the lifecycle folder, wire it into the repo's operating docs.

## Recommended Governance Touchpoints

- `AGENTS.md`
  - say where UX/UI bugs should be logged
  - note that the main agent is the canonical logger/router
- roadmap / current priorities doc
  - explain that UX/UI bugs should be captured continuously but only blocker/local issues should interrupt active work
- docs index / docs README
  - add the lifecycle folder to the documentation map
- current-state / status doc
  - mention that the repo now has a UX/UI bug intake system
- changelog
  - record when the system was introduced

## Good Outcome

The repo should make all of the following obvious:

- where new UX/UI bugs get captured
- where triaged bugs live
- where closed bugs go
- who normalizes and routes entries
- how bugs get pulled into execution streams

## Avoid

- burying the system in an unlinked folder
- creating a folder without updating governance docs
- requiring the user to maintain taxonomy manually
- making every visual bug interrupt the current branch
