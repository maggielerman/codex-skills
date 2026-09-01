# Skill contract tests

## Baseline failure

The legacy skill prescribed ReportLab and a Python generator, created only a PDF artifact, and contained no native Figma Slides template, cloning, layer mapping, image-upload, skipped-template, or connector-export limitation contract.

## Scenario

“Create a TMORA proof presentation from the newest artwork packet, matching the most recent Waters proof deck, and make it reusable.”

## Passing behavior

- Uses native Figma Slides through `figma-use` and `figma-use-slides`; no computer-use clicking.
- Opens the established template and discovers slides by section plus stable layer signature rather than unstable slide names or stored IDs.
- Keeps template slides skipped and clones only the necessary slide types into an active production section.
- Reconciles every proof asset to a SKU and named image role before upload.
- Reads recommendations only from `recommended_fronts`; supports zero or multiple recommendations and never defaults to B.
- Uses `figma_upload_assets` with `FIT`, hides template hint text after upload, and removes placeholder strokes from populated production rectangles.
- Preserves same-size physical scale and optional recommendation logic.
- Uses PDF as the default output and clearly identifies the final single manual Figma export action.
- Audits structure and screenshots every active slide before completion.

## Recommendation regression

The approved Waters fixture uses `recommended_fronts: ["A", "C"]`. A passing implementation shows badges below A and C, shows none below B, and leaves the reusable template badge pair hidden. A fixture with `recommended_fronts: []` shows no badges.

## Independent workflow test

Clone the reusable cover and postcard-option templates for a separate one-front artwork. Populate all named text fields, upload one front and one back with `FIT`, clear both populated rectangles' placeholder strokes, hide unused B/C targets and all recommendation badges, apply PDF export settings, visually audit both slides, then keep the test section skipped so it cannot enter a client export.
