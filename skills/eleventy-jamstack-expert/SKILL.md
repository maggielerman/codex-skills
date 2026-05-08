---
name: eleventy-jamstack-expert
description: 'Eleventy/11ty, Build Awesome, Nunjucks, and JAMstack expert workflow. Use when working with .eleventy.*, eleventy.config.*, @11ty/eleventy, Build Awesome/Pro, .njk, Nunjucks includes/macros/layouts, _data, _includes, collections, pagination, shortcodes, filters, static assets, or deployments.'
---

# Eleventy JAMstack Expert

Use this skill to work as an Eleventy/Nunjucks/JAMstack specialist. Treat Build Awesome as the continuation/rebrand path for Eleventy, with Build Awesome Pro as optional paid workflow/services on top. Favor static-first architecture, small build-time data transforms, clear template composition, and progressive enhancement over app-like client complexity.

## Start Here

1. Inspect `package.json`, Eleventy config shape, input/output directories, scripts, template formats, passthrough copy, bundler/CSS pipeline, and deployment target.
2. If dependency currency, Node support, or migration advice matters, pair with `jamstack-version-auditor` before recommending Eleventy, plugin, bundler, or runtime upgrades.
3. Map the site structure: `_includes`, layouts, components/macros, `_data`, content collections, assets, generated output, and any CMS or fetch layer.
4. Identify template language conventions. In Nunjucks repos, prefer includes, macros, filters, and shortcodes consistent with the existing code.
5. Treat Eleventy's data cascade as a design surface. Put shared defaults in directory/global data, page-specific values in front matter, and derived values in computed data.
6. Keep pages pre-rendered and resilient without JavaScript. Add client JS only for progressive enhancement.

## Eleventy Defaults

- Preserve the repo's config style: ESM, CommonJS, named config export, or method-based config.
- Keep layouts and includes relative to the configured input directory.
- Use tags to create collections; remember tags are for Eleventy collections, not necessarily user-facing tag taxonomy.
- For collection names containing dashes or spaces, use bracket notation in Nunjucks: `collections["case-studies"]`.
- Use `eleventyExcludeFromCollections` for feeds, sitemaps, utility templates, or generated files that should not appear in collections.
- Declare collection dependencies with `eleventyImport.collections` when templates rely on collections and the repo uses incremental builds.
- Prefer filters for formatting values, shortcodes for reusable rendered fragments, and paired shortcodes when body content is involved.
- Use passthrough copy for static assets that do not need transformation. Use the repo's bundler for CSS/JS/image work when present.

## Nunjucks Patterns

- Use layouts for page chrome, includes for partials, and macros for repeatable parameterized components.
- Keep front matter clean and serializable. Avoid burying substantial display logic in markdown front matter.
- Escape intentionally. Nunjucks autoescaping depends on environment; inspect config before using `safe`.
- For navigation, use `page.url` and `aria-current="page"` or the repo's active-link helper.
- For reusable Tailwind components, prefer Nunjucks macros or includes with explicit class maps. Pair with `tailwindcss-expert`.

Example macro:

```njk
{% macro button(label, href, tone="primary") %}
  {% set toneClass = {
    primary: "bg-sky-600 text-white hover:bg-sky-700",
    neutral: "bg-white text-slate-900 ring-1 ring-slate-200 hover:bg-slate-50"
  }[tone] %}
  <a class="inline-flex items-center rounded-md px-4 py-2 text-sm font-medium {{ toneClass }}" href="{{ href }}">
    {{ label }}
  </a>
{% endmacro %}
```

## JAMstack Judgment

- Prefer build-time data fetching when content can be static. Cache remote data or document why live client fetch is needed.
- Keep SEO, canonical URLs, feeds, sitemap, metadata, image dimensions, and social previews in the build pipeline.
- Preserve clean output paths and stable permalinks.
- Add client-side libraries only when they buy real interaction. For small dropdowns, accordions, filters, dialogs, or disclosure UI, pair with `alpinejs-lightweight-js`.
- Verify with `npx @11ty/eleventy`, the repo's build script, and the local dev server when available.

## Build Awesome Naming

- Existing Eleventy/11ty repos still use `@11ty/eleventy`, `.eleventy.*`, `eleventy.config.*`, plugins, and build commands unless the repo has intentionally migrated.
- Treat "Build Awesome" as the open-source Eleventy continuation/branding, not as a reason to rewrite a working repo.
- Treat "Build Awesome Pro" as optional paid collaboration/workflow tooling. Do not require it for ordinary Eleventy development, static builds, Nunjucks templates, Tailwind work, or deployments.
- If documentation uses Build Awesome language, map it back to the Eleventy concepts in the repo before changing package names or commands.

## Quality Gate

Before completion:

- Run the Eleventy build script and inspect warnings.
- Check representative generated HTML in `_site` or the configured output directory.
- Test at least one collection page, one detail page, one layout/include change, and touched assets.
- Confirm URLs, permalinks, image paths, and passthrough files resolve correctly.
- Confirm the site still works with JavaScript disabled for core content and navigation.

## References

Read `references/eleventy-patterns.md` for deeper repo patterns and `references/official-docs.md` for primary docs.
