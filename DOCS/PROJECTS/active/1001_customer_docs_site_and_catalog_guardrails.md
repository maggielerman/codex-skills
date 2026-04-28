---
title: Customer Docs Site and Catalog Guardrails
description: Build the commercial customer docs surface and make suite catalog drift auditable
status: active
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Product/Engineering
---

# 1001 Customer Docs Site and Catalog Guardrails

## Goal

Create a repeatable operating layer for selling and supporting Codex Skills Packs while keeping customer-facing docs separate from repo maintenance docs.

## Scope

- Add catalog drift detection before generated catalog output is regenerated.
- Add a customer-facing Next.js/Tailwind/shadcn docs site.
- Generate customer-facing skill and plugin pages from source metadata.
- Add repo-native product operating docs, evidence folders, docs tooling, and CI hooks.

## Checkpoints

### Checkpoint 01 - 2026-04-28 12:04 ET (America/New_York)

Completed since prior checkpoint:
- Added `scripts/build_catalog.py --check` drift detection for `skills/`, `skills/SUITE_SKILLS.txt`, and `skills/SUITE_METADATA.json`.
- Added `docs-site/` customer-facing marketing and implementation docs site.
- Added docs-site catalog generation from `skills/manifest.json` and custom plugin metadata.
- Added this `DOCS/` product operating scaffold to keep repo memory and customer docs distinct.

Next checkpoint target:
- Review customer-facing copy for purchase readiness.
- Decide pricing, license, and support boundaries before launch.

## MAGGIE TODO

- MAGGIE TODO: Decide final pricing, license, and support boundaries before selling the packs.
- MAGGIE TODO: Provide preferred public contact or purchase CTA for the docs site.
