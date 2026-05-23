# Repository Contract

## Default Asset Repo

`${HOME}/Github/rps-creative-assets`

## Pack Shape

```text
pack-slug/
  manifest.json
  raw-bases/
  composited-examples/
  review-board.jpg
```

## Main Surfaces

- `shopify-listing`
- `shopify-blog`
- `shopify-collection`
- `faire`
- `etsy`
- `social`
- `ads`
- `catalog-cleanup`

## Folder Map

```text
mockups/wall-art/
  approved-packs/
  shopify-listings/
  blog-editorial/
  collection-hero/
  marketplace/
    etsy/
    faire/
  social/
  ads/
source-art/
  public-domain/
  product-art/
```

## Promotion Rule

Only move a pack into `approved-packs/` after Maggie approves the visual direction or an applied production usage proves it should be reused.

## Validation

Run from the asset repo:

```bash
node scripts/validate-manifests.mjs
```
