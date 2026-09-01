# RPS Etsy Ops Repo Map

This plugin is a workflow/router layer. It does not own live catalog state,
project evidence, reusable media assets, or upload artifacts.

Resolve every named repository on the current host using
`repository-resolution.md`.

## Canonical Repos

- `rps-etsy`
  - Etsy catalog operations source of truth.
  - Owns Shop Uploader exports, apply plans, generated CSV/XLSX files, upload reports, evidence packets, mockup availability rows, visual indexes, and project checkpoints.
- Google Drive `RPS Creative Assets` plus the catalog sheet
  - Reusable creative asset source of truth.
  - Owns approved mockup binaries, evergreen blank bases, informational media assets, review boards, and Drive file/folder IDs.
  - Google Drive for desktop may provide an optional local cache, but native desktop paths are not durable automation references.
- `rps-creative-assets`
  - Read-only migration archive and optional local cache.
  - Does not own new active reusable asset work.
- `shopify-headless`
  - Optional future readiness surface.
  - Reference only when Shopify publishing, CDN hosting, product media mapping, or headless storefront readiness is explicitly in scope.

## Non-Goals

- Do not store upload-ready Shop Uploader files in this plugin.
- Do not store project evidence or review boards in this plugin.
- Do not store approved reusable mockup assets in this plugin.
- Do not create new active assets in the archived `rps-creative-assets` repo.
- Do not use this plugin as a replacement for current repo docs.
