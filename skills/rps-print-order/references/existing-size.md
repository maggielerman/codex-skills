# Existing Exact-Size Artwork

Use this route only when the ordered size already exists as an approved Photoshop cloud document inside the stable-SKU folder.

## Locate the file

1. Search for the stable SKU and enter the matching folder, for example `PXC10226-Blue Cat Gouache by Louis Wain`.
2. Inside that folder, identify the document whose size prefix exactly matches the order, such as `8x10-PXC10226.psdc`.
3. Treat a differently named variant as acceptable only when the folder is the stable-SKU match and the document is clearly the correct artwork and exact size. Do not accept a global fuzzy-search result merely because it contains similar characters.
4. If Photoshop search does not surface the file, locate it through Adobe Creative Cloud and open the cloud document in Photoshop. Do not print a lower-resolution browser preview as a substitute.
5. Confirm that the cloud document's orientation and canvas agree with the Shopify-derived manifest values. Stop on a mismatch instead of relying on automatic print rotation.

## Queue the approved file

1. Open the exact cloud document in Photoshop.
2. Follow [submit-print-job.md](submit-print-job.md), setting the full ordered quantity.
3. Close the Photoshop document after submission.

At batch readback, verify the cloud filename, printer, paper/media, orientation when exposed, copies, and queue state. Do not split an already approved exact-size file into proof and remainder jobs unless the user specifically requests a new proof.
