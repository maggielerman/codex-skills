---
name: catalog-review
description: Custom skill created by Maggie Lerman. Standard Shopify-first catalog review workflow for opening a numbered project, generating numbered JPG review boards with optional PDF bundles, collecting human corrections, and translating that feedback into apply/verify passes with evidence artifacts. Use when asked to create catalog review boards, set up a catalog cleanup project, review missing colors/orientations/subjects, prepare a merchandising review packet, or apply catalog review corrections.
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
3. Generate numbered JPG review boards.
4. Optionally bundle the JPGs into a PDF for easier markup.
5. Emit `manifest.json`, `manifest.csv`, and `index.md`.
6. Collect numbered human corrections.
7. Normalize corrections into a bounded apply plan.
8. Apply changes.
9. Verify the touched records.
10. Record checkpoints and evidence artifact paths in the project doc.
11. Delete the temporary review packet unless the user explicitly wants it kept or archived.

## Standard Artifact Contract

Every review packet should include:

- numbered JPG pages
- optional combined PDF bundle
- `manifest.json`
- `manifest.csv`
- `index.md`

The manifest is the source of truth for later apply/verify work.

## Human Feedback Contract

- numbered correction notes in chat or markdown are authoritative
- annotated PDFs are supporting context only
- if the PDF and numbered notes disagree, resolve the conflict explicitly before applying changes

## Shopify-First Guidance

Prefer these source selectors:

- collection handle
- product query
- explicit product-handle list

Prefer featured images by default unless the repo’s local workflow says otherwise.

Common mutation outputs include:

- add/remove tags
- set/clear metafields
- move products between review buckets
- write orientation/color/subject decisions
- set boolean merchandising flags

## Project And Review-Board Expectations

A catalog-review project should record:

- review target
- source or bucket definition
- generated board packet
- feedback packet reviewed
- apply audit paths
- verify audit paths
- live counts or outcome summaries
- next checkpoint targets

Keep the project doc lightweight.
Use a repo's generic project template for the project doc itself, and keep review-board-specific scaffolding under the docs root's `evidence/templates/catalog-review/` area when the repo has one.

## Cleanup Rule

Generated review packets are disposable by default.

After apply + verify + project-doc checkpointing are complete, delete the run packet unless the user explicitly asks to keep or archive it. If it is intentionally preserved, store it under the owning project's evidence directory under `review-packets/<run-name>/` rather than a separate durable temp root.

## Prompt Examples

- `Create a catalog review board for all products that do not have a color set.`
- `Set up a catalog cleanup project and generate review boards for portrait/landscape mismatches.`
- `Prepare a merchandising review packet for this collection and include a PDF bundle.`
- `Apply the numbered catalog review corrections and verify the touched products.`
