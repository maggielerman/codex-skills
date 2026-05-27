---
name: "rps-etsy-digital-product-packet-workflow"
description: "Use when creating, reviewing, or validating reusable Rock Paper Scissors Etsy digital-download product packets before Shop Uploader draft creation or updates. Custom skill by Maggie Lerman."
---

# RPS Etsy Digital Product Packet Workflow

Use this skill for reusable digital-download product packets before creating or
updating Etsy listings through Shop Uploader.

## Source Of Truth

- Etsy catalog repo: `/Users/maggielerman/Github/rps-etsy`
- Creative asset repo: `/Users/maggielerman/Github/rps-creative-assets`
- Packet reference: `references/digital-product-packet-contract.md`
- Shop Uploader workflow: `$rps-etsy-shop-uploader-listing-workflow`
- Media hosting workflow: `$rps-etsy-media-hosting-workflow`
- Wall-art mockup workflow: `$rps-wall-art-mockup-workflow`

## Packet Requirements

A product packet is not complete until it includes:

- exact product type and intended Etsy action
- source art, rights notes, and transformation notes
- SKU/listing identifiers where known
- buyer ZIP/file manifest
- promised aspect ratios and delivered file set
- mockup/media manifest and review board when media is included
- selected Shop Uploader template type
- field coverage notes for metadata, attributes, tags, materials, and media
- hosted URL manifest and audit report when URLs are included
- approval state and open `MAGGIE TODO` items

## Workflow

1. Read `AGENTS.md`, the relevant project doc, and `docs/etsy/workstreams/digital-product-pipeline.md` as a packet-contract reference.
2. Identify whether the packet is for a new draft listing, partial update, media-only update, or buyer-file update.
3. Validate source art and buyer deliverables before preparing listing metadata.
4. Use the Shop Uploader workflow for CSV/XLSX shape and apply planning.
5. Use the wall-art mockup workflow for marketplace media.
6. Use the media hosting workflow for any public URLs.
7. Store the packet under `docs/evidence/active/<project>/`.

## Stop Conditions

Stop and ask Maggie before proceeding if:

- listing IDs, SKU strategy, or product type are ambiguous
- buyer deliverables are incomplete or unreviewed
- source-art rights are unclear
- mockup/media review is missing
- the packet would imply live Etsy mutation without explicit approval
