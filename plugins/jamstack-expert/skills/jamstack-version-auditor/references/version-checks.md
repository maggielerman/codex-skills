# Version Checks

## Package Coverage

Core packages:

- Tailwind: `tailwindcss`, `@tailwindcss/cli`, `@tailwindcss/postcss`, `@tailwindcss/vite`, `prettier-plugin-tailwindcss`
- Eleventy: `@11ty/eleventy`, `@11ty/eleventy-img`, `@11ty/eleventy-navigation`, `@11ty/eleventy-plugin-rss`, `@11ty/eleventy-plugin-syntaxhighlight`, `@11ty/eleventy-plugin-vite`
- Templates/content: `nunjucks`, `markdown-it`, `gray-matter`, `slugify`, `luxon`, `date-fns`
- Alpine: `alpinejs`, `@alpinejs/collapse`, `@alpinejs/focus`, `@alpinejs/intersect`, `@alpinejs/persist`, `@alpinejs/mask`, `@alpinejs/csp`
- Build: `vite`, `postcss`, `autoprefixer`, `lightningcss`, `sass`, `npm-run-all`, `concurrently`
- Deploy/static: host adapters or CLI tools used by the repo, such as Netlify, Vercel, Cloudflare Pages/Wrangler, GitHub Pages helpers

## Installed-Version Inspection

Use lockfiles for exact resolved versions. `package.json` ranges are intent, not proof.

Useful commands:

```bash
npm ls tailwindcss @11ty/eleventy alpinejs --depth=0
pnpm list tailwindcss @11ty/eleventy alpinejs --depth=0
yarn list --pattern "tailwindcss|@11ty/eleventy|alpinejs"
bun pm ls
```

For workspaces, run from the workspace root and inspect per-package manifests.

## Latest Stable Inspection

Use `npm view <package> version dist-tags --json`. Treat `latest` as stable unless the project itself documents a different stable tag. Treat `next`, `beta`, `alpha`, `canary`, `insiders`, and dated internal builds as prerelease or non-default.

## Migration-Risk Notes

Tailwind v3 to v4:

- Check CSS entrypoint and PostCSS/Vite integration.
- Check custom theme/config, plugins, `@apply`, arbitrary variants, and content scanning.
- Verify output CSS and visual regressions after migration.

Eleventy major updates:

- Check Node version support first.
- Check config file format, plugins, collections, pagination, passthrough copy, data cascade, and incremental build behavior.
- Run a full build and inspect generated URLs/output.

Alpine updates:

- Check CDN pinning versus npm import.
- Check plugin versions align with Alpine core.
- Test interactions, transitions, `x-cloak`, focus behavior, and CSP mode.

General rule: a major update deserves a migration note and build/browser verification; a patch or minor update may still be deferred if it is unrelated to the user task.
