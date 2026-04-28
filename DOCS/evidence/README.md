---
title: Evidence System
description: Canonical storage model for audits, baseline packets, review artifacts, and historical proof.
status: evolving
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Product/Engineering
---

# Evidence System

Use `DOCS/evidence/` as the canonical home for durable audits, baseline packets, review artifacts, and historical proof.

## Structure

- `DOCS/evidence/active/`
- `DOCS/evidence/archive/`
- `DOCS/evidence/templates/`

Prefer project-scoped organization inside those folders.

If a review packet is intentionally preserved, store it under the owning project's evidence directory, typically:

- `DOCS/evidence/active/<project>/review-packets/<run-name>/`
- `DOCS/evidence/archive/<project>/review-packets/<run-name>/`
