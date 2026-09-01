# Shop Uploader Template Contract

Shop Uploader templates in this plugin are contracts and examples only. Upload
files must be generated and preserved in `rps-etsy`.

## Rules

- Start existing-listing updates from a fresh Shop Uploader export for the exact target listing IDs.
- Preserve the source export and full header in `docs/evidence/active/<project>/`.
- Use the typed reusable template set in `rps-etsy` to choose the correct shape.
- Keep plugin fixtures header-only and marked `TEMPLATE-DO-NOT-UPLOAD`.
- Do not use historical rapid drafts, minimal/safe CSVs, or regression packets as template sources.
- Do not call a media/file CSV upload-ready until URLs, media review, and file manifests have passed the workflow checks.

## Current Template Source

Resolve the `rps-etsy` root using `repository-resolution.md`, then use
`docs/evidence/templates/shop-uploader/digital-downloads/digital-prints-2078-template-set-2026-05-27/`
relative to that root.
