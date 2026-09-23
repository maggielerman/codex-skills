---
name: rps-faire-packing-sheet
description: Create searchable, offline HTML packing checklists for Rock Paper Scissors Faire orders, using a photo-card format with titles, SKUs, ordered sizes, quantities, saved checkmarks, and a print view. Use for one order or all open Faire orders.
---

# Faire packing sheets

Create one self-contained HTML packing checklist per order and an index linking the batch. The bundled template uses a warm paper background, green accents, and product photo cards.

## Source and scope

- Read the live Faire Brand Portal. For “all open orders,” inspect both **New** and **Unfulfilled**, every results page, with search and optional filters cleared. Exclude Fulfilled and Canceled; record when the inventory was checked.
- Capture customer, exact order ID, status, ship date, and every line's title, full variant SKU, ordered size, unit quantity, and matching photo. Faire case counts are not unit quantities: use the displayed units in parentheses where present. Keep different variants separate.
- Use the order's own photo and variant. Normalize display-only `05x7` to `5 × 7` if useful; preserve the SKU exactly. Do not assume every order is 5x7 like an earlier example.
- Keep raw order-row evidence under the task's `work/` folder. Check line count and summed units against the rendered order table or a fresh Faire pick-list CSV. If a source is incomplete, state the gap instead of labeling the batch complete.
- This workflow creates local documents. It does not accept orders, alter quantities or ship dates, buy labels, send messages, mark shipped, print, or change printer queues.

## Build

Read [references/input.md](references/input.md) for the input shape and browser extraction notes. Download only the product-photo URLs observed in the order to local files. Verify image content; never silently substitute another SKU's art. Use the current browser tools and their documented APIs for live extraction.

Run the bundled standard-library Python generator:

```sh
python3 scripts/build_packing_sheets.py /path/to/work/orders.json --output /path/to/outputs/faire-packing-sheets
```

Resolve the script path relative to this skill directory. Use a fresh dated output directory on reruns so earlier documents and browser packing progress remain recoverable. The generator produces individual HTML sheets, matching CSVs, an index, and a manifest. It checks expected counts, image signatures, and unique order/line identifiers before writing the sheets.

Each HTML embeds its photos and has title/SKU/size search, All / Still to pack / Packed filters, full-quantity checkboxes, unit and line progress, undo, photo enlargement, and print styling. Progress is isolated by order ID and line identity in localStorage. Checkmarks are browser-local and do not establish physical packing or Faire fulfillment.

## Verify and deliver

Open the index and a generated sheet in the browser. Check every sheet's card count, summed quantity, and loaded photo count against the manifest. Exercise search, one checkmark, reload persistence, Still to pack, undo or uncheck, and photo enlargement. Restore any test checkmark before delivery. Check mixed-size rows and a narrow screen when present. Report totals and any unresolved coverage gaps; link the index and leave it open for the user.
