# UX/UI Bug Intake

UX/UI bug intake is optional during scaffold setup.

If enabled, create:

- `DOCS/ux-ui-bugs/README.md`
- `DOCS/ux-ui-bugs/INBOX.md`
- `DOCS/ux-ui-bugs/TRIAGED.md`
- `DOCS/ux-ui-bugs/ARCHIVE.md`

Use templates from:

- `assets/templates/ux-ui-bugs/`

## Operating Model

- Users, main agents, and subagents may detect UX/UI bugs.
- The main agent is the canonical logger/router.
- Subagents should report bug candidates with surface, actor, summary, likely owner stream, severity, and defer/fix-now recommendation.
- Keep the register lightweight; do not create one file per bug.

## Governance Wiring

When enabled, safe-update:

- `AGENTS.md`
- `ROADMAP.md`
- `DOCS/README.md`
- `DOCS/index.md`
- current project docs when the bug intake belongs to a specific project stream

Add a short note that UX/UI bug candidates go to `DOCS/ux-ui-bugs/INBOX.md`, triaged items go to `TRIAGED.md`, and durable proof goes under `DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`.

## Evidence

The bug register is not the evidence store. Store screenshots, recordings, reproduction notes, visual diffs, or audit packets under:

`DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`

Link evidence paths from the bug entry and owning project doc when the bug affects sign-off, lifecycle state, or roadmap scope.
