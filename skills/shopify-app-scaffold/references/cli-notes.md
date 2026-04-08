# CLI Notes

The scaffold script is designed around the installed Shopify CLI.

Known local command shape when this skill was created:

- `shopify app init --template reactRouter --flavor typescript`
- `shopify app config link`
- `shopify app env pull`
- `shopify app env show`

Behavior to expect:

- the installed CLI may be behind the latest published CLI
- `shopify app init` can drift over time, so prefer the installed help output over memory
- do not auto-upgrade the user's global CLI unless they explicitly ask

Useful checks:

```bash
shopify version
shopify app init --help
shopify app config --help
shopify app env --help
```
