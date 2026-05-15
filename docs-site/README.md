# Maggie Lerman Codex Skills Site

This is the public marketing and documentation site for Maggie Lerman's Codex skills library.

It is intentionally about sharing reusable workflow patterns, making the catalog browsable, and giving people enough context to copy or adapt the skills from the public repo.

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

Run this when checking whether the generated public catalog is stale:

```bash
npm run catalog:check
```

## Content intent

The docs should help readers answer:

- What is this workflow for?
- Which skill or plugin should I use for my workflow?
- How do I install it without breaking bundled scripts or references?
- How do I invoke it inside my own repo?
- What should I troubleshoot before opening an issue or adapting the workflow?

Keep internal repository maintenance guidance in the root README, CONTRIBUTING, AGENTS, and generated suite catalog.
