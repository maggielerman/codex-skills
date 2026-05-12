---
name: ML-product-operating-system-scaffold
description: Scaffold or standardize a comprehensive repo-native product operating system for human-agent teams. Installs the docs root, project lifecycle model, governance files, agent instructions, ROADMAP/CHANGELOG control plane, evidence system, docs automation scripts, timestamp/checkpoint rules, visual design critique gates, optional VitePress docs site, optional product-doc pack, optional PROJECTS dashboard, and optional repo-agnostic review-board workflow. Use when asked for product operating system setup, repo-native product management, agent-readable project memory, lifecycle/governance scaffolding, evidence-system setup, docs-site setup, product docs, project dashboards, visual/design quality gates, or review-board scaffolding.
---

# Product Operating System Scaffold

## Overview
Create or standardize a comprehensive repo-native product operating system with safe-write behavior. This is not just documentation scaffolding. It turns a repository into the shared operating layer for product intent, project state, agent instructions, evidence, checkpoints, review, and launch memory.

This skill combines:
- docs root and information architecture scaffolding,
- project lifecycle and status-lane scaffolding,
- repo-level governance via `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md`,
- agent-readable project memory under `PROJECTS/`,
- evidence-system scaffolding,
- docs automation tooling (`manifest`, `links`, `frontmatter`, timestamps),
- checkpoint, timestamp, and manual-work forcing mechanisms,
- visual design critique gates for user-facing UI work,
- optional docs site scaffolding,
- optional lightweight product-doc pack scaffolding,
- optional HTML project dashboard scaffolding,
- optional Review Board Operating Pattern scaffolding.

Default project lifecycle states created/enforced by the operating system:
- `active`
- `in-review`
- `blocked`
- `completed`
- `backlog`
- `stale`

Legacy migration note: use `$ML-docs-project-lifecycle-statuses` only for previously scaffolded repos that still lack `in-review` and `blocked`.

Visual design gate migration note: for repos that already have this scaffold but predate `$visual-design-critique`, backfill the missing quality-gate docs and references with:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/visual-design-critique/scripts/backfill_visual_design_gate.py" --repo /path/to/repo
```

Default progress model: checkpoint-based updates (absolute timestamps, completed since prior checkpoint, next checkpoint target). Avoid `today/tomorrow` phrasing.

Timestamp reliability rule: never invent timestamps manually. Always generate Eastern Time (NYC) timestamps via the bundled script.

Capitalization and naming standard:
- For new scaffolds, default the docs root to `DOCS/`.
- If a repo already uses `docs/` or `documentation/`, preserve the existing docs root instead of renaming it automatically.
- Reserve uppercase directory names for the top-level docs root (`DOCS/` when newly created) and the project tracker root (`PROJECTS/`).
- Use lowercase for all other scaffolded docs directories: `development/`, `evidence/`, `features/`, `getting-started/`, `database/`, `deployment/`, `api/`, `contributing/`, `historical/`, `product/`.
- Reserve uppercase markdown filenames for repo-level governance and entrypoint docs: `README.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Use lowercase for content pages such as `index.md`, `checkpoint-workflow.md`, and numbered project docs like `1001_feature_plan.md`.

Manual-work callout standard:
- Whenever work requires Maggie's manual input, evidence gathering, manual testing, approval, or an external workstream, add a literal `MAGGIE TODO:` callout in the relevant project doc.
- Use one unresolved item per line, preferably as a bullet: `- MAGGIE TODO: <specific action or missing input>`.
- Keep unresolved items collected in a dedicated `## MAGGIE TODO` section in the project doc, and repeat the same callout near the relevant checkpoint, risk, note, or dependency section when useful for context.
- If unresolved `MAGGIE TODO` items block progress, move the project doc to `PROJECTS/blocked/` and keep the callouts visible until resolved.

Visual design quality gate:
- For significant user-facing UI, redesign, restyle, dashboard, form, app, website, visual QA, or screenshot-route work, require a `$visual-design-critique` checkpoint before implementation sign-off or movement to `PROJECTS/in-review/`.
- The critique must cover hierarchy, composition, typography, color/material, component states, interaction clarity, accessibility, responsive behavior, and product fit.
- Store durable screenshots, review-board packets, or critique artifacts in the evidence system only when they are needed for future verification or sign-off.
- Use `MAGGIE TODO:` when human taste approval, manual screenshot review, or external brand input gates completion.

