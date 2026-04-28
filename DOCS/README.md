---
title: Documentation Index
description: Canonical documentation map for the project
status: stable
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Documentation
---

# Documentation Index

Welcome to the project documentation hub. This index keeps the knowledge base predictable and easy to navigate.

## Governance
- `AGENTS.md` — AI/automation guardrails
- `ROADMAP.md` — priorities and milestones
- `CHANGELOG.md` — notable changes

## Naming Standard
- Prefer `DOCS/` when this docs root is newly scaffolded; preserve an existing `docs/` or `documentation/` root when retrofitting.
- Keep `PROJECTS/` uppercase as the reserved planning root.
- Keep other scaffolded docs folders lowercase.
- Keep repo-level governance and entrypoint docs uppercase: `README.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Keep content pages lowercase unless they are one of those reserved entrypoints.

## Projects (Planning & Tracking)
- `DOCS/PROJECTS/active/` — in progress
- `DOCS/PROJECTS/in-review/` — implementation complete, awaiting walkthrough/sign-off
- `DOCS/PROJECTS/blocked/` — waiting on user decisions/permissions/input
- `DOCS/PROJECTS/completed/` — delivered
- `DOCS/PROJECTS/backlog/` — queued
- `DOCS/PROJECTS/stale/` — paused or deprecated

See `DOCS/PROJECTS/README.md` for rules and numbering.

## Evidence
- `DOCS/evidence/active/` — current durable audits, baseline packets, and review artifacts
- `DOCS/evidence/archive/` — historical evidence retained for reference
- `DOCS/evidence/templates/` — reusable packet and review templates

## MAGGIE TODO
- Use a literal `MAGGIE TODO:` callout inside project docs when work needs Maggie's manual input, evidence gathering, manual testing, approval, or an external workstream.
- Keep unresolved items in the project's `## MAGGIE TODO` section so they are easy to spot and can be surfaced in the dashboard.

## Product & Feature Guides
- `DOCS/features/`
- `DOCS/getting-started/`

## Engineering Guides
- `DOCS/development/` (flat layout; no nested folders)
- `DOCS/development/checkpoint-workflow.md` (timestamped checkpoint standard)

## Database
- `DOCS/database/`

## Historical
- `DOCS/historical/`

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Customer docs site: `docs-site/` is a Next.js/Tailwind/shadcn app. Build with `npm --prefix docs-site run build`.
