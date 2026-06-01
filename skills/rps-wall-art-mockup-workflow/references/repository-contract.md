# Repository Contract

## Current Storage Contract

Reusable asset binaries live in Google Drive under `RPS Creative Assets`.
The catalog sheet and the `rps-etsy` snapshot are the durable lookup surfaces.
`${HOME}/Github/rps-creative-assets` is a read-only migration archive and
optional local cache.
Google Drive for desktop may be used as an optional machine-local cache via
`RPS_CREATIVE_ASSETS_DRIVE_CACHE`, but automation must use catalog
`template_id`, `drive_file_id`, `drive_folder_id`, and Drive URL fields as the
durable references.

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

## Intended Drive Folder Map

```text
RPS Creative Assets/
  Wall Art Mockups/
    Etsy/
      Approved/
      In Review/
      Calibration/
      Historical/
      Review Boards/
```

## Promotion Rule

Only mark a catalog row `approved` after Maggie approves the visual direction
or an applied production usage proves it should be reused.

## Validation

Run from `rps-etsy`:

```bash
python3 scripts/etsy/check-creative-asset-drive-cache.py
python3 scripts/etsy/validate-mockup-availability.py
```
