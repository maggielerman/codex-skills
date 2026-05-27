---
name: "rps-etsy-media-hosting-workflow"
description: "Use when preparing, auditing, reviewing, or cleaning up hosted image, video, or digital-file URLs for Rock Paper Scissors Etsy Shop Uploader packets. Custom skill by Maggie Lerman."
---

# RPS Etsy Media Hosting Workflow

Use this skill when Etsy listing work needs public URLs for Shop Uploader fields
such as `image_*`, `video_1`, or `digital_file_*`.

## Source Of Truth

- Etsy catalog repo: `/Users/maggielerman/Github/rps-etsy`
- Creative asset repo: `/Users/maggielerman/Github/rps-creative-assets`
- Hosting policy: `/Users/maggielerman/Github/rps-etsy/docs/etsy/asset-hosting-policy.md`
- Plugin reference: `../../references/media-hosting-url-contract.md`

## Core Rules

1. Never treat hosted URL preparation as approval to mutate Etsy.
2. Use approval-state-aware paths that make current files distinct from historical or test uploads.
3. Preserve a hosted URL manifest in the owning `rps-etsy` evidence folder.
4. Audit every URL before adding it to a Shop Uploader file.
5. Record cleanup status for temporary hosted URLs after verification.
6. Do not host or upload buyer files without a reviewed buyer-file manifest.

## Workflow

1. Identify the owning project, listing IDs/SKUs, and target fields.
2. Read `asset-hosting-policy.md` and the current project doc.
3. Confirm source media or buyer files are approved for the intended listing.
4. Create or update the hosted URL manifest under `docs/evidence/active/<project>/`.
5. Run the URL audit from the `rps-etsy` repo:

   ```bash
   python3 scripts/etsy/audit-hosted-url-manifest.py <hosted-url-manifest.csv>
   ```

6. Block Shop Uploader preparation if any URL fails, redirects unexpectedly, lacks public access, or maps to the wrong MIME/type.
7. Link the audit result, manifest, and cleanup plan from the apply packet.

## Stop Conditions

Stop and ask Maggie before proceeding if:

- URL hosting location is unclear
- a URL points to historical, rapid-draft, or test media
- a buyer file would be replaced or removed
- the URL audit fails
- live Etsy mutation approval is unclear
