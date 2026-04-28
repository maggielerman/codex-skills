# Codex Skills Packs Docs Site

This is the customer-facing marketing and implementation docs site for the Codex skills packs.

It is intentionally about buyer setup, implementation, and troubleshooting. It is not the source of truth for maintaining this repository.

## Local development

```bash
npm install
npm run catalog
npm run dev
```

## Generated catalog

Skill and plugin pages are generated from repository metadata:

- `../skills/manifest.json`
- `../plugins/*/.codex-plugin/plugin.json`

Regenerate after changing suite metadata or plugin metadata:

```bash
npm run catalog
```

Run this when checking whether the generated customer-facing catalog is stale:

```bash
npm run catalog:check
```

## Content intent

The docs should help customers answer:

- What did I buy?
- Which skill or plugin should I use for my workflow?
- How do I install it without breaking bundled scripts or references?
- How do I invoke it inside my own repo?
- What should I troubleshoot before asking for support?

Avoid documenting this repository's internal maintenance process here. Keep repo maintenance guidance in the root README, CONTRIBUTING, AGENTS, and generated suite catalog.
