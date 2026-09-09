---
name: "rps-etsy-shop-uploader-listing-workflow"
description: "Use when preparing, reviewing, applying, verifying, or debugging Rock Paper Scissors Etsy listing work through Shop Uploader, including exports, CSV/XLSX templates, draft-create packets, partial updates, media/file URLs, upload reports, and post-update verification. Custom skill by Maggie Lerman."
---

# RPS Etsy Shop Uploader Listing Workflow

Custom skill by Maggie Lerman.

Use this skill for RPS Etsy listing work that touches Shop Uploader or could become a Shop Uploader apply packet.

## Source Of Truth

- Etsy catalog repo: resolve `rps-etsy` using `references/repository-resolution.md`
- Creative asset storage/catalog: Google Drive `RPS Creative Assets` plus `docs/etsy/creative-asset-drive-catalog.md` in the resolved `rps-etsy` root
- Durable plugin backup: `plugins/rps-etsy-ops/` in the resolved `codex-skills` root
- Shop Uploader dashboard: `https://www.shopuploader.com/app/dashboard`
- Live Etsy mutation path: Shop Uploader CSV/XLSX only, after Maggie approves a reviewable apply plan.

Do not use Etsy API mutation paths for this workflow.

## Required Reading

In the resolved `rps-etsy` root, read:

1. `AGENTS.md`
2. `docs/etsy/workstreams/shop-uploader-operations.md`
3. The relevant active project doc under `docs/PROJECTS/active/`
4. For media/mockup/image/video work, also read:
   - `docs/etsy/workstreams/listing-images-and-alt-text.md`
   - `docs/etsy/mockup-library.md`
   - `docs/etsy/creative-asset-drive-catalog.md`
   - `docs/etsy/asset-hosting-policy.md`
   - `$rps-wall-art-mockup-workflow`
   - `$rps-etsy-media-hosting-workflow`

## Core Rules

1. Never mutate live Etsy listings without explicit Maggie approval and a reviewable apply plan.
2. Start from a fresh Shop Uploader export for the exact listing IDs whenever updating existing listings.
3. Preserve the full source export and template header.
4. Populate only approved fields.
5. Treat media, videos, and digital files as higher risk than title/tag updates.
6. Do not prepare `image_*`, `image_alt_text_*`, `video_1`, or `digital_file_*` values from historical scripts, minimal/safe CSVs, or regression packets.
7. Use the typed reusable template set for file shape selection, but do not treat a template shell as an upload file.
8. A Shop Uploader success report proves field acceptance only. It does not prove metadata completeness, media quality, publish readiness, or buyer-file correctness.

## Task Classification

Before doing work, classify the request:

- `read_only_review`: inspect exports, reports, docs, listings, or evidence without preparing an upload file.
- `review_packet`: prepare proposed changes, manifests, review boards, or comparison reports only.
- `draft_create`: create new Etsy draft listing packet.
- `partial_update_metadata`: update existing listing titles, tags, descriptions, attributes, or shop sections.
- `partial_update_media`: update existing listing images, videos, or digital files.
- `post_apply_verification`: inspect Shop Uploader reports, Etsy UI, exports, screenshots, or cleanup status after an approved run.

If the task could affect live listings, keep it review-only until approval is explicit.

## Existing Listing Partial Updates

1. Identify exact listing IDs and SKUs.
2. Export only target listings from Shop Uploader.
3. Preserve the source export under `docs/evidence/active/<project>/`.
4. Create a listing-level apply plan with current value, proposed value, reason, and approval status.
5. For conservative metadata edits, prefer `partial_update` with only:
   - `listing_id`
   - approved changed fields
   - `action=partial_update`
6. Confirm no media, price, quantity, listing state, digital file, delete, or overwrite fields are populated unless approved.
7. After approval, upload through Shop Uploader.
8. Download the upload report.
9. Verify with a fresh post-update export.
10. Record the result in the owning project doc and master changelog when durable.

## New Draft Listings

Use draft-first creation.

Do not call a new-listing Shop Uploader file upload-ready until it includes and has been reviewed for:

