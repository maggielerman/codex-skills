# Submit and Verify a Photoshop Print Job

Use this procedure for every artwork submission, whether the file already existed or was created during the order.

## Preflight the active cloud document

Before opening Print, confirm all of the following in desktop Photoshop:

- The active document is the expected saved Creative Cloud `.psdc` inside the current stable-SKU folder. Do not print a downloaded source image, browser preview, local PSD, or unsaved document.
- Its size prefix and stable SKU match the manifest.
- Its canvas inches, pixel dimensions, 300-ppi resolution, and portrait/landscape orientation match the manifest values derived from Shopify.
- The visible composition is upright and matches the sold product. For a landscape `5x7`, the canvas and expected sheet are `7 in x 5 in` or `2100 x 1500 px`, not portrait.

If any preflight item fails, stop without opening Print.

## Submit through the established Photoshop flow

1. Open the Photoshop print dialog from the active cloud document.
2. Confirm the locked order printer, exact paper preset, Normal quality, copies, and visible portrait/landscape preview. The preview must show a landscape composition on a landscape sheet and a portrait composition on a portrait sheet.
3. Do not infer orientation from a `5x7` or `5x7.Fullbleed` label. If the Photoshop or macOS sheet exposes an orientation control, set it to the manifest value and recheck the preview.
4. Open **Print Settings** only when the printer, paper, quality, or orientation is wrong, unclear, or unavailable. Do not reopen it routinely when all visible values are already correct.
5. Stop and cancel the submission if Photoshop or macOS reports clipping, an image larger than the printable area, unexpected rotation, scaling, or auto-orientation. Correct the document or print layout and repeat the full preflight; do not automatically choose **Proceed**.
6. Submit the job. If macOS says the printer is stopped, choose **Add to Printer**, never **Resume**, unless the user explicitly asked to resume the printer.

## Read back before continuing

For an approved existing-size file, the job may carry the full ordered quantity. For a file created or changed during this order, submit a one-copy proof and a separate `quantity - 1` remainder, then hold only the remainder at the job level.

Before moving to another created SKU, verify in Print Center/CUPS:

- the document name is the expected size-prefixed cloud `.psdc`
- printer, paper/media, and copies match the manifest
- `orientation-requested` matches the Shopify-derived orientation when CUPS exposes it
- when CUPS does not expose orientation, record that limitation and rely on the completed visual print-preview check rather than assuming orientation from the media name
- the proof and remainder states are distinct and only the remainder is intentionally held at the job level

If the queued document name is a source image, local PSD, browser asset, or other unexpected name, or if any setting does not reconcile, keep the printer paused, submit no additional artwork jobs, and report the exact mismatch. Do not call the line correctly queued until the mismatch has been safely resolved and read back again.
