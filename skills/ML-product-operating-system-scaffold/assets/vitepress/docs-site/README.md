# Docs Site

This folder wraps the docs site for local development.

## Local Dev
- `npm install`
- `npm run dev`

## Cloudflare Pages
If your docs live at repo root (for example, `DOCS/` or `docs/`), keep Root Directory at the repo root, set Build command to `npm --prefix docs-site run build`, and set Build output directory to `DOCS/.vitepress/dist` or `docs/.vitepress/dist`.
If you use `wrangler.toml`, keep it aligned with the settings in the Cloudflare dashboard.
