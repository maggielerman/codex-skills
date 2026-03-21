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

## Projects (Planning & Tracking)
- `{{DOCS_ROOT}}/PROJECTS/active/` — in progress
- `{{DOCS_ROOT}}/PROJECTS/in-review/` — implementation complete, awaiting walkthrough/sign-off
- `{{DOCS_ROOT}}/PROJECTS/blocked/` — waiting on user decisions/permissions/input
- `{{DOCS_ROOT}}/PROJECTS/completed/` — delivered
- `{{DOCS_ROOT}}/PROJECTS/backlog/` — queued
- `{{DOCS_ROOT}}/PROJECTS/stale/` — paused or deprecated

See `{{DOCS_ROOT}}/PROJECTS/README.md` for rules and numbering.

## Product & Feature Guides
- `{{DOCS_ROOT}}/features/`
- `{{DOCS_ROOT}}/getting-started/`

## Engineering Guides
- `{{DOCS_ROOT}}/development/` (flat layout; no nested folders)
- `{{DOCS_ROOT}}/development/checkpoint-workflow.md` (timestamped checkpoint standard)

## Database
- `{{DOCS_ROOT}}/database/`

## Historical
- `{{DOCS_ROOT}}/historical/`

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Cloudflare Pages: Root Directory repo root, Build command `npm --prefix docs-site run build`, Build output directory `{{DOCS_ROOT}}/.vitepress/dist`
