---
name: evidence-system
description: "Use when asked to save, archive, organize, or link evidence: screenshots, audit packets, review packets, manifests, recordings, or verification records."
---

# Evidence System

Use this skill to route durable artifacts into the repo-native evidence system.

## First Checks

1. Locate `DOCS/evidence/`.
2. Identify the owning project doc and project id when possible.
3. Decide whether the artifact is active evidence, archived evidence, or a reusable template.

If the evidence system is missing, offer to run `$context-layer-scaffold`.

## Placement

- Current evidence: `DOCS/evidence/active/<project-id>/`
- Archived evidence: `DOCS/evidence/archive/<project-id>/`
- Templates: `DOCS/evidence/templates/`
- Preserved review packets: `DOCS/evidence/active/<project-id>/review-packets/<run-name>/`
- Journey audits: `DOCS/evidence/active/<project-id>/journey-audits/<audit-name>/`
- Visual design critique: `DOCS/evidence/active/<project-id>/visual-design/<run-name>/`
- Governance audits: `DOCS/evidence/active/<project-id>/governance-audits/<run-name>/`
- Portfolio Context Layer audits: `DOCS/evidence/active/context-layer-audits/<run-name>/`
- UX/UI bug evidence: `DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`

## Rules

- Link durable evidence from the owning project doc.
- Do not preserve temporary files unless they are useful for future verification or Maggie explicitly asks.
- Do not create separate durable temp buckets.
- Domain registers such as `DOCS/ux-ui-bugs/` are operating workflows; durable proof artifacts still belong under `DOCS/evidence/...`.
- Use `MAGGIE TODO:` if evidence gathering requires Maggie's manual action.
- Add a checkpoint when evidence changes the project state, review status, or sign-off readiness.
