# Alpine Patterns

## Choosing The Smallest Tool

- No JS: static content, ordinary links, server-rendered pages, native details/summary, CSS hover/focus, CSS-only layout.
- Alpine inline component: one small local interaction.
- `Alpine.data()`: repeated component, enough logic to deserve named methods/getters, CSP-friendly extraction.
- `Alpine.store()`: shared UI state such as theme, cart count, dismissed banner, or synchronized filters.
- Heavier framework: complex routing, deep client state, collaborative editing, offline-first app behavior, or app-level data synchronization.

## Common Components

Disclosure/accordion:

- `x-data="{ open: false }"`
- Button with `aria-expanded` and `aria-controls`.
- Panel with `x-show`, `x-transition`, and stable `id`.
- Consider native `details` when it fits the design.

Dropdown/menu:

- `@click.outside` to close.
- Escape key handling.
- Focus movement or at least sensible focus return.
- Use real links/buttons inside the menu.

Tabs:

- Server-render useful default content.
- Use buttons with `role="tab"` only if implementing the full tab pattern.
- Otherwise use simpler segmented controls or links.

Filters:

- Prefer URL/query-parameter backed filters when results should be shareable or indexed.
- Use Alpine for immediate local filtering of already-rendered content.

Dialog:

- Prefer native `<dialog>` if the repo supports it and styles it well.
- Trap or manage focus; close on Escape; restore focus.
- Prevent background interaction when open.

## CSP Notes

Standard Alpine evaluates HTML attribute expressions in a way that can conflict with strict `script-src` policies. If the site forbids unsafe eval, use `@alpinejs/csp`, keep inline expressions simple, and move complex logic into `Alpine.data()`.

## Tailwind State Hooks

Prefer stateful attributes and variants:

```html
<button
  x-data="{ pressed: false }"
  :data-pressed="pressed"
  @click="pressed = !pressed"
  class="rounded-md px-3 py-2 data-[pressed=true]:bg-slate-900 data-[pressed=true]:text-white"
>
  Toggle
</button>
```

Avoid hiding class names from Tailwind:

```html
<!-- Avoid -->
<div :class="`bg-${tone}-500`"></div>

<!-- Prefer -->
<div :class="tone === 'good' ? 'bg-emerald-500' : 'bg-rose-500'"></div>
```
