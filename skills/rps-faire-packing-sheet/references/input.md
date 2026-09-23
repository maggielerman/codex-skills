# Input and extraction

The script accepts a JSON object with `verified_at` and an `orders` array:

```json
{
  "verified_at": "2026-09-21T12:00:00-04:00",
  "orders": [{
    "order_id": "EXAMPLE123",
    "customer": "Example shop",
    "status": "Unfulfilled",
    "ship_date": "Sep 25, 2026",
    "source_url": "https://www.faire.com/brand-portal/orders/observed-order-path",
    "verified_at": "2026-09-21T12:00:00-04:00",
    "expected_lines": 1,
    "expected_units": 5,
    "items": [{
      "sku": "ABC1001-8x10",
      "title": "Example art print",
      "size": "8 × 10 in.",
      "quantity": 5,
      "photo_path": "photos/ABC1001.jpg"
    }]
  }]
}
```

Photo paths are resolved relative to the JSON file. Optional `id` on each item should be the source line ID when identical SKU/size combinations occur more than once. Otherwise, the script derives a stable line ID from full SKU plus size. Quantities must be positive integer units. Canceled or unavailable lines require explicit reconciliation; do not silently drop them.

## Browser extraction

Inspect the current DOM before choosing selectors. The original Faire order table had product-name anchors with a test ID ending `-product-name-button`, a nearby image and variation, followed by SKU and quantity cells. This is a historical hint, not a stable API. Read the actual row structure and visible column headers each time; do not carry fixed ancestor counts across site changes.

Capture order rows directly from rendered DOM, including image `src`/`currentSrc`. Browser page-assets export is another supported way to save observed photos. For already observed public CDN URLs, an ordinary download such as curl can save images locally; do not access session cookies, undocumented endpoints, or hidden application state. If Chrome automation is blocked by another extension UI, pivot to an authenticated in-app browser when available; otherwise ask the user to dismiss the popup while continuing local work.

Unit quantities may read `5 cases (5 units)`. Preserve the literal source quantity text in evidence and parse the parenthesized unit count. Do not infer case pack size from price.

The original design uses a warm paper background, green accents, photo cards, and a serif customer heading. `assets/packing.html` retains that format while replacing order, totals, size, and verification date with generated data.

## Native Chrome save fallback

When browser automation is blocked but native Chrome controls remain available, use Save Page As → Webpage, Complete to capture the rendered order and local image files. Save into `work/`. Wait until the save completes and verify the saved HTML's order heading before navigating: Chrome can serialize the next page if navigation happens while a save is still running. Parse only the rendered order table from the saved HTML; do not rely on scripts or hidden state. Cross-check every SKU, ordered variation, and unit quantity with the available Faire pick-list CSV. Keep full page exports private under `work/`; generated packing sheets should contain only the packing details.
