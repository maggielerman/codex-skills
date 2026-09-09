# Create a Missing Size in an Existing SKU Folder

Use this route when the stable-SKU folder and artwork exist but the ordered size does not.

## Create without changing approved originals

1. Inventory the sizes in the stable-SKU folder and confirm the exact ordered size is absent.
2. Choose the existing size that provides the strongest source for the new aspect ratio and composition. Resolution and edge content matter more than filename similarity.
3. Duplicate that Photoshop cloud document. Keep the source document unchanged.
4. Rename the duplicate using the exact ordered size and stable SKU, for example `8x10-PXC10029.psdc`, and retain it in the same stable-SKU folder.
5. Confirm the duplicate's portrait/landscape orientation from the Shopify-derived manifest. Change the duplicate's **canvas size first** to the exact ordered physical dimensions at 300 pixels per inch, anchored appropriately for the composition. For example, an `8x10` portrait document must have an `8 in x 10 in` canvas, which is `2400 x 3000 px` at 300 ppi; a `5x7` landscape document must be `2100 x 1500 px`. Preserve the established RGB, bit depth, background, and layer conventions unless the source requires a reasoned change.
6. After the canvas is correct, select the artwork layer or artwork layer group and use Free Transform to resize and reposition the artwork to fit the new canvas. Reframe for the new aspect ratio without stretching or changing the whole document through **Image Size**. Use generative expansion only when the transformed artwork leaves exposed areas that need new image content and it produces a clean, compositionally faithful result. Inspect seams, repeated forms, invented text, distorted figures, and abrupt borders before accepting a variation.
7. Save the cloud document, reopen **Image Size only as a readback check**, and confirm the saved document reports the exact ordered inches, pixel dimensions, and 300 ppi. Do not submit a proof from the filename or visible crop alone. Also confirm the final name, folder location, and visible composition.

Do not overwrite or rename the approved source size. Do not substitute that source size for the ordered size.

This is the required route whenever another approved size exists. Do not rebuild the artwork from a product image, use a custom batch/JSX transformation, save the production master locally, or print from a source image. If the cloud document cannot be duplicated, renamed, retained in the same current SKU folder, and verified, stop the line without queueing it.

## Queue through the proof gate

1. Follow [submit-print-job.md](submit-print-job.md) and submit one proof copy.
2. Submit `quantity - 1` as a separate job, then pause/hold that remainder. Skip this step when the ordered quantity is one.
3. Read back the proof and remainder before starting another created SKU. Both jobs must carry the expected size-prefixed `.psdc` name, printer, paper, and orientation when exposed; only the remainder is intentionally held at the job level.
4. Close the Photoshop document after the jobs are submitted and verified.

Do not resume the remainder until the user approves the physical proof.
