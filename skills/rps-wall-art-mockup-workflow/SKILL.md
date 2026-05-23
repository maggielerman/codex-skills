---
name: "rps-wall-art-mockup-workflow"
description: "Use when creating, refining, organizing, or applying Rock Paper Scissors wall art mockups for Shopify listings, Shopify blog/editorial images, collection heroes, catalog cleanup, marketplace imagery, social, ads, or reusable mockup packs. Custom skill by Maggie Lerman."
---

# RPS Wall Art Mockup Workflow

Custom skill by Maggie Lerman.

Use this skill for Rock Paper Scissors wall art mockup work across Shopify listings, Shopify editorial/content, Shopify collections, catalog cleanup, Faire/Etsy/marketplace images, social, ads, and reusable creative asset packs.

## Source Of Truth

- Asset repo default: `${HOME}/Github/rps-creative-assets`
- Durable workflow source: `codex-skills/skills/rps-wall-art-mockup-workflow/`
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
9. Validate the pack with the asset repo script.
10. Promote approved packs under `mockups/wall-art/approved-packs/`.

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
node scripts/validate-manifests.mjs
```

For skill repo changes:

```bash
python3 scripts/build_catalog.py --check
python3 scripts/build_catalog.py
python3 scripts/build_docs_site_catalog.py
```
