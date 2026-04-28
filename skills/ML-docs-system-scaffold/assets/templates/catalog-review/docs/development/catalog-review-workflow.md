---
title: Catalog Review Workflow
description: Standard operating pattern for numbered catalog review boards and collaborative cleanup passes
status: evolving
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# Catalog Review Workflow

Use this workflow for collaborative catalog optimization where a human needs to review a visual packet and hand back precise corrections.

## When to Use This Workflow

Use catalog review when the work is better handled through numbered review boards than through blind automation, including:

- color cleanup
- orientation cleanup
- subject or theme assignment review
- missing-attribute review
- featured-image or image-normalization review
- other merchandising passes where human visual judgment is the source of truth

## Standard Loop

1. Open a numbered project doc for the review stream.
2. Define the review target and the bucket/source rules.
3. Generate numbered JPG review boards.
4. Optionally generate a combined PDF bundle for easier markup.
5. Collect numbered human feedback.
6. Convert feedback into a bounded apply pass.
7. Verify the touched records.
8. Record checkpoints plus evidence artifacts in the project doc, `ROADMAP.md`, and `CHANGELOG.md`.
9. Delete the temporary review packet when the session is complete unless the user explicitly asks to keep it.

## Standard Artifacts

Every ML-catalog-review run should produce:

- numbered JPG pages
- optional combined PDF bundle
- `manifest.json`
- `manifest.csv`
- `index.md`

Use the manifest as the source of truth for later apply/verify work.

## Human Feedback Contract

- numbered correction notes in chat or markdown are authoritative
- annotated PDFs are useful supporting context, but not the source of truth
- if both exist and conflict, normalize the conflict explicitly before applying changes

## Project And Review-Board Expectations

Keep the project doc lightweight and use it to capture:

- review target
- source or bucket definition
- board packet location
- feedback packet reviewed
- apply audit paths
- verification audit paths
- current live counts or outcome summaries
- next checkpoint targets

Keep review-board-specific templates and conventions in a dedicated `{{DOCS_ROOT}}/evidence/templates/ML-catalog-review/` area rather than in project-template folders.

If a review packet is intentionally preserved, store it under the owning project's evidence directory under `{{DOCS_ROOT}}/evidence/{active|archive}/<project>/review-packets/<run-name>/`.

## Repo-Specific Rules Stay Local

Do not treat the scaffold as the source of truth for repo-specific business rules.

Keep local rules in repo docs/code for things like:

- color taxonomy
- subject collection definitions
- metafield ownership and mapping
- destination collection logic
- featured-image or image-role policies

## Starter Prompt Examples

- `I want to do some catalog optimization work. Create a review board for all products that do not have a color set.`
- `Open a new ML-catalog-review project and generate boards for products missing orientation.`
- `Prepare a catalog review packet for the Blue collection and include a PDF bundle.`
