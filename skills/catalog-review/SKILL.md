---
name: catalog-review
description: Custom skill created by Maggie Lerman. Standard Shopify-first catalog review workflow for opening a numbered project, choosing the right numbered review-packet shape (static JPG/PDF boards, hosted-image HTML pages, or interactive decision-capture surfaces), collecting human corrections or saved decisions, and translating that feedback into apply/verify passes with evidence artifacts. Use when asked to create catalog review pages, set up a catalog cleanup project, review missing colors/orientations/subjects, prepare a merchandising review packet, or apply catalog review corrections.
---

# Catalog Review

Custom skill created by Maggie Lerman.

Use this skill when catalog cleanup should be driven by a human-reviewed packet rather than by pure automation.

This skill is Shopify-first and intentionally process-heavy rather than framework-heavy.

## Start Here

If the repo already has `DOCS/development/catalog-review-workflow.md` or `docs/development/catalog-review-workflow.md`, use that file as the local source of truth first.

If the repo has a docs project system, open a numbered project doc and treat the work as a project stream, not a one-off utility task.

If the repo also has a docs-root evidence system such as `DOCS/evidence/templates/catalog-review/` or `docs/evidence/templates/catalog-review/`, treat that directory as the durable home for review-session templates and conventions.

If the repo does not yet have a docs system or catalog-review scaffold, follow the workflow below directly.

## When This Workflow Fits

Use catalog review for:

- color cleanup
- orientation cleanup
- subject or theme review
- missing-attribute review
- merchandising cleanup where visual judgment matters
- later featured-image and image-normalization review

Do not over-abstract repo-specific business rules into this skill.
Keep local taxonomy, collection logic, and metafield rules in the repo.

## Standard Workflow

1. Define the review target.
2. Define the source selector or buckets.
3. Choose the review-packet shape that fits the work.
4. Ask whether the review packet should include all images for each product or only the first image when image inclusion is not already defined. Default to the first image if the user does not choose.
5. Generate the numbered review packet.
6. Emit the shared apply/verify artifacts: `manifest.json`, `manifest.csv`, and `index.md`.
7. Emit shape-specific artifacts such as numbered JPG pages, an optional PDF bundle, a numbered HTML review page, or `requests.csv` for interactive decision-capture runs.
8. Collect numbered human corrections or saved/exported interactive decisions.
9. Normalize corrections into a bounded apply plan.
10. Apply changes.
11. Verify the touched records.
12. Record checkpoints and evidence artifact paths in the project doc.
13. Delete the temporary review packet unless the user explicitly wants it kept or archived.

## Standard Packet Shapes

Choose one packet shape at the start of a review stream and record that choice in the project doc or packet `index.md`.

### Static JPG / PDF Boards

Use this for bounded visual-review sets, printable review, simple approve / reject / revise decisions, and markup where screenshots or PDF annotation are the natural review surface.

Standard artifacts:

- numbered JPG pages
- optional combined PDF bundle
- `manifest.json`
- `manifest.csv`
- `index.md`

### Hosted-Image HTML Page

Use this for larger Shopify-first review packets where images should load from live hosted Shopify CDN URLs instead of being downloaded into the packet. Prefer this shape when the reviewer needs a browser page but not persistent in-page decision controls.

Standard artifacts:

- numbered HTML review page
- `manifest.json`
- `manifest.csv`
- `index.md`

### Interactive Decision-Capture Surface

Use this for complex markup, multi-filter review, per-image actions such as change, delete, crop whitespace, and order changes, saved local decisions, and agent handoff. In repos that provide an internal review route or app surface, prefer this shape when the reviewer needs to capture structured decisions rather than just read a packet.

Standard artifacts:

- interactive route or app surface
- `manifest.json`
- `manifest.csv`
- `requests.csv`
- `index.md`

## Standard Artifact Contract

Every review packet should include:

- `manifest.json`
- `manifest.csv`
- `index.md`

The manifest is the source of truth for later apply/verify work.

The review surface depends on the selected packet shape: numbered JPG pages, an optional PDF bundle, a numbered HTML page, or an interactive route/app surface.

Hosted-image HTML pages and interactive decision-capture surfaces should render product images from the live hosted image URLs returned by Shopify or the repo's product source. Do not download or copy all product images into those packets by default. If the user explicitly requests a self-contained archive or offline review packet, record that exception in `index.md` and preserve both the hosted URL and any local copy path in the manifest.

Static JPG / PDF boards may include locally rendered image assets because their purpose is a portable visual review artifact. Still preserve source image URLs in the manifest whenever available.

Each product entry should have a stable review number that appears in the review surface and both manifest files. Include enough product metadata for review without needing to open Shopify: product title, handle, product ID or GID when available, current bucket or selector context, relevant tags/metafields under review, image count included, and source image URLs.

## Human Feedback Contract

- numbered correction notes in chat or markdown are authoritative
- annotated screenshots or browser notes are supporting context only
- saved/exported interactive decisions are authoritative when the project doc names the interactive manifest as the review input
- if visual annotations and numbered notes disagree, resolve the conflict explicitly before applying changes
- if saved interactive decisions and separate written notes disagree, resolve the conflict explicitly before applying changes

## Shopify-First Guidance

Prefer these source selectors:

- collection handle
- product query
- explicit product-handle list

Prefer the first product image by default unless the user asks to include all images or the repo’s local workflow says otherwise.

When asking about image inclusion, use a direct question:

`Should the review packet include all images for each product, or just the first image?`

If all images are included, keep each product grouped under one review number unless the local workflow specifically needs per-image decisions. If the review needs per-image decisions, make the sub-numbering explicit, such as `12.1`, `12.2`, and `12.3`.

Common mutation outputs include:

- add/remove tags
- set/clear metafields
- move products between review buckets
- write orientation/color/subject decisions
- set boolean merchandising flags

## Project And Packet Expectations

A catalog-review project should record:

- review target
- source or bucket definition
- selected packet shape
- image inclusion choice: all product images or first image only
- generated board/page/surface packet
- feedback packet reviewed
- apply audit paths
- verify audit paths
- live counts or outcome summaries
- next checkpoint targets

Keep the project doc lightweight.
Use a repo's generic project template for the project doc itself, and keep review-page-specific scaffolding under the docs root's `evidence/templates/catalog-review/` area when the repo has one.

## Cleanup Rule

Generated review packets are disposable by default.

After apply + verify + project-doc checkpointing are complete, delete the run packet unless the user explicitly asks to keep or archive it. If it is intentionally preserved, store it under the owning project's evidence directory under `review-packets/<run-name>/` rather than a separate durable temp root.

## Prompt Examples

- `Create a catalog review packet for all products that do not have a color set.`
- `Set up a catalog cleanup project and choose the best review packet shape for portrait/landscape mismatches.`
- `Prepare a merchandising review page for this collection using all product images.`
- `Use the interactive catalog-review surface for image order and delete/change requests.`
- `Apply the numbered catalog review corrections and verify the touched products.`
