---
name: tmora-print-proof-deck
description: Use when creating or revising TMORA client-facing landscape-letter print proof packets, postcard front/back comparisons, triptych proofs, or final proof PDFs for Mary.
---

# TMORA Print Proof Deck

## Outcome

Build an editable native **Figma Design** proof packet at true landscape US Letter size (11 × 8.5 inches, 792 × 612 Figma units), then leave the ordered pages ready for one PDF export. Do not use Figma Slides and never flatten complete proof pages into images.

## Required sub-skills

- **REQUIRED:** Use `figma:figma-use` for every Figma read or write.
- Use `figma:figma-generate-library` when creating or changing the reusable proof components, variables, or text styles.
- Use `google-drive:google-sheets` to read the shared Artwork Data sheet.
- Use `pdf:pdf` to inspect supplied reference PDFs and visually verify exported PDFs when one is provided.

## Established Figma system

- Figma Design file: https://www.figma.com/design/o8FYnmAe5XhPJisTs1MOQm
- Shared Sheet: https://docs.google.com/spreadsheets/d/1CXU9FpM8Jn3EKTzU2ywTEQpodLHZBR9c6x5qmHV8Tg0/edit
- Sheet tab: `Artwork Data`
- Reusable components on the `Components` page:
  - `TMORA / Proof Cover / 11×8.5`
  - `TMORA / Proof Page / 11×17 + Info Card / 11×8.5`
  - `TMORA / Proof Page / 4×6 Postcard Front + Back / 11×8.5`
  - `TMORA / Proof Page / 8×10 Triptych + Info Card / 11×8.5`

Discover components by exact name rather than remembered node IDs. Preserve the existing info-card and postcard-back components.

## Source contract

Written fields come from `Artwork Data`: `sku`, `artist`, `artist_years`, `title`, `artwork_year`, and `material`.

- Derive the base SKU with `TMORA\d+` from the Sheet SKU.
- `artist_years`, `artwork_year`, and `material` are optional.
- Normalize a leading comma from `artwork_year` for display when the title and year render on separate lines.
- Ignore the `artwork_image` column for proof images. Do not use Shopify-hosted images.
- Proof images must come from the supplied local artwork folder and all of its SKU-named subfolders.
- Match images to the correct SKU and role before uploading. Stop only when the filename/folder identity is genuinely ambiguous.
- No recommendation is inferred from option order, filenames, or layout. Show a
  recommendation badge only when explicit source data identifies the recommended
  front or fronts.

## Page selection

Create one cover, then add only the proof pages supported by the local source files. Page types have fixed contents:

- Three ordered 8×10/10×8 panel files: the three prints plus their matching 6×4 info card.
- A local 11×17/17×11 print: the large print plus its matching 6×4 info card.
- A local 4×6/6×4 postcard front: the front plus its matching 4×6 postcard back.

The info card on a print page and every postcard front/back are the same physical 4×6 rectangle. Orientation rotates the rectangle; it never changes its scale.

Order pages by base SKU and keep related formats together. Name top-level pages with a two-digit prefix so Figma and PDF order are unambiguous.

## Workflow

1. Inspect the reference PDF only for visual hierarchy and page inventory. Do not reuse an old Slides template.
2. Inventory every supplied SKU subfolder and build an explicit manifest of base SKU, page types, and exact local file-to-slot mappings.
3. Read the Sheet and reconcile every manifest record to one Sheet row. Confirm title, artist, year, material, and base SKU before creating pages.
4. Discover the four reusable components by exact name. Confirm each master is 792 × 612 and exposes the expected text properties.
5. Create or clear a production page named `Proofs — [client/batch] — 11×8.5`.
6. Create component instances in final PDF order and set text through component properties. Keep the cover linked to its master.
7. Detach only image-bearing instances after text is correct. Find local image targets by their semantic names:
   - `Image Slot / 11×17|17×11 Print — upload local file (FIT)`
   - `Image Slot / 6×4 Info Card — upload local file (FIT)`
   - `Image Slot / 4×6|6×4 Postcard Front — upload local file (FIT)`
   - `Image Slot / 4×6 Postcard Back — upload local file (FIT)`
   - `Image Slot / Panel 1|2|3 — upload local file (FIT)`
