# Review Board Format

## Requirements

- White or neutral background.
- Clear option labels: `A1`, `A2`, `A3`, etc.
- Filename or pack option name visible below each image.
- Keep options comparable in size.
- Include only images under review; do not mix approved and rejected items without labels.

## Recommended Outputs

- `review-board.jpg`
- `manifest.json`
- Final selected image(s) in `composited-examples/`
- Raw generated base(s) in `raw-bases/`

## Notes

When an option is approved, update the manifest with:

- `status`
- `preferredOption`
- `approvalContext`
- intended `surfaces`
