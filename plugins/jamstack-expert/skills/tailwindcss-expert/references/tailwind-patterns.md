# Tailwind Patterns

## Repo Inspection

Check these before editing:

- Tailwind version: `npm ls tailwindcss`, `package.json`, lockfile.
- Build integration: Vite plugin, PostCSS, framework adapter, CLI script, or static-site pipeline.
- CSS entrypoint: `@import "tailwindcss";`, `@tailwind base/components/utilities`, `@theme`, `@layer`, `@source`, `@plugin`, `@config`.
- Source scanning: v3 `content`, v4 automatic detection plus any explicit source configuration.
- Local helpers: `cn`, `clsx`, `tailwind-merge`, `cva`, `tv`, design-system wrappers.
- Existing tokens: color names, radius scale, font families, spacing conventions, dark mode strategy.

## Version-Sensitive Guidance

For Tailwind v4:

- Prefer CSS-first configuration in the existing CSS entrypoint when the repo already uses it.
- Use `@theme` for tokens that should create utilities or variants.
- Use ordinary CSS variables for runtime values that should not generate utilities.
- Be careful with `@apply` in CSS modules or component-scoped styles; theme context may need `@reference`, and utility classes in markup are usually simpler.

For Tailwind v3:

- Use `tailwind.config.*` and `theme.extend` for reusable tokens.
- Make sure all template locations are covered by `content`.
- Use safelists only for truly dynamic classes that cannot be enumerated in source.

## Class Authoring

- Order classes roughly by role: layout, box model, sizing, typography, color, effects, transitions, states, responsive variants. Follow local formatter plugins if present.
- Prefer complete, readable strings over clever composition.
- For conditionals, map states to complete class strings:

```js
const toneClasses = {
  info: "border-sky-200 bg-sky-50 text-sky-900",
  warning: "border-amber-200 bg-amber-50 text-amber-950",
  danger: "border-rose-200 bg-rose-50 text-rose-950",
};
```

- Use `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-* focus-visible:ring-offset-2` or the repo's equivalent focus treatment for custom controls.
- Prefer `aria-current`, `aria-expanded`, `aria-selected`, `disabled`, and `data-state` attributes as styling hooks instead of extra JS-only classes.

## When CSS Is Appropriate

Use CSS for:

- Tailwind imports and theme declarations.
- Site-level base styles and third-party resets.
- Generated content or markup outside your control.
- Complex keyframes, masks, print styles, or rich text/prose defaults.
- Extremely repeated component internals when the repo already has a component-layer pattern.

Avoid CSS for ordinary layout, spacing, color, typography, state, and responsive rules that can live directly on the element.
