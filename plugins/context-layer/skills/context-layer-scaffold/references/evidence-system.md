# Evidence System

Use `DOCS/evidence/` as the durable artifact home.

## Required Folders

- `DOCS/evidence/active/`
- `DOCS/evidence/archive/`
- `DOCS/evidence/templates/`

## Placement Rules

Use `active/` for current evidence needed for ongoing verification, review, or sign-off.

Use `archive/` for historical evidence retained for context.

Use `templates/` for reusable evidence packet templates.

For project-specific evidence, prefer:

- `DOCS/evidence/active/<project-id>/`
- `DOCS/evidence/archive/<project-id>/`

For preserved review-board runs:

- `DOCS/evidence/active/<project-id>/review-packets/<run-name>/`

For user journey audits:

- `DOCS/evidence/active/<project-id>/journey-audits/<audit-name>/`

For visual design critique evidence:

- `DOCS/evidence/active/<project-id>/visual-design/<run-name>/`

For governance or Context Layer audits:

- `DOCS/evidence/active/<project-id>/governance-audits/<run-name>/`
- `DOCS/evidence/active/context-layer-audits/<run-name>/` for portfolio-wide audits

For UX/UI bug evidence:

- `DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`

Do not create a separate durable temp bucket. Temporary files should be removed unless Maggie explicitly asks to preserve them.

Domain-specific registers, such as `DOCS/ux-ui-bugs/`, may exist as operating workflows. Durable screenshots, PDFs, manifests, recordings, and verification proof should still live under `DOCS/evidence/...` and be linked from the register or owning project doc.
