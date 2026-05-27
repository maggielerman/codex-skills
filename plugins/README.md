# Plugin Backups

This directory stores backups of custom local Codex plugins.

Rules:

- Back up only custom local plugins, not every installed plugin.
- Keep plugin folders self-contained and preserve `.codex-plugin/plugin.json`.
- Update [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) when adding, removing, or renaming a backed-up plugin.
- Treat these as durable backups and portable install sources, not as part of the generated skills catalog.

Current backed-up plugins:

- `context-layer`
- `design-system-first`
- `jamstack-expert`
- `project-tranche-orchestrator`
- `rps-etsy-ops`
