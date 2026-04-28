# Coverage Checklist

Use this checklist before claiming that a user journey audit covers the current route graph.

## Route families

Check:
- auth entry surfaces
- dashboard home
- top-level nav destinations
- detail pages linked from those destinations
- settings and profile subroutes

## Query-state workspaces

Check for:
- `tab=`
- `filter=`
- `scope=`
- `view=`
- `mode=`
- `focus=`
- selected-item query states like `personId=`, `treeId=`, `reminder=`, `update=`

If a query state changes the visible workspace, capture it as a distinct current-state screen.

## Aliases and redirects

Check:
- legacy routes that redirect into settings or newer surfaces
- role-specific aliases
- default route redirects

Document them even if they are not in the primary navigation.

## Tokenized and public handoff routes

Check:
- invite links
- share links
- public pages
- verify/reset/auth handoffs when relevant

Do not claim public or token-route coverage if you only captured a broken direct URL and never verified a valid live state.

## Dashboard shortcuts

Check dashboard cards and summary modules for routes that are not visible in the sidebar:
- queue filters
- exact detail routes
- alternate role-owned workspaces

These often reveal the app’s real route graph more accurately than the sidebar alone.

## Trust classification

Classify route families as:
- covered
- partially covered
- missing
- untrusted

Use `untrusted` when the route exists in code or tests but the live capture did not resolve as expected.
