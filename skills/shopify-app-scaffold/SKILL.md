---
name: shopify-app-scaffold
description: Custom skill created by Maggie Lerman. Scaffold a new Shopify app from the latest installed Shopify CLI template, then layer in a reusable shell for merchant email opt-in, unsubscribe flow, review prompts, and optional billing/app-proxy/theme-extension placeholders. Use when creating a new Shopify app quickly without copying an old repo wholesale.
---

# Shopify App Scaffold

Custom skill created by Maggie Lerman.

Use this skill when the user wants a new Shopify app created fast, but still wants a reusable shell for common app concerns like merchant comms and review prompts.

## What This Skill Does

The skill is intentionally split into two layers:

1. A fresh Shopify CLI scaffold.
2. Optional reusable overlays copied from this skill's bundled assets.

This keeps the base app current with Shopify's latest installed template while still giving us a reusable shell.

## What This Skill Does Not Do

- It does not scaffold docs or repo governance.
- It does not clone an existing product repo.
- It does not infer the app's product-specific logic.
- It does not automatically build a full billing system in v1.

## Before You Start

Check the installed Shopify CLI:

```bash
shopify version
```

If the CLI reports that a newer version is available, do not upgrade it automatically unless the user asks. Use the installed CLI, but call out version drift in your response.

Before scaffolding, pause and confirm the repo/location decision with the user. Ask explicitly:

- should the app live in the folder opened for this thread
- should it live in a new repo directory, and if so, at what exact path
- is git already initialized there, or should the agent initialize a new repo after scaffolding

Do not assume GitHub repo creation. The scaffold script creates the app locally; publishing to GitHub is a separate follow-up step.

## Primary Workflow

### 1. Run the scaffold script

Use the bundled script first:

```bash
python3 /Users/maggielerman/.codex/skills/shopify-app-scaffold/scripts/scaffold_shopify_app.py --help
```

Typical command:

```bash
python3 /Users/maggielerman/.codex/skills/shopify-app-scaffold/scripts/scaffold_shopify_app.py \
  --app-name "Agentic Shopping SEO" \
  --path /absolute/path/to/new-app \
  --support-email support@example.com \
  --scopes write_content \
  --database-mode postgres_prisma \
  --features merchant-comms,review-prompts
```

Important defaults:

- Template: `reactRouter`
- Flavor: `typescript`
- Package manager: `npm`

Notes:

- `shopify app init` is interactive unless you pass `--client-id`, so expect an organization selection prompt during fresh scaffolds.
- In the interactive "create a new app" path, Shopify CLI may scaffold into a slugged child directory under the provided `--path`. The script now detects that case and collapses the nested app back into the requested target path when it is safe to do so.
- Use `--skip-init` only against an existing Shopify app project that already has `package.json` and `prisma/schema.prisma`.
- Use `--no-install` when you want a dry-ish scaffold pass without installing overlay dependencies yet.

Path guidance:

- If the user wants to work in the folder opened for the thread, pass that folder as `--path`.
- If the user wants a brand-new repo, have them choose the final parent folder first, then pass the intended repo root as `--path`.
- If the user says the current location already has an initialized repo/app, treat that as an existing target and prefer the existing repo structure over creating a sibling directory.

### 2. Review the scaffold summary

The script will:

- create the new Shopify app
- detect installed vs latest CLI version when possible
- write or extend `.env.example`
- ensure `.env.example` remains commitable even if the template gitignore ignores `.env.*`
- add overlay files for selected modules
- append required Prisma models
- switch the generated Prisma datasource from SQLite to Postgres and add `prisma:setup` when Postgres mode is selected
- add any missing dependencies for selected features
- harden the generated package manifest with the current audit-safe `@typescript-eslint` versions plus scoped Prisma/minimatch overrides
- remove pnpm-only `.npmrc` flags when scaffolding with `npm` so repeated `npm` commands stay warning-free

### 3. Finish integration in the generated app

After the script runs, inspect the generated app and wire any remaining app-specific pieces:

- choose where review prompts should appear
- define the app's value milestones
- connect comms opt-in UI to the app's settings/onboarding flow
- decide whether the app will eventually need app proxy or theme extension routing

Use [module-selection.md](./references/module-selection.md) for the follow-up integration steps.

## Feature Selection

Supported v1 features:

- `merchant-comms`
- `review-prompts`

Reserved feature flags, not bundled yet:

- `billing-stub`
- `app-proxy`
- `theme-extension`

If you request a reserved flag before its overlay is implemented, the scaffold script will fail fast with a clear error instead of silently doing nothing.

Recommended default set for lightweight admin apps:

- `merchant-comms,review-prompts`

Reserved storefront-adjacent follow-on flags once implemented:

- `app-proxy`
- `theme-extension`

## Database Modes

- `sqlite_local`
  Best for fast exploration.
- `postgres_prisma`
  Best for production-ready apps. This adds `DATABASE_URL`, `DIRECT_URL`, and `scripts/prisma-setup.sh`.

## Overlay Boundaries

The bundled overlays are repo-agnostic and intentionally generic:

- merchant comms uses milestone-triggered lifecycle emails rather than job-specific logic
- review prompts use milestone-based eligibility rather than bulk-task completion
- billing/app-proxy/theme-extension are reserved expansion points until those overlays are bundled

If the user wants docs or governance setup too, use your docs skill separately after the Shopify app exists.
