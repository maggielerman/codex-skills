# Modes And Add-ons

## Starter modes

### `marketing-only`

Use this when the user wants a branded landing page, campaign page, or brochure-style marketing shell.

Expected outcome:
- one strong poster-like first viewport
- bold typography and visible design tokens
- a small number of sections with clear jobs
- shadcn components used as foundations, not as a card-grid aesthetic

### `app-shell`

Use this when the user wants a product workspace, dashboard shell, or operational interface.

Expected outcome:
- one primary workspace
- one supporting rail or sidebar
- calm, restrained hierarchy
- starter metrics, queue, and workspace sections instead of generic dashboard mosaics

## Add-ons

### `docs`

This add-on should provide a docs-root baseline, not a full docs site.

Expected outcome:
- `DOCS/` root with lifecycle folders and baseline docs
- root governance files such as `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md`
- docs helper scripts under `scripts/docs/`
- package scripts for docs manifest, links, frontmatter normalization, and timestamps

If the user wants a docs site, product docs pack, or governance expansion beyond that baseline, follow with `$ML-docs-system-scaffold`.

### `testing`

This add-on should provide just enough coverage to verify the starter:
- Vitest for a simple component/unit test
- Playwright for a home-page smoke path
- package scripts that make both easy to run

Do not overbuild testing in v1. The goal is confidence that the starter boots and renders, not a large QA harness.