## Required Decision Gates (ask first)
Before writing files, explicitly ask:
1. Do you want a docs site scaffolded now (`yes`/`no`)?
2. Do you want product docs pack scaffolding included (`yes`/`no`)?
3. Do you want the HTML project dashboard scaffolded now (`yes`/`no`)?
4. Do you want the optional Review Board Operating Pattern scaffold included for visual comparison, evidence review, and numbered human corrections (`yes`/`no`)?

Defaults if user does not specify:
- docs site: `no` (do not assume site generation)
- product docs pack: `no` (do not create product docs unless explicitly requested)
- project dashboard: `no` (do not create the dashboard unless explicitly requested)
- Review Board Operating Pattern scaffold: `no` (do not add review-board workflow docs unless explicitly requested)

Note: if invoked through deprecated `$ML-docs-product-pack`, force `product docs pack: yes`.

## Workflow (Step-by-step)

### 1) Discover the docs root
Check for existing docs root in this order:
1. `DOCS/`
2. `docs/`
3. `documentation/`

If multiple exist, prefer the one that already contains `README.md` or `index.md`. If ambiguous, ask the user.
If none exist, scaffold a new docs root at `DOCS/`.

### 1A) Detect review-board signals (required before optional Review Board Operating Pattern scaffolding)
Before asking the Review Board Operating Pattern question, inspect the repo for clear review-board signals such as:
- screenshot, route, UI, or design QA workflows
- evidence packets, audit reports, or visual comparison work
- image, asset, content, metadata, taxonomy, or catalog cleanup
- product review, PDP, feed, collection-management, or merchandising workflows
- requests for numbered boards, human corrections, or compare/contrast review

Use these signals to recommend whether the optional Review Board Operating Pattern scaffold should be included when you ask the required decision gate.
If the repo does not appear to need review-board support, recommend `no` but still respect an explicit user request to include it.

### 2) Apply safe-write rules
- Create missing files/directories.
- If a file exists, only add missing sections or append required guidance.
- Never overwrite existing file contents wholesale without explicit confirmation.

### 3) Generate trusted timestamps (required)
Run:

```bash
node <skill_dir>/assets/scripts/scripts/docs/timestamp-et.mjs --json
```

Use:
- `{{LAST_UPDATED_DATE_ET}}` -> `dateEt` (`YYYY-MM-DD`)
- `{{LAST_UPDATED_TS_ET}}` -> `timestampEt` (`YYYY-MM-DD HH:MM ET (America/New_York)`)

### 4) Scaffold baseline docs root
Copy templates from `assets/templates/docs-root/` into chosen docs root and replace placeholders:
- `{{DOCS_ROOT}}` -> chosen docs root (`DOCS` for new scaffolds; preserve existing `docs`/`documentation` roots)
- `{{LAST_UPDATED_DATE_ET}}` -> `dateEt`
- `{{LAST_UPDATED_TS_ET}}` -> `timestampEt`
- `{{PROJECT_NAME}}` -> repo name

Minimum required docs-root files:
- `{{DOCS_ROOT}}/README.md`
- `{{DOCS_ROOT}}/index.md`
- `{{DOCS_ROOT}}/PROJECTS/README.md`
- `{{DOCS_ROOT}}/PROJECTS/active/NNNN_project_template.md`
- `{{DOCS_ROOT}}/development/checkpoint-workflow.md`
- `{{DOCS_ROOT}}/development/visual-design-quality-gate.md`
- `{{DOCS_ROOT}}/evidence/README.md`
- `{{DOCS_ROOT}}/historical/index.md`

Also ensure lifecycle status folders exist under `{{DOCS_ROOT}}/PROJECTS/`:
- `active/`
- `in-review/`
- `blocked/`
- `completed/`
- `backlog/`
- `stale/`

Also ensure the evidence-system folders exist under `{{DOCS_ROOT}}/evidence/`:
- `active/`
- `archive/`
- `templates/`

When creating missing docs folders/files, follow the capitalization standard above instead of inventing repo-local variants.

### 5) Scaffold/update governance + agent instruction docs (required)
Update or create repository governance docs from `assets/templates/governance/`:
- `AGENTS.md`
- `ROADMAP.md`
- `CHANGELOG.md`

Also update docs references in root guidance files when present:
- `README.md`
- `AGENTS.md`
- `ROADMAP.md`
- `CHANGELOG.md`

