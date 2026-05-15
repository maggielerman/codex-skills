---
title: Documentation Index
description: Canonical documentation map for the project
status: stable
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Documentation
---

# Documentation Index

Welcome to the project documentation hub. This index keeps the knowledge base predictable and easy to navigate.

## Governance
- `AGENTS.md` — AI/automation guardrails
- `ROADMAP.md` — priorities and milestones
- `CHANGELOG.md` — notable changes

## Naming Standard
- Use `DOCS/` as the canonical docs root for all new and retrofitted scaffolds.
- Treat legacy `docs/` or `documentation/` roots as migration sources, not canonical destinations.
- Keep `PROJECTS/` uppercase as the reserved planning root.
- Keep other scaffolded docs folders lowercase.
- Keep repo-level governance and entrypoint docs uppercase: `README.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Keep content pages lowercase unless they are one of those reserved entrypoints.

## Projects (Planning & Tracking)
- `{{DOCS_ROOT}}/PROJECTS/NNNN_project_template.md` — reusable project template
- `{{DOCS_ROOT}}/PROJECTS/active/` — in progress
- `{{DOCS_ROOT}}/PROJECTS/in-review/` — implementation complete, awaiting walkthrough/sign-off
- `{{DOCS_ROOT}}/PROJECTS/blocked/` — waiting on user decisions/permissions/input
- `{{DOCS_ROOT}}/PROJECTS/completed/` — delivered
- `{{DOCS_ROOT}}/PROJECTS/backlog/` — queued
- `{{DOCS_ROOT}}/PROJECTS/stale/` — paused or deprecated

See `{{DOCS_ROOT}}/PROJECTS/README.md` for rules and numbering.

## Project Dashboard
- `{{DOCS_ROOT}}/PROJECTS/dashboard.html` — generated portfolio dashboard across lifecycle lanes, parent/child streams, status drift, and unresolved `MAGGIE TODO:` items.
- Markdown project docs remain the source of truth.

## Evidence
- `{{DOCS_ROOT}}/evidence/active/` — current durable audits, baseline packets, and review artifacts
- `{{DOCS_ROOT}}/evidence/archive/` — historical evidence retained for reference
- `{{DOCS_ROOT}}/evidence/templates/` — reusable packet and review templates

## MAGGIE TODO
- Use a literal `MAGGIE TODO:` callout inside project docs when work needs Maggie's manual input, evidence gathering, manual testing, approval, or an external workstream.
- Keep unresolved items in the project's `## MAGGIE TODO` section so they are easy to spot and can be surfaced in the dashboard.

## Product & Feature Guides
- `{{DOCS_ROOT}}/features/`
- `{{DOCS_ROOT}}/getting-started/`

## Engineering Guides
- `{{DOCS_ROOT}}/development/` (flat layout; no nested folders)
- `{{DOCS_ROOT}}/development/checkpoint-workflow.md` (timestamped checkpoint standard)
- `{{DOCS_ROOT}}/development/visual-design-quality-gate.md` (visual UI/UX critique gate)

## Visual Design Quality
- Use `$visual-design-critique` before sign-off for significant user-facing UI work.
- Record critique outcomes in the owning project doc and preserve screenshots or review-board packets only when they are useful durable evidence.

## Database
- `{{DOCS_ROOT}}/database/`

## Historical
- `{{DOCS_ROOT}}/historical/`

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Cloudflare Pages: Root Directory repo root, Build command `npm --prefix docs-site run build`, Build output directory `{{DOCS_ROOT}}/.vitepress/dist`
