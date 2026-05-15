---
name: review-board
description: Use when asked to create, update, review, or apply feedback from a numbered review board, visual screenshot board, evidence board, or correction board.
---

# Review Board

Use this skill for Maggie's repo-native review-board workflow. A review board is a numbered visual/evidence packet with manifests, human feedback, an apply pass, and verification.

## First Checks

1. Locate `DOCS/`.
2. Look for `DOCS/development/review-board-operating-pattern.md`.
3. Look for `DOCS/evidence/templates/review-board-operating-pattern/`.

If those docs are missing, tell the user the repo does not appear to have the Review Board Operating Pattern installed and offer to run `$context-layer-scaffold` or install the review-board scaffold.

## Workflow

When installed, follow `DOCS/development/review-board-operating-pattern.md`.

Default loop:

1. Open or update a numbered project doc for the review stream.
2. Define review target, source rules, and success criteria.
3. Generate numbered JPG boards.
4. Optionally generate a PDF bundle.
5. Produce `manifest.json`, `manifest.csv`, and `index.md`.
6. Collect numbered human feedback.
7. Convert feedback into a bounded apply plan.
8. Apply changes only within the approved scope.
9. Verify touched records, screens, docs, or artifacts.
10. Record checkpoints and evidence paths.

## Evidence

Temporary packets may be deleted when done. If preserving a packet, store it under:

`DOCS/evidence/active/<project-id>/review-packets/<run-name>/`

Do not invent repo-specific business rules. Keep taxonomy, accessibility, product, catalog, metadata, and mutation rules in the repo docs/code.