When updating governance/instruction docs, include lifecycle transition policy:
- `active -> in-review` when implementation is complete and awaiting walkthrough/sign-off.
- `* -> blocked` when progress requires user decision/permission/input/access.
- `in-review -> completed` only after collaborative walkthrough/sign-off.
- Continue autonomous execution from backlog/stale while items are in `in-review` or `blocked`.
- Use `MAGGIE TODO:` callouts for Maggie-owned or externally gated manual follow-up items.
- Require `$visual-design-critique` before sign-off for significant user-facing UI work, and record the outcome in the owning project doc.

Additionally, if present, append docs-root links in agent instruction files (safe append only):
- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `.cursor/rules/*`

### 6) Add docs tooling scripts
Copy `assets/scripts/scripts/docs/*.mjs` into `scripts/docs/`.

Required scripts:
- `manifest.mjs`
- `check-links.mjs`
- `normalize-frontmatter.mjs`
- `timestamp-et.mjs`

### 7) Patch root `package.json` scripts (if present)
Add missing scripts only:
- `docs:manifest`: `node scripts/docs/manifest.mjs {{DOCS_ROOT}}`
- `docs:links`: `node scripts/docs/check-links.mjs {{DOCS_ROOT}}`
- `docs:frontmatter`: `node scripts/docs/normalize-frontmatter.mjs {{DOCS_ROOT}}`
- `docs:timestamp`: `node scripts/docs/timestamp-et.mjs --json`

If docs-site is enabled, also add:
- `docs:dev`
- `docs:build`
- `docs:preview`

### 8) Optional project dashboard scaffolding (only if user said yes)
After the baseline docs root, lifecycle folders, and `scripts/docs/` tooling exist, scaffold the companion dashboard output.

This built-in step should wire the same repo-level assets as the legacy standalone retrofit skill:
- `scripts/docs/projects-dashboard.mjs`
- `package.json` script `docs:projects-dashboard`
- `{{DOCS_ROOT}}/PROJECTS/dashboard.html`
- `{{DOCS_ROOT}}/PROJECTS/README.md` link to the dashboard

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ML-docs-project-dashboard-legacy/scripts/install_docs_project_dashboard.py" \
  --repo . \
  --docs-root {{DOCS_ROOT}}
