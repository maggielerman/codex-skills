---
name: "rps-wall-art-mockup-workflow"
description: "Use when creating, refining, organizing, or applying Rock Paper Scissors wall art mockups for Shopify listings, Shopify blog/editorial images, collection heroes, catalog cleanup, marketplace imagery, social, ads, or reusable mockup packs. Custom skill by Maggie Lerman."
---

# RPS Wall Art Mockup Workflow

Custom skill by Maggie Lerman.

Use this skill for Rock Paper Scissors wall art mockup work across Shopify listings, Shopify editorial/content, Shopify collections, catalog cleanup, Faire/Etsy/marketplace images, social, ads, and reusable creative asset packs.

## Source Of Truth

- Asset repo default: `${HOME}/Github/rps-creative-assets`
- Durable plugin backup: `/Users/maggielerman/Github/codex-skills/plugins/rps-etsy-ops/`
- Standalone transition copy: `/Users/maggielerman/Github/codex-skills/skills/rps-wall-art-mockup-workflow/`
- Application repos keep project evidence, live apply proof, and deployment records.

If the asset repo is missing, create or locate it before generating a new reusable pack. See `references/repository-contract.md`.

## Core Rule

For named artists, public-domain works, or identifiable artworks:

1. Generate or select the room/mockup base with blank frames or blank placeholders only.
2. Composite real RPS source/product artwork into the placeholders.
3. Never generate fake artwork in a named artist's style.

## Workflow

1. Identify the target surface: `shopify-listing`, `shopify-blog`, `shopify-collection`, `faire`, `etsy`, `social`, `ads`, or `catalog-cleanup`.
2. Search the asset repo for an approved pack that already fits the surface and visual direction.
3. If a pack exists, reuse it or adapt it before generating a new scene.
4. If a new base is needed, generate blank-frame/blank-placeholder scenes only.
5. Gather real RPS artwork assets for all visible framed art.
6. Composite artwork into the generated base with plausible perspective, crop, scale, and frame fill.
7. Export a small labeled option set and one review board.
8. Write or update `manifest.json` using `templates/mockup-manifest.template.json`.
9. If a new reusable wall-art mockup pack or base is created, register it in the relevant channel availability/index before treating the work as complete. For Etsy, update `rps-etsy/docs/etsy/mockup-availability.csv`, regenerate the Etsy mockup visual index, and keep the asset repo wall-art index current.
10. Validate the pack with the asset repo script.
11. Promote approved packs under `mockups/wall-art/approved-packs/`.

## Library Naming Rule

Reusable pack names, matrix rows, review-board labels, and generated indexes must use generic product/use-case language such as `modern botanical`, `warm metallic`, `traditional single frame`, or `Samsung Frame TV`.

Do not use artist/provenance names as reusable library labels, CSV product-fit copy, pack titles, or visual-index titles. If old filesystem paths still contain legacy names, migrate them to generic names before publishing or committing new library work.

## Practical Defaults

- Use `shopify-listing` as a first-class surface, not an afterthought.
- Keep Shopify listing mockups clear and product-informative; avoid misleading physical-frame claims if RPS is selling prints.
- Blog/editorial images can be more atmospheric, but the art must still be specific and compelling.
- Marketplace variants should satisfy channel constraints without becoming the organizing center of the library.

## When To Read References

- Read `references/visual-guardrails.md` before generating or judging visuals.
- Read `references/prompt-patterns.md` before writing image prompts.
- Read `references/repository-contract.md` before creating, moving, or validating asset packs.
- Read `references/review-board-format.md` before building a review board.

## Validation

In the asset repo:

```bash
node scripts/build-wall-art-index.mjs
node scripts/validate-manifests.mjs
```

For Etsy mockup work in `rps-etsy`:

```bash
python3 scripts/etsy/validate-mockup-availability.py
python3 scripts/etsy/build-mockup-library-visual-index.py
```

For skill repo changes:

```bash
python3 scripts/build_catalog.py --check
python3 scripts/build_catalog.py
python3 scripts/build_docs_site_catalog.py
```
