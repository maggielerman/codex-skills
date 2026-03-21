---
name: docs-system-scaffold
description: Scaffold or standardize a repository documentation system (DOCS/ or docs), optionally scaffold a VitePress docs site, install docs tooling, and include an optional lightweight product-doc pack. Use when asked for docs system setup, docs IA cleanup, docs governance hardening, product docs scaffolding, or docs-site setup.
---

# Docs System Scaffold

## Overview
Create or standardize a predictable documentation system with safe-write behavior. This skill now combines:
- docs root + governance scaffolding,
- docs tooling (`manifest`, `links`, `frontmatter`, timestamps),
- optional docs site scaffolding,
- optional lightweight product-doc pack scaffolding.

Default project lifecycle states created/enforced by scaffolded docs:
- `active`
- `in-review`
- `blocked`
- `completed`
- `backlog`
- `stale`

Legacy migration note: use `$docs-project-lifecycle-statuses` only for previously scaffolded repos that still lack `in-review` and `blocked`.

Default progress model: checkpoint-based updates (absolute timestamps, completed since prior checkpoint, next checkpoint target). Avoid `today/tomorrow` phrasing.

Timestamp reliability rule: never invent timestamps manually. Always generate Eastern Time (NYC) timestamps via the bundled script.

## Required Decision Gates (ask first)
Before writing files, explicitly ask:
1. Do you want a docs site scaffolded now (`yes`/`no`)?
2. Do you want product docs pack scaffolding included (`yes`/`no`)?

Defaults if user does not specify:
- docs site: `no` (do not assume site generation)
- product docs pack: `no` (do not create product docs unless explicitly requested)

Note: if invoked through deprecated `$docs-product-pack`, force `product docs pack: yes`.

## Workflow (Step-by-step)

### 1) Discover the docs root
Check for existing docs root in this order:
1. `DOCS/`
2. `docs/`
3. `documentation/`

If multiple exist, prefer the one that already contains `README.md` or `index.md`. If ambiguous, ask the user.

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
- `{{DOCS_ROOT}}` -> `DOCS` or `docs`
- `{{LAST_UPDATED_DATE_ET}}` -> `dateEt`
- `{{LAST_UPDATED_TS_ET}}` -> `timestampEt`
- `{{PROJECT_NAME}}` -> repo name

Minimum required docs-root files:
- `{{DOCS_ROOT}}/README.md`
- `{{DOCS_ROOT}}/index.md`
- `{{DOCS_ROOT}}/PROJECTS/README.md`
- `{{DOCS_ROOT}}/PROJECTS/active/NNNN_project_template.md`
- `{{DOCS_ROOT}}/development/checkpoint-workflow.md`
- `{{DOCS_ROOT}}/historical/index.md`

Also ensure lifecycle status folders exist under `{{DOCS_ROOT}}/PROJECTS/`:
- `active/`
- `in-review/`
- `blocked/`
- `completed/`
- `backlog/`
- `stale/`

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

### 8) Optional docs-site scaffolding (only if user said yes)
If enabled:
1. Copy `assets/vitepress/DOCS/.vitepress/config.ts` -> `{{DOCS_ROOT}}/.vitepress/config.ts`
2. Copy `assets/vitepress/docs-site/` -> `docs-site/` and replace `{{DOCS_ROOT}}` in `docs-site/package.json`
3. Copy `assets/vitepress/docs-site/wrangler.toml` -> `wrangler.toml` and replace placeholders:
   - `{{DOCS_ROOT}}`
   - `{{PROJECT_NAME}}`
   - `{{COMPATIBILITY_DATE}}` (`dateEt`)

### 9) Add docs CI sync workflow (required)
Create/update `.github/workflows/docs-site-sync.yml` from:
- `assets/templates/workflows/docs-site-sync.yml`

Replace placeholders:
- `{{DOCS_ROOT}}` -> docs root
- `{{DOCS_SITE_ENABLED}}` -> `true` or `false`

Rules:
- Trigger on `push` to `main`
- Use docs-related `paths` filters
- Do not auto-commit generated artifacts from CI

### 10) Product docs pack scaffolding (optional)
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

### 11) Prime docs manifest
Run:

```bash
node scripts/docs/manifest.mjs {{DOCS_ROOT}}
```

### 12) Verification checklist (required)
Before finishing, verify and report:
- docs root exists and has required baseline files
- governance files exist and reference docs root
- agent instruction docs (when present) include docs-root links
- docs CI workflow exists and matches selected docs-site mode
- manifest generation succeeds

## Default automation policy
Docs changes merged to `main` should run docs normalization, manifest regeneration, link checks, and (when enabled) docs-site build in CI.

## Resources
- Docs root templates: `assets/templates/docs-root/`
- Governance templates: `assets/templates/governance/`
- Workflow template: `assets/templates/workflows/`
- Product docs templates: `assets/templates/product-docs/`
- Tooling scripts: `assets/scripts/`
- Optional VitePress/docs-site assets: `assets/vitepress/`