- full current Shop Uploader template header
- the correct typed template shape from `docs/evidence/templates/shop-uploader/digital-downloads/digital-prints-2078-template-set-2026-05-27/`
- title, description, price, quantity, draft listing state, category, shop section, SKU, and create controls
- all 13 tags and materials where applicable
- all available category `_underscore_columns`
- all five printable wall-art aspect ratios when the listing promises a five-ratio buyer bundle: `2:3`, `3:4`, `4:5`, `11:14`, `5:7 (ISO ratio)`
- colors, style, room, subject, occasion/holiday, recipient where exposed
- image URLs and image alt text
- video URL when approved
- digital file URLs and file names when approved
- source-art and rights notes
- buyer ZIP/file manifest
- media/mockup review board when media is included

Create listings as drafts first and keep publishing as a separate approval step.

## Reusable Templates

For `Digital Prints (2078)`, use the reusable typed template set before preparing a review packet:

`docs/evidence/templates/shop-uploader/digital-downloads/digital-prints-2078-template-set-2026-05-27/`

Key files:

- `README.md`: template-set operating notes
- `template-set-manifest.csv`: intended use and risk by template
- `column-dictionary.csv`: full 217-column surface and requirement guide
- `product-type-profiles.csv`: recommended starting template by product/update type

Available template types:

- full draft create
- slim draft create
- title/tags partial update
- description/tags/attributes partial update
- attributes-only correction
- 20-image/video media update
- 20-image-only update
- video-only update
- digital-file-only update
- shop-settings update
- high-risk listing-state control review

Every generated template is header-only and starts with `TEMPLATE-DO-NOT-UPLOAD`. When Shop Uploader's current export/template changes, regenerate the set:

```bash
python3 scripts/etsy/build-shop-uploader-template-set.py
```

## Media, Mockups, Videos, And Digital Files

Before any Shop Uploader file includes media or file URLs:

1. Use `$rps-wall-art-mockup-workflow` for wall-art mockups.
2. Select a row from `docs/etsy/mockup-availability.csv`.
3. Validate the mockup matrix:

   ```bash
   python3 scripts/etsy/validate-mockup-availability.py
   ```

4. Confirm artwork count gates match the listing.
5. Build a review board and manifest mapping listing ID, SKU, source art, mockup catalog row/template ID, output path, intended slot, and approval status.
6. Confirm mockup/media labels use generic product/use-case language and do not expose artist/provenance labels.
7. Use clear hosted URL paths from `docs/etsy/asset-hosting-policy.md`.
8. Use `$rps-etsy-media-hosting-workflow` for hosted URL manifests, URL access audits, and cleanup tracking.
9. Audit public URLs before upload:

   ```bash
   python3 scripts/etsy/audit-hosted-url-manifest.py <hosted-url-manifest.csv>
   ```

10. Preserve local media validation, URL audit reports, prepared upload files, upload reports, and post-update proof.

## Evidence Packet Shape

Store evidence under:

`docs/evidence/active/<project>/shop-uploader/<YYYY-MM-DD-short-slug>/`

Keep:

- source export
- prepared upload file
- apply plan
- review board when visual/media changes are involved
- hosted URL manifest and access audit when URLs are involved
- Shop Uploader upload report
- post-update export or Etsy UI proof
- comparison summary
- cleanup proof for temporary hosted URLs

## Validation Commands

Common commands from the resolved `rps-etsy` root:

```bash
python3 scripts/etsy/validate-mockup-availability.py
python3 scripts/etsy/refresh-mockup-library-indexes.py
python3 scripts/etsy/audit-hosted-url-manifest.py <hosted-url-manifest.csv>
python3 scripts/etsy/build-shop-uploader-template-set.py
python3 scripts/etsy/audit-shop-uploader-field-coverage.py
node scripts/docs/manifest.mjs docs
node scripts/docs/check-links.mjs docs
```

For `Digital Prints (2078)` metadata files:

```bash
python3 scripts/etsy/validate-shop-uploader-digital-prints-2078.py <shop-uploader-csv>
python3 scripts/etsy/audit-shop-uploader-field-coverage.py
```

## Stop Conditions

Stop and ask Maggie before proceeding if:

- approval to mutate Etsy is unclear
- target listing IDs or SKUs are ambiguous
- the source export is stale or missing
- required Shop Uploader template columns are missing
- the media/mockup review board is not approved
- URL audit fails
- buyer files would be replaced or deleted
- the upload would publish listings instead of creating/updating drafts