```

Expected result:
- `{{DOCS_ROOT}}/PROJECTS/dashboard.html`
- `scripts/docs/projects-dashboard.mjs`
- optional `package.json` script:
  - `docs:projects-dashboard`
- `{{DOCS_ROOT}}/PROJECTS/README.md` link to `dashboard.html`

Rules:
- Treat the HTML dashboard as generated output, not source of truth.
- The markdown project docs remain the source of truth.
- If an older generated `dashboard.md` exists, it is safe for the installer to remove it.
- If a non-generated `dashboard.html` already exists, stop and ask before replacing it unless the user explicitly approved overwrite behavior.
- The generated dashboard should surface unresolved `MAGGIE TODO:` callouts in a dedicated section.

### 8A) Optional Review Board Operating Pattern scaffolding (only if user said yes)
If enabled, copy the optional Review Board Operating Pattern templates from `assets/templates/review-board-operating-pattern/` into the repo root with safe-write behavior:

- `{{DOCS_ROOT}}/development/review-board-operating-pattern.md`
- `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/README.md`
- `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/review-session-template.md`
- `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/corrections-template.md`

Then safe-update the following docs so the workflow is discoverable:
- `{{DOCS_ROOT}}/README.md`
- `{{DOCS_ROOT}}/index.md`
- `{{DOCS_ROOT}}/development/index.md`
- `{{DOCS_ROOT}}/PROJECTS/README.md`

Add references that make the Review Board Operating Pattern obvious:
- link the new development guide from docs indexes
- link the dedicated evidence templates area from docs indexes
- note that numbered JPG review boards are the primary artifact and PDF bundles are optional
- note that generated run packets should live under the owning project's evidence directory under `review-packets/<run-name>/` if intentionally preserved
- note that there is no separate durable docs temp bucket for evidence

When Review Board Operating Pattern scaffolding is enabled, append a short repo-specific note in `AGENTS.md`:
- for visual review, evidence review, or compare/contrast work, follow `{{DOCS_ROOT}}/development/review-board-operating-pattern.md`
- treat review-board work as a numbered project stream, not a one-off utility task
- use `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/` as the durable home for review-board templates
- if a review packet is intentionally preserved, store it under the owning project's evidence directory under `review-packets/<run-name>/`

Do not encode repo-specific business rules into the scaffold.
Keep rules like visual quality criteria, accessibility standards, content taxonomy, data ownership, metafield mappings, and destination collection logic local to the repo.

### 9) Optional docs-site scaffolding (only if user said yes)
If enabled:
1. Copy `assets/vitepress/DOCS/.vitepress/config.ts` -> `{{DOCS_ROOT}}/.vitepress/config.ts`
2. Copy `assets/vitepress/docs-site/` -> `docs-site/` and replace `{{DOCS_ROOT}}` in `docs-site/package.json`
3. Copy `assets/vitepress/docs-site/wrangler.toml` -> `wrangler.toml` and replace placeholders:
   - `{{DOCS_ROOT}}`
   - `{{PROJECT_NAME}}`
   - `{{COMPATIBILITY_DATE}}` (`dateEt`)

### 10) Add docs CI sync workflow (required)
Create/update `.github/workflows/docs-site-sync.yml` from:
- `assets/templates/workflows/docs-site-sync.yml`

Replace placeholders:
- `{{DOCS_ROOT}}` -> docs root
- `{{DOCS_SITE_ENABLED}}` -> `true` or `false`

Rules:
- Trigger on `push` to `main`
- Use docs-related `paths` filters
- Do not auto-commit generated artifacts from CI

### 11) Product docs pack scaffolding (optional)
Only if enabled, ensure product docs folder exists under docs root:
- `{{DOCS_ROOT}}/product/`

Create/update (safe-write):
- `{{DOCS_ROOT}}/product/README.md`
- `{{DOCS_ROOT}}/product/product-brief.md`
- `{{DOCS_ROOT}}/product/lean-canvas.md`
- `{{DOCS_ROOT}}/product/prd.md`
- `{{DOCS_ROOT}}/product/decision-log.md`

Use templates from:
- `assets/templates/product-docs/product-doc-templates.md`

### 12) Prime docs manifest
Run:

```bash
node scripts/docs/manifest.mjs {{DOCS_ROOT}}
```

If the project dashboard is enabled and `package.json` contains `docs:projects-dashboard`, also run:

```bash
npm run docs:projects-dashboard
```

### 13) Verification checklist (required)
Before finishing, verify and report:
- docs root exists and has required baseline files
- evidence root exists and has required baseline folders
- governance files exist and reference docs root
- agent instruction docs (when present) include docs-root links
- docs CI workflow exists and matches selected docs-site mode
- generated docs follow the capitalization standard for newly scaffolded paths/files
- manifest generation succeeds
- if dashboard is enabled:
  - `{{DOCS_ROOT}}/PROJECTS/dashboard.html` exists
  - dashboard links open the project markdown docs
  - `scripts/docs/projects-dashboard.mjs` exists
  - `PROJECTS/README.md` links to `dashboard.html`
  - unresolved `MAGGIE TODO:` callouts render in a dedicated dashboard section when present
- if Review Board Operating Pattern scaffold is enabled:
  - `{{DOCS_ROOT}}/development/review-board-operating-pattern.md` exists
  - `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/README.md` exists
  - `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/review-session-template.md` exists
  - `{{DOCS_ROOT}}/evidence/templates/review-board-operating-pattern/corrections-template.md` exists
  - `{{DOCS_ROOT}}/README.md`, `{{DOCS_ROOT}}/index.md`, and `{{DOCS_ROOT}}/development/index.md` point to the Review Board Operating Pattern workflow or evidence templates area
  - `{{DOCS_ROOT}}/PROJECTS/README.md` references the Review Board Operating Pattern workflow pairing
  - `AGENTS.md` points visual review, evidence review, or compare/contrast work to the Review Board Operating Pattern workflow guide and the evidence templates area

## Retrofit Guidance

For existing repos with evidence drift, do not treat this skill as the migration workflow.

Use `$ML-docs-evidence-backfill` to:
- inventory fragmented evidence roots
- classify evidence into `active`, `archive`, `templates`, or delete
- migrate evidence into `{{DOCS_ROOT}}/evidence/`
- update old docs references and script defaults

## Default automation policy
Docs changes merged to `main` should run docs normalization, manifest regeneration, link checks, and (when enabled) docs-site build in CI.

## Resources
- Docs root templates: `assets/templates/docs-root/`
- Governance templates: `assets/templates/governance/`
- Workflow template: `assets/templates/workflows/`
- Product docs templates: `assets/templates/product-docs/`
- Tooling scripts: `assets/scripts/`
- Optional Review Board Operating Pattern templates: `assets/templates/review-board-operating-pattern/`
- Optional VitePress/docs-site assets: `assets/vitepress/`
- Companion dashboard installer: `${CODEX_HOME:-$HOME/.codex}/skills/ML-docs-project-dashboard-legacy/scripts/install_docs_project_dashboard.py`
