# RPS Etsy Ops Repo Map

This plugin is a workflow/router layer. It does not own live catalog state,
project evidence, reusable media assets, or upload artifacts.

## Canonical Repos

- `/Users/maggielerman/Github/rps-etsy`
  - Etsy catalog operations source of truth.
  - Owns Shop Uploader exports, apply plans, generated CSV/XLSX files, upload reports, evidence packets, mockup availability rows, visual indexes, and project checkpoints.
- `/Users/maggielerman/Github/rps-creative-assets`
  - Reusable creative asset source of truth.
  - Owns approved mockup packs, evergreen blank bases, informational media assets, manifests, and asset library indexes.
- `/Users/maggielerman/Github/shopify-headless`
  - Optional future readiness surface.
  - Reference only when Shopify publishing, CDN hosting, product media mapping, or headless storefront readiness is explicitly in scope.

## Non-Goals

- Do not store upload-ready Shop Uploader files in this plugin.
- Do not store project evidence or review boards in this plugin.
- Do not store approved reusable mockup assets in this plugin.
- Do not use this plugin as a replacement for current repo docs.
