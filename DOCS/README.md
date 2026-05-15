---
title: Documentation Index
description: Lean documentation map for the public skills library
status: stable
lastUpdated: "2026-05-15 10:40 ET (America/New_York)"
owner: Documentation
---

# Documentation Index

This folder keeps only repo-native notes that are useful alongside the public skills library. Public reader docs live in `docs-site/`.

## Governance
- `AGENTS.md` — AI/automation guardrails
- `ROADMAP.md` — priorities and milestones
- `CHANGELOG.md` — notable changes

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

## Engineering Guides
- `DOCS/development/` (flat layout; no nested folders)
- `DOCS/development/checkpoint-workflow.md` (timestamped checkpoint standard)

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Public docs site: `docs-site/` is a Next.js/Tailwind/shadcn app for the catalog and implementation notes.
