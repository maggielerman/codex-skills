---
name: tailwindcss-expert
description: 'Tailwind CSS expert workflow for utility-first inline classes. Use when working with Tailwind repos/files: tailwind.config.*, @import "tailwindcss", @theme/@apply, class/className utilities, PostCSS/Vite setup, shadcn-style utilities, or default Tailwind UI styling.'
---

# Tailwind CSS Expert

Use this skill to make Tailwind utility classes in markup the default styling surface. Treat repo conventions as authoritative, but prefer inline utilities over new CSS selectors, CSS modules, styled components, or broad custom styles unless the existing system clearly requires them.

## Start Here

1. Inspect the repo before editing: `package.json`, lockfile, Tailwind version, CSS entrypoint, framework, component conventions, class helpers, and existing design tokens.
2. If version currency or migration risk matters, pair with `jamstack-version-auditor` before recommending changes to Tailwind major versions, CLI packages, PostCSS/Vite integration, or plugin dependencies.
3. Detect Tailwind generation style:
   - v4-style projects often use `@import "tailwindcss";`, CSS-first `@theme`, `@source`, and theme variables.
   - v3-style projects often use `tailwind.config.*`, `content`, `theme.extend`, PostCSS config, and plugin arrays.
4. Preserve existing class ordering, component patterns, and token names. If the repo has `cn`, `clsx`, `cva`, `tailwind-merge`, `class-variance-authority`, or variant helpers, use them consistently.
5. Put styling in `class` or `className` by default. Use CSS files for Tailwind imports, theme tokens, base resets, genuinely global styles, third-party styling, typography prose, animations/keyframes, or selectors targeting HTML you cannot edit.
6. Verify generated classes are statically discoverable by Tailwind. Avoid dynamic string fragments like `bg-${color}-500`; use explicit maps, complete class strings, safelists, or documented source configuration.

## Implementation Rules

- Use utility classes as the public API of the design system. Prefer spacing, color, type, radius, shadow, breakpoint, state, dark-mode, data, group, peer, aria, and container-query variants directly in markup.
- Prefer semantic HTML and accessible states first; Tailwind classes should express the styling, not compensate for weak markup.
- Build mobile-first. Add `sm:`, `md:`, `lg:`, and larger breakpoints only when the layout actually changes.
- Style states in the class list: `hover:`, `focus-visible:`, `active:`, `disabled:`, `aria-*`, `data-*`, `group-*`, and `peer-*`.
- Keep arbitrary values rare and intentional. Use existing tokens first; add theme variables or config tokens when a value repeats or belongs to the design system.
- Avoid `@apply` for component styling unless the repo already uses it heavily or the target is hard to style in markup. Tailwind's own v4 guidance favors utilities in markup over component `<style>` blocks for many toolchains.
- For long class strings, improve maintainability with local constants, variant maps, `cva`, or a `cn()` helper instead of moving styles into CSS.
- When refactoring CSS to Tailwind, keep behavior equivalent: layout, responsive behavior, states, print styles, reduced-motion preferences, and specificity-sensitive rules.

## Tailwind With 11ty/Nunjucks

Pair this skill with `eleventy-jamstack-expert` in Eleventy projects. In `.njk`, `.liquid`, `.md`, and data-generated templates, make sure Tailwind scans the actual template paths. Use explicit class maps in Nunjucks macros/includes instead of composing partial class names at runtime.

Good Nunjucks pattern:

```njk
{% set toneClass = {
  primary: "bg-sky-600 text-white hover:bg-sky-700",
  subtle: "bg-slate-100 text-slate-900 hover:bg-slate-200"
}[tone or "primary"] %}

<a class="inline-flex items-center rounded-md px-4 py-2 text-sm font-medium {{ toneClass }}" href="{{ href }}">
  {{ label }}
</a>
```

Risky pattern:

```njk
<a class="bg-{{ color }}-600 hover:bg-{{ color }}-700">
```

## Quality Gate

Before calling work complete:

- Run the repo's build or Tailwind generation command when available.
- Confirm new classes appear in scanned source files.
- Check responsive layouts at narrow and desktop widths.
- Check focus-visible, hover, disabled, selected/current, empty, error, and loading states for touched controls.
- Scan for accidental one-off CSS that should have remained utilities.

## References

Read `references/tailwind-patterns.md` for detailed authoring patterns, version detection, and class organization guidance. Read `references/official-docs.md` when you need current primary-source links.
