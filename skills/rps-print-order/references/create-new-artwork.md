# Create a New Artwork Folder and Print File

Use this route only when the stable SKU has no usable prepared folder or Photoshop artwork. It is a last-resort production route, not a fallback for incomplete Creative Cloud discovery.

## Prove that the artwork is genuinely new

1. Search the current Creative Cloud folder hierarchy by exact stable SKU and inspect current variant-SKU folders when the ordered and stable SKU differ.
2. Confirm in both Photoshop and Creative Cloud that no approved exact-size document or other approved source size exists. A missing, empty, weak, or globally ranked search result is not proof of absence.
3. Open the canonical Shopify product for the stable SKU, including for a Faire order, and record its title, orientation, product media, and any explicit artwork/source information.
4. If an approved size exists, switch to [create-missing-size.md](create-missing-size.md). If folder or artwork absence cannot be confirmed, stop the line instead of creating replacement artwork.

## Establish the cloud structure

1. Identify the highest-resolution authorized source that exactly matches the Shopify product. Prefer clean, flat, front-facing artwork. Do not use a framed-room mockup, lifestyle photograph, thumbnail, or browser preview as the production image.
2. Create a root folder in the current Adobe Creative Cloud SKU folder system named `STABLESKU-Title`, using the canonical Shopify title.
3. Create a Photoshop document at the exact ordered physical dimensions, Shopify-derived orientation, and 300 pixels per inch. Use RGB Color, 8 Bits/Channel, and a white background unless the artwork requires a documented exception.
4. Place the source artwork as an embedded layer above the background.
5. Immediately save the cloud document inside the new folder using `SIZE-STABLESKU.psdc`, for example `8x10-RNW1004.psdc`, before substantial enhancement.

The cloud `.psdc` is the production master. A downloaded image may be a temporary source layer only. Do not create a local PSD master, save production work in a Codex work folder, print the downloaded image, or submit a job until the active Photoshop document is the correctly named cloud `.psdc` in the new current SKU folder.

## Choose the source and enhancement path

Default to the highest-resolution authorized original and ordinary, non-generative placement, scaling, and reframing. Search for a better authorized original before using generative tools when the product image is too small or is only a mockup. Confirm that any found original is the same sold artwork.

Use generative upscaling or edge expansion only when the authorized original cannot support the required canvas through ordinary preparation and the result remains faithful to the sold product. Never use generation to replace the core artwork, rewrite text, signatures, dates, typography, figures, or recognizable composition.

Review the final image against the Shopify product media for invented or damaged text, anatomy or geometry errors, obvious repeated texture, edge seams, halos, softness, orientation, and mismatch with the sold product image. Keep the result editable and save the final cloud document.

If no adequate authorized source can be found or produced, do not invent unrelated artwork; report that line as not queued.

## Queue through the proof gate

1. Reopen Image Size as a readback check and confirm the cloud document's folder, `.psdc` name, inches, pixels, 300-ppi resolution, orientation, layers, and visible composition.
2. Follow [submit-print-job.md](submit-print-job.md) and submit one proof copy.
3. Submit `quantity - 1` as a separate job and pause/hold it. Skip the remainder when quantity is one.
4. Read back both jobs before starting another created SKU. Both must carry the expected cloud `.psdc` name, printer, paper, and orientation when exposed; only the remainder is intentionally held.
5. Close the Photoshop document after submission and verification.

The held remainder stays paused until the user physically reviews and approves the proof.
