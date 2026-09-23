---
name: rps-label-4up
description: Combine shipping-label PDFs into print-ready US Letter sheets with four equal quarters. Use for Faire, UPS, USPS, or other supplied labels requested as 4-up, quarter-sheet, or four equal labels per page.
---

# Shipping labels on four equal quarters

Use the user's established layout: US Letter portrait (612 x 792 pt), divided into four **4.25 x 5.5 inch** quarters. This is not an Avery 4 x 5 template. Center each label upright in its quarter, preserving aspect ratio with at least 9 pt (1/8 inch) clearance on every side. Do not add captions or cutting lines unless requested.

## Prepare

- Read the PDF skill and follow its applicable artifact and visual-review requirements. Use the available workspace dependency tool to locate Python with Pillow, pypdf, and reportlab, plus Poppler for rendering.
- Inspect every supplied PDF page. Count label pages, not files: a PDF may contain multiple distinct package labels. Preserve the supplied file order and page order; fill top-left, top-right, bottom-left, bottom-right. Leave unused quarters blank. More than four labels require additional sheets; never silently discard pages or duplicate a label to fill a gap.
- Use the helper below. Inputs are preserved, and existing outputs are refused. Keep customer addresses and tracking numbers in task files, never in the installed skill.

```bash
python scripts/build_label_sheet.py --mode auto --single-sheet --output /path/to/outputs/shipping-labels-letter-4up.pdf /path/to/label1.pdf /path/to/label2.pdf
```

Resolve the script relative to this skill's directory. Quote paths containing spaces. Omit `--single-sheet` when multiple sheets are appropriate; it otherwise stops if more than four labels are supplied.

## Choose the source mode

- **`--mode auto`** (default) extracts eligible image-only labels and preserves full PDF pages for labels with other content, including vector carrier logos. It reports each fallback. Review both kinds in the rendered sheet.

- **`--mode image`** for visually inspected, image-only shipping labels such as eligible Faire/UPS exports. It extracts the one embedded image per page, trims only exterior pure-white vertical space, and retains the full image width (including barcode quiet zones). It embeds original pixels without resampling; placement alone scales the image. This also avoids the stretched page-image ratio in some Faire exports. Verify the extracted image's orientation and all content against the source before use. The helper rejects text, extra images, annotations, and unsupported drawing operations (a white background before the image is allowed) instead of losing them.
- **`--mode page`** preserves the entire visible PDF page, including vector text and barcodes. It normalizes page rotation and scales proportionally without rasterizing or cropping. Use for other PDFs or when extraction is unsuitable. Inspect for large blank borders, clipped annotations, and layout; a page with multiple labels or unrelated content requires task-specific preparation first.
- Preserve barcode, routing, address, package number, service, reference, and footer content. Never redraw barcodes or reinterpret address text. Label formatting does not authorize purchasing labels, changing orders, or submitting a print job.

## Verify and deliver

The helper checks Letter dimensions, sheet count, slot bounds, and (in image mode) exact embedded-pixel hashes. Render **every** output page with Poppler and inspect all quarters for complete addresses/barcodes, upright orientation, correct order, and no clipping. Automated checks do not prove scanner readability.

Deliver the PDF with: **US Letter, portrait, Actual Size / 100%, one page per sheet**. The PDF is already four-up; do not select four pages per sheet again. If asked to add a label later, rebuild from the original label PDFs, not from the already imposed sheet.
