---
title: Project Documentation
description: Central hub for product, engineering, and operational docs
status: evolving
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Documentation
---

# Project Documentation

Welcome to the documentation hub. Use the sections below to navigate the system.

## Naming Standard
- Prefer `DOCS/` for newly scaffolded docs roots, but preserve existing `docs/` or `documentation/` roots when retrofitting.
- Keep `PROJECTS/` uppercase as the reserved planning root.
- Keep other scaffolded docs directories lowercase.
- Keep governance and entrypoint docs uppercase: `README.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Keep content pages lowercase unless they are one of those reserved entrypoints.

## Getting Started
- `{{DOCS_ROOT}}/getting-started/`

## Features
- `{{DOCS_ROOT}}/features/`

## Development
- `{{DOCS_ROOT}}/development/`
- `{{DOCS_ROOT}}/development/visual-design-quality-gate.md`

## Evidence
- `{{DOCS_ROOT}}/evidence/`
- `{{DOCS_ROOT}}/evidence/active/`
- `{{DOCS_ROOT}}/evidence/archive/`
- `{{DOCS_ROOT}}/evidence/templates/`

## Database
- `{{DOCS_ROOT}}/database/`

## Deployment
- `{{DOCS_ROOT}}/deployment/`

## API
- `{{DOCS_ROOT}}/api/`

## Contributing
- `{{DOCS_ROOT}}/contributing/`

## Projects
- `{{DOCS_ROOT}}/PROJECTS/`

## Project Lifecycle Status Folders
- `{{DOCS_ROOT}}/PROJECTS/active/` - in progress
- `{{DOCS_ROOT}}/PROJECTS/in-review/` - ready for collaborative walkthrough
- `{{DOCS_ROOT}}/PROJECTS/blocked/` - waiting on user input or permissions
- `{{DOCS_ROOT}}/PROJECTS/completed/` - delivered after walkthrough/sign-off
- `{{DOCS_ROOT}}/PROJECTS/backlog/` - queued
- `{{DOCS_ROOT}}/PROJECTS/stale/` - paused or deprecated

## Historical
- `{{DOCS_ROOT}}/historical/`

## MAGGIE TODO
- Add a literal `MAGGIE TODO:` callout inside project docs whenever work needs Maggie's manual input, evidence gathering, manual testing, approval, or an external dependency.
- Keep unresolved items in each project's `## MAGGIE TODO` section so the dashboard can surface them cleanly.
