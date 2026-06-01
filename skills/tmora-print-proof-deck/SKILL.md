---
name: "tmora-print-proof-deck"
description: "Custom skill created by Maggie Lerman. Use when creating or revising TMORA, The Museum of Russian Art, print proof PDFs or option decks for Mary, museum gift-shop print files, postcard fronts/backs, 11x17 proofs, or packaging/layout option review."
---

# TMORA Print Proof Deck

Custom skill created by Maggie Lerman.

Use this skill for client-facing TMORA proof PDFs that show print files, sizes, front/back options, and recommendations. The goal is an editorial proof deck Mary can inspect quickly, not a contact sheet or a generic gallery.

## Required Inputs

- A folder of proof assets, usually grouped by size or format, such as `11x17`, `4x6 postcards/postcard fronts`, and `4x6 postcards/postcard backs`.
- A TMORA design system source if available. Prefer `TMORA_Design_System.md`, `tmora.tokens.json`, or `tmora.css`.
- Any reference deck or screenshot from a prior TMORA presentation when provided.

## Deck Structure

1. Cover page only: `Print Proofs and Options`.
2. One proof page per SKU/artwork. Do not add overview/contact-sheet pages unless the user asks.
3. Each proof page groups all related assets for that SKU:
   - 11x17 print and 11x17 info card, if present.
   - 4x6 info card, if present.
   - 4x6 front options, if present.
   - postcard backs, labeled `Back A` and `Back B`.
4. Include a source manifest CSV beside the PDF.

## Visual System

- Use TMORA charcoal background, gold accents, cream text, square edges, and no decorative shadows or gradients.
- Use serif for artist/artwork metadata, sans serif for proof labels and small structural text.
- Keep proof labels small, sans serif, uppercase, and gold. Examples: `4X6 A`, `4X6 B`, `BACK A`, `BACK B`, `11X17 INFO CARD`.
  Use `4X6 INFO CARD` when the info-card asset is a postcard-size card.
- Do not show raw filenames under proof images in the client deck.
- Footer rules are acceptable on proof pages. Do not put a footer on the cover if the user wants the cleaner reference style.

## Left Info Panel

Match the compact reference style:

- Artist name as the main serif line.
- Artwork title and year in italic serif.
- Short gold rule.
- Size lines, such as `Poster: 11x17 in.` and `Postcard: 4x6 in.`
- SKU in small print, such as `SKU: TMORA109`.

Set the column width so text wraps automatically inside the available left column. Do not manually insert line breaks into titles to force wrapping.

## Option Rules

- If a front has only one option, label it by size only, such as `4X6` or `11X17`; do not append `FRONT`.
- If a front has multiple options, label them by size and option, such as `4X6 A` and `4X6 B`.
- In current TMORA proof workflows, option `B` is the recommended front option when multiple front options exist.
- Place a `RECOMMENDED` badge below the recommended artwork with a clear gap. It must not touch or overlay the artwork.
- Back labels are `Back A` for the info-card back and `Back B` for the postal/address back unless the user gives a different mapping.

## Scale Rules

- All 4x6 components on the same page must share the same physical scale.
- Portrait 4x6 fronts and info backs should render at the same dimensions.
- Landscape postal backs should render as the same scale rotated, not visually larger or smaller.
- Landscape and portrait 11x17 artwork options should render at the same physical 11x17 scale; labels should sit just above the rendered artwork, not at the top of a larger fitting box.
- Info-card assets named like `TMORA###-info-card.png` should render at 4x6 scale unless the asset path or name explicitly marks it as 11x17.
- Do not let image-fit logic make same-size proofs appear different just because one is portrait and another is landscape.

## Asset Grouping

- Infer the SKU from filenames when present, such as `TMORA110`.
- If postcard back filenames use ordered prefixes instead of SKUs, map them consistently:
  - `01-` -> `TMORA108`
  - `02-` -> `TMORA109`
  - `03-` -> `TMORA110`
  - `04-` -> `TMORA111`
  - `05-` -> `TMORA112`
  - `06-` -> `TMORA113`
- Extract artist/title/year from the back/info-card design when available. If OCR is unavailable, inspect the images visually or use known metadata from the current packet.

## Implementation Notes

- Use the `pdf` skill for generation and rendering QA.
- `reportlab` is appropriate for scripted PDF generation.
- Start from `templates/tmora_print_proof_deck.py` for a reusable PDF generator.
- Use `templates/metadata.example.json` as the metadata shape for artist/title/year, SKU order, back-prefix mapping, and the recommended option.
- Render every rebuild with `pdftoppm` and inspect at least a contact sheet plus any pages affected by comments.
- Keep generated outputs in `output/pdf/` and temporary renders in `tmp/pdfs/`.

Template command:

```bash
python3 templates/tmora_print_proof_deck.py \
  --source-root "/path/to/print files" \
  --metadata templates/metadata.example.json \
  --output-dir output/pdf \
  --date "May 2026" \
  --prepared-by "Maggie Lerman\nRock Paper Scissors"
```

## Review Loop

For PDF comments, change the generator/source script, not only the already-built PDF. Rebuild the PDF after each round so the deck stays reproducible.

Before final response:

- Confirm page count.
- Confirm all expected proof assets are represented.
- Confirm no raw filenames are visible in the PDF.
- Confirm 4x6 scale is consistent.
- Confirm recommendations appear only where multiple front options exist.
