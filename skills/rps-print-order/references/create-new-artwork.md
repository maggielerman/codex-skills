# Create a New Artwork Folder and Print File

Use this route when the stable SKU has no usable prepared folder or Photoshop artwork.

## Establish the cloud structure

1. Identify the authorized product image or source artwork associated with the stable SKU.
2. Create a root Adobe cloud folder named `STABLESKU-Title`, using the catalog title when known.
3. Create a Photoshop document at the exact ordered physical dimensions and 300 pixels per inch. Use RGB Color, 8 Bits/Channel, and a white background unless the artwork requires a documented exception.
4. Place the source artwork as an embedded layer above the background.
5. Save the cloud document inside the new folder using `SIZE-STABLESKU.psdc`, for example `8x10-RNW1004.psdc`, before substantial enhancement.

## Choose the source and enhancement path

Default to generative preparation when the product image is already of decent quality:

1. Generatively upscale it enough to support the final 300-ppi canvas.
2. Reframe it for the requested aspect ratio.
3. Generatively expand missing edges when needed.

When the product image is very low quality, first search for a higher-resolution authorized original because generative tools work poorly from an inadequate source. Confirm that a found original is the same artwork. Expect that it may still need digital enhancement to match the product image and generative expansion for the new aspect ratio.

Choose between these paths by final visual quality, source fidelity, and production time. Searching for an original is the exception, not a mandatory step for every new file.

Review the final image for invented or damaged text, anatomy or geometry errors, obvious repeated texture, edge seams, halos, softness, and mismatch with the sold product image. Keep the result editable and save the final cloud document.

If no adequate authorized source can be found or produced, do not invent unrelated artwork; report that line as not queued.

## Queue through the proof gate

1. Submit one proof copy to the current order's exact printer and exact paper size.
2. Submit `quantity - 1` as a separate job and pause/hold it. Skip the remainder when quantity is one.
3. Close the Photoshop document after submission.
4. At batch readback, verify the proof plus held remainder equals the ordered quantity.

The held remainder stays paused until the user physically reviews and approves the proof.
