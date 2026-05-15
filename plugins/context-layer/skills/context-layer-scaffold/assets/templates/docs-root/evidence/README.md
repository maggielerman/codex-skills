---
title: Evidence System
description: Canonical storage model for audits, baseline packets, review artifacts, and historical proof.
status: evolving
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# Evidence System

Use `{{DOCS_ROOT}}/evidence/` as the canonical home for durable audits, baseline packets, review artifacts, and historical proof.

## Structure

- `{{DOCS_ROOT}}/evidence/active/`
- `{{DOCS_ROOT}}/evidence/archive/`
- `{{DOCS_ROOT}}/evidence/templates/`

Prefer project-scoped organization inside those folders.

If a review packet is intentionally preserved, store it under the owning project's evidence directory, typically:

- `{{DOCS_ROOT}}/evidence/active/<project>/review-packets/<run-name>/`
- `{{DOCS_ROOT}}/evidence/archive/<project>/review-packets/<run-name>/`

## Recommended Project Evidence Paths

- Review boards: `{{DOCS_ROOT}}/evidence/active/<project>/review-packets/<run-name>/`
- User journey audits: `{{DOCS_ROOT}}/evidence/active/<project>/journey-audits/<audit-name>/`
- Visual design critique: `{{DOCS_ROOT}}/evidence/active/<project>/visual-design/<run-name>/`
- Governance audits: `{{DOCS_ROOT}}/evidence/active/<project>/governance-audits/<run-name>/`
- Portfolio/context-layer audits: `{{DOCS_ROOT}}/evidence/active/context-layer-audits/<run-name>/`
- UX/UI bug evidence: `{{DOCS_ROOT}}/evidence/active/<project>/ux-ui-bugs/<bug-id>/`

Domain-specific registers may live elsewhere in `{{DOCS_ROOT}}`, but durable screenshots, PDFs, manifests, recordings, and verification proof should be stored here and linked from the owning project doc.
