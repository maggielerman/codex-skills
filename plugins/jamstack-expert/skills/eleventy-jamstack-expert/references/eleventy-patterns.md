# Eleventy Patterns

## Files To Inspect

- `package.json`: Eleventy version, scripts, build pipeline, deployment scripts.
- `eleventy.config.js`, `.eleventy.js`, `eleventy.config.mjs`, or equivalent.
- Input/output directories and configured `dir.includes`, `dir.layouts`, `dir.data`, `dir.output`.
- `_data` and directory data files.
- `_includes`, layout files, macros, shortcodes, filters.
- Markdown/content directories and front matter conventions.
- Asset handling: passthrough copy, Vite, Lightning CSS, PostCSS, Tailwind CLI, image plugin, or custom scripts.

## Data Cascade Placement

- Global data: site name, navigation, global metadata, shared taxonomies.
- Directory data: defaults for a section, collection, or content type.
- Front matter: page-specific title, permalink, date, tags, layout, draft state.
- Computed data: derived URLs, titles, excerpts, social image values, section-aware metadata.
- Config global data: values that are truly build/config-level.

When a value feels duplicated across many pages, move it upward in the cascade. When a value is derived from other fields, compute it instead of copying it manually.

## Template Composition

- Layouts: page frame, document structure, metadata slots, shared chrome.
- Includes: repeated static fragments or components with a small context.
- Macros: parameterized components, especially buttons/cards/badges/forms.
- Filters: string/date/URL/array formatting.
- Shortcodes: reusable generated markup from config, especially cross-template-language fragments.
- Paired shortcodes: wrappers around body content.

## Collections

- Tags create collections. A content item can be in multiple collections.
- Use `collections.all` deliberately; exclude utility templates when needed.
- Sort collections explicitly when date/title/order behavior matters.
- Use `page.*` fields for item path, URL, and date when working with modern Eleventy collection item structures.
- Avoid using collection tags as public taxonomy labels unless the site intentionally shares that model.

## Tailwind In Eleventy

- Make sure the Tailwind scanner sees `.njk`, `.md`, `.html`, `.11ty.js`, and any component/data files that contain classes.
- Prefer explicit complete class strings in macros/includes.
- Avoid Nunjucks interpolation that hides full utility names from the scanner.
- If classes are generated from CMS or data values, map them to a controlled set of complete class strings.

## Deployment Checks

- Confirm the output directory matches host expectations.
- Confirm trailing slash/permalink behavior before changing URLs.
- Preserve redirects, headers, adapter config, and image/CDN assumptions.
- For Netlify/Vercel/Cloudflare Pages/GitHub Pages, inspect existing config before adding new defaults.
