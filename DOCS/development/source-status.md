---
title: Skill and plugin source status
description: Source comparison and public release preparation for the curated Codex skills suite.
status: in-review
lastUpdated: "2026-09-09 13:18 ET (America/New_York)"
owner: Maggie Lerman
---

# Skill and plugin source status

## Source comparison

This audit compared the curated repository against the current Mac's installed standalone skills and custom plugin packages. It did not inspect a second workstation, adopt newer upstream packages wholesale, or treat installed caches as the source of truth.

| Source | Finding | Resolution |
| --- | --- | --- |
| RPS Print Order | Five changed files and a new print-submission reference | Reconciled all six files from the current installed skill. |
| Context Layer | Installed custom package matches the repository byte for byte | Retained the repository package. |
| RPS Etsy Ops | Installed custom package matches the repository byte for byte | Retained the repository package; reconciled the older standalone Shop Uploader copy and bundled its repository-resolution reference. |
| Motion Design Director and Working Modes | Installed custom packages match the repository byte for byte | Retained the repository packages. |
| Design System First, JAMstack Expert, Project Tranche Orchestrator | No matching installed custom package on this Mac | Preserved repository sources; local runtime parity is unverified. |
| Other curated standalone skills | The old sync preflight cannot find 47 allowlisted sources in the two standalone skill directories | Preserved the curated sources. Many capabilities now live in plugins; absence is not a deletion instruction. |

## RPS changes

Print manifests now carry Shopify-derived orientation and expected 300-ppi dimensions. Current Creative Cloud PSDCs remain the production source. Every print submission checks document identity, canvas size, orientation, preview, printer, paper, quality, and copies; clipping or unexpected scaling stops submission. New or modified artwork completes a single SKU through saved cloud document, proof, held remainder, and queue readback before the next SKU. These are instruction updates; this audit did not submit print jobs or validate physical output.

## Portability and public presentation

Removed workstation-specific command paths from Shopify App Scaffold, User Journey Audit, UX/UI Bug Intake, Visual Design Critique, the worktree helper example, and the standalone Shop Uploader workflow. Updated contribution wording to match a publicly viewable repository with optional support. Existing upstream notices remain intact; no public open-source license was added.

## Maintenance boundaries

- Run the standalone sync script in `--check` mode first. Review every proposed copy and every missing source.
- Compare only custom plugin packages tracked in this repository; do not mirror bundled or curated upstream plugins.
- Keep standalone skill references inside the skill folder. Plugin-relative references cannot be copied unchanged into standalone packages.
- Preserve older Git history and branches. Historical audit files describe their original dates and are not current quality scores or current installation inventories.
- Regenerate both catalogs after source changes. Run the repository tests, catalog check, documentation-link check, and docs-site build before publishing updates.

## Validation

- All 11 repository unit tests passed, including portability and RPS package-reference parity checks.
- Suite drift check and documentation-link check passed.
- Public docs-site lint and production build passed; the build generated 71 routes.
- The reconciled RPS Print Order folder matches the current installed source byte for byte.
- A pattern scan reviewed 1,376 historical Git blob versions across fetched refs. No recognizable credential formats were found; three assignment-pattern matches were documentation placeholders. Compressed Shopify assets were GraphQL schemas, and the packaged PDF and slide text contained audit/example material. This is a bounded release review, not a guarantee that every historical artifact is free of sensitive content.
- Historical branches retain workstation paths and operational setup notes. No history was rewritten or branches removed.
