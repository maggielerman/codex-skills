---
name: context-layer-scaffold
description: "Use when asked to scaffold or repair Context Layer repos: canonical DOCS root, project lifecycle, evidence, dashboard, checkpoints, AGENTS/ROADMAP/CHANGELOG, optional content calendar, docs site, product docs, UX bugs, or review board."
---

# Context Layer Scaffold

Create or standardize a repo-native context layer for human-agent teams. This is the setup skill: it installs the shared docs, project state, governance, evidence, dashboard, and workflow memory that later trigger skills can use.

Do not edit the legacy `product-operating-system-scaffold` skill when working from this draft package.

## Non-Negotiables

- Canonical docs root is always `DOCS/`.
- Existing `docs/` or `documentation/` roots are migration sources, not canonical destinations.
- Use safe-write behavior: create missing files, append or patch missing sections, and stop before overwriting user content.
- Generate timestamps with `node scripts/docs/timestamp-et.mjs --json`; do not hand-type timestamps.
- Keep repo-level `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md` at the repository root.
- Maintain lifecycle folders: `active/`, `in-review/`, `blocked/`, `completed/`, `backlog/`, `stale/`.
- Keep the reusable project template at `DOCS/PROJECTS/NNNN_project_template.md`, not inside a lifecycle folder.
- Install the HTML project dashboard as part of the required baseline.
- Use literal `MAGGIE TODO:` callouts for Maggie-owned manual work, approvals, evidence gathering, manual testing, external dependencies, or missing input.
- Require a visual design critique checkpoint for significant user-facing UI before implementation sign-off or movement to `in-review/`.

## Required Decision Gates

Before writing files, ask only for optional modules that are not part of the required baseline:

1. Do you want a docs site scaffolded now (`yes`/`no`)?
2. Do you want product docs pack scaffolding included (`yes`/`no`)?
3. Do you want UX/UI bug intake scaffolding included (`yes`/`no`)?
4. Do you want the optional content calendar scaffold included for repo-side publishing cadence, review status, and content queue planning (`yes`/`no`)?
5. Do you want the optional Review Board Operating Pattern scaffold included for visual comparison, evidence review, and numbered human corrections (`yes`/`no`)?

Defaults when unspecified:

- docs site: `no`
- product docs pack: `no`
- UX/UI bug intake: `no`
- content calendar: `no`
- Review Board Operating Pattern scaffold: `no`

If invoked through a product-docs compatibility skill, force product docs pack to `yes`.

## Reference Map

Read only the references needed for the current run:

- Baseline scaffold: `references/baseline-scaffold.md`
- Governance, lifecycle, and checkpoint policy: `references/governance-and-lifecycle.md`
- Parent projects, subprojects, and supporting docs: `references/project-hierarchy.md`
- Required project dashboard: `references/project-dashboard.md`
- Evidence system: `references/evidence-system.md`
- `MAGGIE TODO` callouts: `references/maggie-todos.md`
- Optional Review Board Operating Pattern: `references/review-board.md`
- Optional UX/UI bug intake: `references/ux-ui-bug-intake.md`
- Optional docs site: `references/docs-site.md`
- Optional product docs pack: `references/product-docs.md`
- Migration from old scaffold/docs roots: `references/migrations.md`
- Verification checklist: `references/verification.md`

## Baseline Workflow

1. Inspect the repo for existing docs roots, governance files, package infrastructure, agent instruction files, project docs, evidence roots, dashboard files, and review-board signals.
2. Ask the required decision gates, including a recommendation for Review Board Operating Pattern based on repo signals.
3. Generate an Eastern Time timestamp using the bundled timestamp script.
4. Standardize the docs root to `DOCS/`; migrate or safely reference old `docs/` or `documentation/` content according to `references/migrations.md`.
5. Scaffold the baseline docs root from `assets/templates/docs-root/`.
6. Create or update governance docs from `assets/templates/governance/`.
7. Copy docs tooling scripts from `assets/scripts/scripts/docs/` into `scripts/docs/`.
8. Add package scripts when `package.json` exists and the repo can support them.
9. Install and generate the project dashboard.
10. Install optional docs site, product docs, UX/UI bug intake, content calendar, and review-board scaffolds only when selected.
11. Run verification from `references/verification.md` and report created, updated, skipped, blocked, and manually gated items.

## Required Assets

Baseline templates:

- `assets/templates/docs-root/`
- `assets/templates/governance/`
- `assets/templates/workflows/docs-site-sync.yml`

Required docs scripts:

- `assets/scripts/scripts/docs/manifest.mjs`
- `assets/scripts/scripts/docs/check-links.mjs`
- `assets/scripts/scripts/docs/normalize-frontmatter.mjs`
- `assets/scripts/scripts/docs/timestamp-et.mjs`

Required dashboard installer:

- `${CODEX_HOME:-$HOME/.codex}/skills/context-layer-dashboard-backfill/scripts/install_docs_project_dashboard.py`

Optional assets:

- Product docs: `assets/templates/product-docs/product-doc-templates.md`
- UX/UI bug intake: `assets/templates/ux-ui-bugs/`
- Review-board workflow: `assets/templates/review-board-operating-pattern/`
- Docs site: `assets/vitepress/`
- Content calendar: installed through the required dashboard installer with `--with-content-calendar`

## Safe-Write Rules

- Never replace an existing non-generated file wholesale without explicit approval.
- If a file exists, add missing sections or append guidance with clear headings.
- If multiple existing docs roots contain unique user content, stop and summarize migration choices before moving content.
- If a generated dashboard exists, it may be regenerated.
- If a non-generated `DOCS/PROJECTS/dashboard.html` exists, stop and ask before replacing it.
- If old `docs/` or `documentation/` roots exist, do not delete them without explicit approval.

## Verification Summary

Before finishing, verify:

- `DOCS/` exists and is the canonical docs root.
- Required docs-root files and folders exist.
- `DOCS/PROJECTS/NNNN_project_template.md` exists at the `PROJECTS/` root.
- Lifecycle folders exist and contain only real project docs.
- Evidence folders exist.
- Governance files exist and reference `DOCS/`.
- Docs scripts exist.
- Dashboard generator exists and `DOCS/PROJECTS/dashboard.html` is generated.
- Package scripts and CI behavior match the repo's package infrastructure.
- Optional modules selected by the user are installed and linked.
- Manifest generation succeeds when package/script prerequisites are present.