8. Upload each local source with `figma_upload_assets` using `FIT`. Never crop the proof image.
   After a successful upload, clear the placeholder stroke on the populated image rectangle.
9. Apply the fixed physical visualization dimensions below. Never size an object to fill available layout space.
10. Hide the internal `Image Source Note` layer on production pages. It may remain in the reusable master as hidden workflow documentation.
11. Set `{format: "PDF"}` export settings on every ordered top-level proof page.
12. Audit and screenshot every page before handoff.

## Image quality

- Use the original local artwork as the source of truth.
- Figma upload assets must be under 10 MB. If an original exceeds the limit, create a temporary high-quality JPEG derivative in the task `work/` folder only: preserve aspect ratio, use a 3000 px maximum dimension, 4:4:4 sampling, and quality 95.
- Do not replace the original production file or treat the temporary derivative as a new source asset.
- At the proof page's printed size, the embedded pixel dimensions must support at least 300 ppi. Text remains native/vector in the PDF.

## Fixed physical visualization scale

Use one scale across the whole packet: **20 Figma units per physical inch**.

| Physical object | Portrait dimensions | Landscape dimensions |
|---|---:|---:|
| 4×6 postcard/info card | 80 × 120 | 120 × 80 |
| 8×10 print | 160 × 200 | 200 × 160 |
| 11×17 print | 220 × 340 | 340 × 220 |

Use the `TMORA Print Dimensions` variables `proof-visual/4in`, `6in`, `8in`, `10in`, `11in`, and `17in`. Rotate by swapping width and height bindings. Never calculate a new scale per page, per orientation, or per number of images.

- An 11×17/17×11 print must be visibly and proportionally much larger than its 6×4 info card.
- Every 8×10/10×8 print uses the same rotated 160 × 200 rectangle across the packet.
- A 6×4 info card is exactly the same size as a landscape 6×4 postcard front.
- A 4×6 postcard back is exactly the same rectangle rotated to 80 × 120.
- Preserve triptych panel order; wrapping is allowed if future mixed orientations cannot fit in one row, but scaling is not.

## Content and visual contract

- Charcoal `#2A2725`; gold `#B19149`; cream `#F4EFE6`; muted `#BEB5AA`.
- Libre Baskerville for display and artwork metadata; Source Sans Pro for labels and structural text.
- Left metadata column: artist, optional artist years, italic title, normalized artwork year, optional material, gold rule, format description.
- Right proof area: full local image(s), never a Shopify URL, screenshot, or flattened proof page.
- Print pages always include the matching local info-card image; postcard pages always include both matching front and back images.
- Square edges, thin gold rules, no shadows or gradients, generous negative space.
- Long titles must use a fixed-width, height-resizing text box and must never be clipped or manually truncated.

## Final verification

Use a read-only `use_figma` audit and screenshots of every ordered top-level page. Confirm:

- Every page is exactly 792 × 612.
- Page count and order match the manifest.
- Every named image slot contains exactly one IMAGE fill with `scaleMode: FIT`.
- Every rendered proof object matches the fixed-dimension table; compare dimensions across all pages, not just within one page.
- Each image is matched to the correct SKU and role; triptych panels are left-to-right in source order.
- Sheet artist, title, year, material, and SKU match the rendered page.
- Optional blank fields do not create incorrect punctuation.
- No clipped text, placeholder image, visible internal source note, swapped artwork, overlap, or out-of-bounds node remains.
- Every page has PDF export settings.

Report the Figma Design link, production page name, page count, source exceptions, and the final user action: select the ordered top-level proof pages and choose `Export to PDF`. Do not use computer-use clicking for the export.

The files under `templates/tmora_print_proof_deck.py` and `templates/metadata.example.json` are legacy non-Figma fallbacks. Do not use them unless the user explicitly requests a scripted PDF fallback.
