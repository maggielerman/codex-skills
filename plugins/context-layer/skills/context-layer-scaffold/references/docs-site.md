# Docs Site

Docs site scaffolding is optional.

If enabled:

1. Copy `assets/vitepress/DOCS/.vitepress/config.ts` to `DOCS/.vitepress/config.ts`.
2. Copy `assets/vitepress/docs-site/` to `docs-site/`.
3. Replace placeholders in `docs-site/package.json` and `wrangler.toml`.
4. Add package scripts when `package.json` exists:
   - `docs:dev`
   - `docs:build`
   - `docs:preview`
5. Set `{{DOCS_SITE_ENABLED}}` to `true` in `.github/workflows/docs-site-sync.yml`.

If disabled, still create/update `.github/workflows/docs-site-sync.yml` with `{{DOCS_SITE_ENABLED}}` set to `false`, but make CI safe for repos without package infrastructure.

Do not assume the docs site should be generated unless Maggie explicitly says yes.
