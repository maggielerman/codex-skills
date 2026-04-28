---
title: PRD
description: MVP requirements for Codex Skills Packs customer docs and sales surface
status: evolving
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Product/Engineering
---

# PRD: Codex Skills Packs customer docs MVP

## Goals
- Provide a customer-facing marketing page for the skills packs.
- Provide setup and troubleshooting docs for purchasers.
- Generate per-skill and per-plugin docs from source metadata.
- Keep customer docs separate from repo maintenance docs.

## Non-goals
- Public license drafting.
- Payment processing.
- Full knowledge-base authoring for every advanced workflow edge case.

## Requirements

### Must-have
- Next.js/Tailwind/shadcn docs site in `docs-site/`.
- Generated customer catalog from `skills/manifest.json` and `plugins/*/.codex-plugin/plugin.json`.
- Repo-native `DOCS/` operating scaffold with `PROJECTS/`, evidence, product docs, and docs tooling.
- Repeatable drift checks for skill catalog membership and metadata.

### Nice-to-have
- Search/filtering across skill and plugin docs.
- Purchase flow and private customer download area.
- Screenshots or walkthrough videos for installation.

## Constraints
- Do not present repo maintenance docs as customer implementation docs.
- Do not publish open-source licensing language unless explicitly approved.
- Preserve skill portability and bundled provenance files.

## MAGGIE TODO

- MAGGIE TODO: Define the customer support promise and refund/update policy.
