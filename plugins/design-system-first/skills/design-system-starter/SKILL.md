---
name: design-system-starter
description: Scaffold greenfield, design-system-first Next.js projects with strong defaults, Tailwind, shadcn, shared tokens, and starter surfaces. Use when creating a new web app or marketing site from scratch and the user wants an opinionated starter with optional docs support or testing scaffolding rather than a blank template.
---

# Design System Starter

Use this skill when the user wants a new project started quickly, but still wants the first commit to already express a coherent design system instead of a generic scaffold.

The starter is intentionally opinionated:
- framework: Next.js App Router + TypeScript
- styling: Tailwind + CSS variables
- component base: shadcn
- starter modes: `marketing-only` and `app-shell`
- optional add-ons: `docs`, `testing`

## Before You Scaffold

Lock these decisions before running the script:

1. Confirm the destination path and whether it should be a fresh folder.
2. Choose the mode:
   - `marketing-only` for a branded landing-page starter
   - `app-shell` for a restrained product/workspace shell
3. Choose add-ons:
   - `docs` for docs-root and governance scaffolding
   - `testing` for Vitest + Playwright
4. Choose the package manager if the repo or user preference makes it clear. Otherwise default to `npm`.

Do not assume backend scaffolding. v1 is frontend-first.

## Primary Workflow

Run the bundled scaffold script:

```bash
python3 scripts/scaffold_design_system_first.py \
  --path /absolute/path/to/project \
  --mode marketing-only \
  --package-manager npm \
  --addons docs,testing
```

The script will:
- create a fresh Next.js app with Tailwind and the App Router
- initialize shadcn and add the core components the starter uses
- apply shared design-system tokens and starter surfaces
- optionally apply testing files and dependencies
- optionally apply a docs-root baseline by reusing the existing docs-system scaffold assets

## After Scaffolding

Use the surrounding ecosystem rather than duplicating it:

- Use `$shadcn` for any follow-on component additions or registry work.
- Use `$frontend-skill` when the user wants stronger art direction or a more premium visual pass.
- Use `$react-best-practices` after substantial React/Next edits.
- If the user wants a full docs site, product docs pack, or docs governance beyond the starter baseline, follow with `$ML-docs-system-scaffold`.
- If the user wants deeper polish after the initial scaffold, follow with `$design-system-refine`.

## Guided Integrations

Do not block the scaffold on missing credentials or MCPs.

Instead:
- recommend relevant MCPs and follow-on plugins using `references/recommended-integrations.md`
- only add env/config placeholders when the user explicitly wants them
- avoid inventing private-registry token names or secret wiring

## References

- `references/modes-and-addons.md` explains what each starter mode and add-on should produce
- `references/recommended-integrations.md` lists recommended MCPs, plugins, and follow-on skills
