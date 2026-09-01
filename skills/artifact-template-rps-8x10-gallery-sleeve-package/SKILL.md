---
name: artifact-template-rps-8x10-gallery-sleeve-package
description: "Create a presentation using the RPS 8x10 Gallery Sleeve Package template and its retained reference file. Use when the user selects this template, names RPS 8x10 Gallery Sleeve Package, or explicitly invokes $artifact-template-rps-8x10-gallery-sleeve-package. Create an 8x10 retail package front for RPS print sets using the sophisticated gallery sleeve layout with editable product art, title, specs, price, and micro SKU."
---

# RPS 8x10 Gallery Sleeve Package

Create a new presentation from this template. Keep the reference file unchanged.

## Workflow

1. Read `artifact-template.json` and resolve its paths relative to this skill directory.
2. Load [@presentations](plugin://presentations@openai-primary-runtime) and invoke its reference/template workflow with the retained file.
3. Treat the user's prompt and available sources as the content input. Do not invent facts merely to fill a template slot.
4. Clone or import the reference instead of replacing its visual system with generic defaults.
5. Render and verify the finished presentation, then return the final artifact.

## Fidelity

Preserve source slides, layouts, masters, typography, geometry, images, charts, tables, and recurring slide chrome.

User instructions control requested content and explicit deviations. The retained reference controls layout and formatting where the user has not requested a change.
