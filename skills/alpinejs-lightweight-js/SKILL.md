---
name: alpinejs-lightweight-js
description: 'Custom skill created by Maggie Lerman. Alpine.js and lightweight progressive JavaScript workflow for static/JAMstack sites. Use when working with x-data, x-show, x-bind, x-on, x-transition, Alpine.data/store, @alpinejs plugins, CSP-safe Alpine, dropdowns, accordions, tabs, dialogs, filters, or minimal client JS.'
---

# Alpine.js Lightweight JS

Custom skill created by Maggie Lerman.

Use this skill to add small, resilient interactivity to otherwise static sites. Prefer HTML-first progressive enhancement, accessible native behavior, and tiny state scopes over large client-side frameworks.

## Start Here

1. Confirm the interaction actually needs JavaScript. Prefer native HTML, CSS, server-rendered variants, and simple links/forms when they solve the problem.
2. Inspect how JavaScript is loaded: CDN script, bundled npm import, deferred module, site-wide entrypoint, page-specific bundle, CSP build, or existing helper.
3. If the repo's Alpine version, CDN pin, plugin compatibility, or CSP package matters, pair with `jamstack-version-auditor` before recommending an update.
4. Keep Alpine component state local with `x-data` unless multiple distant components need shared state.
5. Use `Alpine.data()` for repeated or complex components. Use `Alpine.store()` for genuinely shared state.
6. Preserve core content and navigation without JavaScript whenever practical.

## Alpine Patterns

- Use `x-data` to establish component scope. Alpine directives like `x-bind`, `x-on`, and `x-transition` need an Alpine component context.
- Use `x-show` for toggles that remain in the DOM; pair it with `x-transition` for simple transitions.
- Use `x-if` only when an element should be created/destroyed; do not expect `x-transition` to work with `x-if`.
- Use `x-bind` or `:` for attributes and classes derived from state.
- Use `x-on` or `@` for events, with keyboard and outside-click modifiers when appropriate.
- Use `x-cloak` for content that should stay hidden until Alpine initializes; make sure the cloak CSS exists.
- Keep inline expressions short. Extract complex logic into methods, getters, or `Alpine.data()`.
- For strict Content Security Policy sites, use `@alpinejs/csp` and avoid unsupported global expressions.

## Accessibility Rules

- Match state to ARIA: `aria-expanded`, `aria-controls`, `aria-selected`, `aria-current`, `hidden`, `inert`, or dialog semantics as appropriate.
- Keep keyboard support complete for menus, dialogs, tabs, disclosures, and combobox-like controls.
- Manage focus deliberately for dialogs, popovers, and menu-like interactions.
- Do not hide important content in a JS-only path. Server-render default content when possible.
- Respect reduced motion for custom transitions if the repo has motion utilities or CSS support.

## Tailwind And Nunjucks

Pair with `tailwindcss-expert` for styling and `eleventy-jamstack-expert` in 11ty repos.

- Put state styling in Tailwind variants when possible: `aria-expanded:*`, `data-*`, `group-*`, `peer-*`, or class maps from Alpine state.
- Keep Tailwind class names statically discoverable. Avoid constructing partial utility names in Alpine expressions.
- In Nunjucks macros/includes, pass simple behavior options and emit complete Alpine attributes and complete class strings.

Example disclosure:

```html
<section x-data="{ open: false }" class="border border-slate-200">
  <button
    type="button"
    class="flex w-full items-center justify-between px-4 py-3 text-left font-medium"
    :aria-expanded="open.toString()"
    @click="open = !open"
  >
    Details
  </button>
  <div x-show="open" x-transition class="px-4 pb-4">
    Content that is useful even when rendered statically.
  </div>
</section>
```

## Quality Gate

Before completion:

- Verify the page still has useful content before Alpine starts.
- Test mouse, keyboard, focus, and escape/outside-click behavior where relevant.
- Test with the repo's CSP assumptions.
- Run the repo's build and browser smoke test.
- Check for console errors and hydration-like assumptions that do not belong in a static site.

## References

Read `references/alpine-patterns.md` for component patterns and `references/official-docs.md` for primary docs.
