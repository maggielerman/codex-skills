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
- `working-modes`
