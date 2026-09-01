# TMORA Figma Slides production specification

## File contract

- Template: https://www.figma.com/slides/FIHkV6Cv9TeykmzbCrbwte
- Template section: `Reusable Templates`
- Example section: `Waters Example`
- Template slides remain skipped; cloned production slides are unskipped.
- PDF is the default export format.

## Template discovery

Do not depend on Figma Slides names; the editor automatically renumbers them. Inside `Reusable Templates`, resolve each skipped slide by its stable layer signature:

- Cover: contains `Field / Deck Title` and no `Image / ...` rectangles.
- Print set: contains `Image / Set Cover` and `Image / Panel 1`.
- Postcard options: contains `Image / Front A` and `Image / Back`.

## Named text layers

### Cover

- `Field / Deck Title`
- `Field / Date`
- `Field / Prepared By`

### Proof slides

- `Info / Artist`
- `Info / Artwork`
- `Info / Material`
- `Info / Sizes`
- `Info / SKU`
- `Section / Label`
- `Section / Description`
- `Proof Label / ...`

## Named image layers

### Print set

- `Image / Set Cover`
- `Image / Panel 1`
- `Image / Panel 2`
- `Image / Panel 3`

### Postcard options

- `Image / Front A`
- `Image / Front B`
- `Image / Front C`
- `Image / Back`

Each image rectangle has a matching `Template Hint / Image / ...` text node and may carry a visible placeholder stroke. After a successful upload, hide the hint and set the populated production rectangle's `strokes` to `[]`. Use `FIT` for proof images.

## Optional nodes

- `Badge / Recommended`
- `Badge / Recommended Text`
- Unused proof labels, image rectangles, and hints

The reusable badge pair stays hidden by default. `recommended_fronts` is the only authority for showing badges. Move one pair below the first recommended front and clone the pair for additional recommended fronts. Missing or empty recommendation data produces no badge. Hide other optional nodes instead of leaving blank placeholders in a production slide.

## Data shape

Use `templates/deck-data.example.json` as the portable input shape. `recommended_fronts` is an array of front labels and may be empty or contain multiple values. Never infer a recommendation from option order. `assets` values may be local file paths, Shopify-hosted originals, or extracted source-PDF images. Identity and role must be reconciled before upload.

## Export limitation

The Figma connector can create, populate, proof, and configure Slides through the Plugin API. It does not provide a downloadable final PDF artifact. The finished deck therefore ends with one user-performed Figma `Export to PDF` action; no computer-use automation is required.
