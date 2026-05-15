---
name: review-board-operating-pattern
description: Repo-agnostic visual review-board operating pattern for opening a numbered project, generating numbered JPG review boards with optional PDF bundles, collecting human corrections, and translating that feedback into bounded apply/verify passes with evidence artifacts. Use when asked to create review boards, compare visual options, audit UI/screenshots/content/assets, prepare a human review packet, or apply numbered review corrections.
---

# Review Board Operating Pattern

Use this skill when work should be driven by a human-reviewed visual packet rather than by blind automation.

The workflow is repo-agnostic. It works for UI states, design concepts, content inventories, screenshots, datasets with visual evidence, image libraries, research artifacts, ecommerce catalogs, or any situation where a person needs to compare and correct numbered items.

## Start Here

If the repo already has `DOCS/development/review-board-operating-pattern.md` or `docs/development/review-board-operating-pattern.md`, use that file as the local source of truth first.

If the repo has a docs project system, open a numbered project doc and treat the work as a project stream, not a one-off utility task.

If the repo also has a docs-root evidence system such as `DOCS/evidence/templates/review-board-operating-pattern/` or `docs/evidence/templates/review-board-operating-pattern/`, treat that directory as the durable home for review-session templates and conventions.

If the repo does not yet have a docs system or review-board scaffold, follow the workflow below directly.

## When This Workflow Fits

Use review boards for:

- comparing design concepts or UI states
- route, dashboard, or screenshot audits where visual review matters
- content, taxonomy, or metadata cleanup
- image quality, orientation, color, subject, or theme review
- research or evidence packets that need numbered human feedback
- ecommerce catalog and merchandising cleanup
- any review pass where visual judgment is the source of truth

Do not encode repo-specific business rules into this skill.
Keep local taxonomy, data ownership, mutation rules, accessibility criteria, design standards, or product-specific logic in the repo.

## Standard Workflow

1. Define the review target.
2. Define the source selector, bucket, route list, artifact list, or comparison set.
3. Generate numbered JPG review boards.
4. Optionally bundle the JPGs into a PDF for easier markup.
5. Emit `manifest.json`, `manifest.csv`, and `index.md`.
6. Collect numbered human corrections.
7. Normalize corrections into a bounded apply plan.
8. Apply changes or record accepted decisions.
9. Verify the touched records, screens, docs, or artifacts.
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
- if feedback introduces new criteria, update the apply plan before touching source data or code

## Domain Guidance

Prefer source selectors that are explicit and reproducible:

- route list, viewport list, or screenshot directory
- design concept set or asset manifest
- collection handle, product query, or product-handle list
- document set, content inventory, or metadata export
- manually supplied item list

Common outputs include:

- UI or visual design changes
- content, metadata, taxonomy, or tagging changes
- image normalization or asset-selection decisions
- accessibility, responsive, or route-quality fixes
- evidence classification or archive decisions
- ecommerce catalog corrections

## Project And Review-Board Expectations

A review-board project should record:

- review target
- source or bucket definition
- generated board packet
- feedback packet reviewed
- apply audit paths
- verify audit paths
- outcome summaries or changed-item counts
- next checkpoint targets

Keep the project doc lightweight.
Use a repo's generic project template for the project doc itself, and keep review-board-specific scaffolding under the docs root's `evidence/templates/review-board-operating-pattern/` area when the repo has one.

## Cleanup Rule

Generated review packets are disposable by default.

After apply + verify + project-doc checkpointing are complete, delete the run packet unless the user explicitly asks to keep or archive it. If it is intentionally preserved, store it under the owning project's evidence directory under `review-packets/<run-name>/` rather than a separate durable temp root.

## Prompt Examples

- `Create a review board comparing these three homepage concepts.`
- `Generate review boards for the dashboard routes and collect UI corrections.`
- `Prepare a visual evidence packet for the screenshots in this audit folder.`
- `Create a review board for all product images that need visual classification.`
- `Apply the numbered review-board corrections and verify the touched items.`
