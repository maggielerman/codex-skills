# Plugin Packages

This directory stores installable custom Codex plugin packages.

Rules:

- Package only custom reusable plugins, not every installed plugin.
- Keep plugin folders self-contained and preserve `.codex-plugin/plugin.json`.
- Update [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) when adding, removing, or renaming a packaged plugin.
- Treat these as durable install sources indexed separately from the generated standalone skills catalog.

Current packaged plugins:

- `context-layer`
- `design-system-first`
- `jamstack-expert`
- `motion-design-director`
- `project-tranche-orchestrator`
- `rps-etsy-ops`
- `rps-fulfillment`
- `working-modes`

`rps-fulfillment` bundles `rps-faire-packing-sheet` and `rps-label-4up`. Keep its skill copies synchronized with the corresponding standalone sources in `skills/` when updating either workflow. Customer orders, photos, labels, and generated documents stay outside the repository.
