---
title: Review Board Operating Pattern
description: Standard operating pattern for numbered visual review boards, evidence packets, and collaborative cleanup passes
status: evolving
lastUpdated: "{{LAST_UPDATED_TS_ET}}"
owner: Product/Engineering
---

# Review Board Operating Pattern

Use this workflow when a human needs to compare visual evidence, review numbered items, and hand back precise corrections before an apply/verify pass.

The pattern is repo-agnostic. It can support UI review, design selection, screenshot audits, content review, image classification, product catalog work, evidence triage, or any compare/contrast task where human visual judgment is the source of truth.

## When to Use This Workflow

Use review boards when the work is better handled through numbered visual packets than through blind automation, including:

- design concept comparison
- UI route, dashboard, responsive, or screenshot audits
- evidence packets that need human review
- content, metadata, or taxonomy cleanup
- image quality, orientation, color, subject, or theme assignment
- ecommerce catalog and merchandising passes
- any compare/contrast review where human visual judgment is the source of truth

## Standard Loop

1. Open a numbered project doc for the review stream.
2. Define the review target and the bucket/source rules.
3. Generate numbered JPG review boards.
4. Optionally generate a combined PDF bundle for easier markup.
5. Collect numbered human feedback.
6. Convert feedback into a bounded apply pass.
7. Verify the touched records, screens, docs, or artifacts.
8. Record checkpoints plus evidence artifacts in the project doc, `ROADMAP.md`, and `CHANGELOG.md`.
9. Delete the temporary review packet when the session is complete unless the user explicitly asks to keep it.

## Standard Artifacts

Every review-board run should produce:

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
- if feedback introduces new criteria, update the apply plan before touching source data or code

## Project And Review-Board Expectations

Keep the project doc lightweight and use it to capture:

- review target
- source or bucket definition
- board packet location
- feedback packet reviewed
- apply audit paths
- verification audit paths
- current outcome summaries or changed-item counts
- next checkpoint targets

Keep review-board-specific templates and conventions in a dedicated `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/` area rather than in project-template folders.

If a review packet is intentionally preserved, store it under the owning project's evidence directory under `{{DOCS_ROOT}}/evidence/{active|archive}/<project>/review-packets/<run-name>/`.

## Repo-Specific Rules Stay Local

Do not treat the scaffold as the source of truth for repo-specific business rules.

Keep local rules in repo docs/code for things like:

- visual quality criteria
- accessibility or responsive standards
- content taxonomy or metadata ownership
- product, collection, or catalog business rules
- image role policies
- apply-pass permissions and mutation boundaries

## Starter Prompt Examples

- `Create a review board comparing these homepage concepts.`
- `Generate review boards for the dashboard route screenshots.`
- `Prepare a visual evidence packet for this audit folder and include a PDF bundle.`
- `Open a new review-board project and generate boards for products missing orientation.`
