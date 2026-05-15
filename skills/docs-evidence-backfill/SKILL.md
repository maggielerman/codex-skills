---
name: docs-evidence-backfill
author: Maggie Lerman
description: Retrofit an existing repository from fragmented audit and artifact storage into a unified docs evidence system. Use when an existing repo has evidence spread across places like docs assets, review-board folders, repo-root artifacts, tmp folders, or legacy generated outputs and needs a canonical docs-root evidence structure such as `DOCS/evidence/` or `docs/evidence/` plus path/reference cleanup.
---

# Docs Evidence Backfill

Use this skill to retrofit an existing repo onto a unified evidence system.

Treat the repository's configured docs root (`DOCS/`, `docs/`, or equivalent) as the source of truth. The examples below use `{{DOCS_ROOT}}` to mean that root.

## Start Here

Before editing, inventory where the repo currently stores:

- audits and baseline packets
- review packets and review templates
- screenshots, exports, and manual evidence
- visual comparison boards, decision packets, and correction manifests
- repo-root `artifacts/` or `tmp/` output
- script defaults that still emit to old paths
- durable artifacts that embed absolute machine-specific paths

If the repo is greenfield or early-stage and does not already have evidence drift, use `$product-operating-system-scaffold` instead.

## Target Model

Use this canonical layout:

- `{{DOCS_ROOT}}/development/`
  - process docs only
- `{{DOCS_ROOT}}/evidence/active/`
  - current durable evidence
- `{{DOCS_ROOT}}/evidence/archive/`
  - historical evidence
- `{{DOCS_ROOT}}/evidence/templates/`
  - reusable packet shells and review templates

Prefer project-scoped organization under each bucket.

## Migration Workflow

1. Inventory current evidence locations.
2. Classify files into:
   - `active`
   - `archive`
   - `templates`
   - delete
3. Create the `{{DOCS_ROOT}}/evidence/` root if it does not exist.
4. Move durable evidence into the canonical structure.
5. Move review templates into `{{DOCS_ROOT}}/evidence/templates/`.
6. Update docs references and script defaults that still point at old evidence paths.
7. Rewrite non-portable path references where reasonable.
8. Delete true scratch and cache material.
9. Rebuild docs-generated surfaces and verify links.

## Known Drift Patterns To Handle

- `{{DOCS_ROOT}}/assets/audits/`
- `{{DOCS_ROOT}}/review-boards/`
- repo-root `artifacts/`
- repo-root `tmp/`
- `tmp/review-boards/`
- `tmp/pdfs/`
- `output/playwright/`-style evidence references
- JSON/MD/TXT artifacts with stale worktree-specific absolute paths

## Classification Rules

- Reusable structure belongs in `templates`.
- Live proof for active, blocked, or in-review work belongs in `active`.
- Older but still useful proof belongs in `archive`.
- True caches, downloads, and scratch files should be deleted rather than preserved in a fake durable temp area.

## Review Board Evidence Rule

- Store reusable review-board scaffolding in `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/`.
- Treat review boards as repo-agnostic visual evidence packets, not ecommerce-only artifacts.
- If a review packet is intentionally kept, store it in the owning project's evidence directory under `review-packets/`.
- Do not keep a separate durable review-board temp root.

## Validation

After migration, verify:

- repo docs point to `{{DOCS_ROOT}}/evidence/`
- script defaults no longer point to retired evidence locations
- `pnpm docs:links`
- `pnpm docs:manifest`
- `pnpm docs:projects-dashboard`
- `git diff --check`
