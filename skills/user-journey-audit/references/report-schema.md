# Journey Audit Report Schema

Use this schema when building the manifest consumed by `scripts/render_journey_audit_pdf.mjs`.

## Required top-level fields

```json
{
  "title": "string",
  "intro": "string",
  "scopeLock": "string",
  "generatedAt": "string",
  "auditRoot": "string",
  "roles": [],
  "crossRoleComparison": { "headers": [], "rows": [] },
  "routeReuse": [],
  "redundancyMatrix": { "headers": [], "rows": [] },
  "terminologyMatrix": { "headers": [], "rows": [] },
  "brokenRoutes": { "headers": [], "rows": [] },
  "findings": [],
  "priorities": [],
  "coverage": {},
  "roleReports": []
}
```

## Roles

Each role controls color coding and route reuse columns.

```json
{
  "id": "family",
  "label": "Family",
  "color": "#b74f2e"
}
```

If `color` is omitted, the renderer falls back to a default palette.

## Shared tables

Use `headers` plus `rows`.

```json
{
  "headers": ["User Type", "Observed User Task", "Current Surfaces", "Why It Feels Redundant"],
  "rows": [
    ["Family", "Review relationship status", "`connections`, `contacts`, `messages`", "Explanation here."]
  ]
}
```

Cells may contain backticks for inline code and standard Markdown links, but keep content short enough to render in a table.

## Route reuse

Use one row per route pattern.

```json
{
  "route": "/dashboard/contacts?tab=*",
  "observedPurpose": "Relationship coordination workspace split into tab states",
  "rolePaths": {
    "family": ["Sidebar: Contacts", "Dashboard card: Open Contact Hub"],
    "donor": ["Sidebar: Contacts"],
    "clinic": ["Sidebar: Contacts"]
  }
}
```

The renderer creates one color-coded column per role from `rolePaths`.

## Coverage section

```json
{
  "updatedAt": "2026-04-05 15:12 ET (America/New_York)",
  "verdict": [
    "No. The current report does not yet cover every route family."
  ],
  "covered": { "headers": [], "rows": [] },
  "missingDashboard": { "headers": [], "rows": [] },
  "missingPublic": { "headers": [], "rows": [] },
  "implications": [
    "The report is reliable for primary seeded walkthroughs."
  ]
}
```

## Role reports

```json
{
  "id": "family",
  "label": "Family",
  "title": "Family User Journey",
  "accountUsed": "family@demo.example.com (Sofia Martinez)",
  "lastUpdated": "2026-04-05 14:53 ET (America/New_York)",
  "diagrams": [
    {
      "title": "Overview",
      "mermaid": "flowchart TD\n  A --> B"
    }
  ],
  "findings": [
    "Current-state finding one.",
    "Current-state finding two."
  ],
  "inventory": {
    "headers": [
      "Screen ID",
      "URL / State",
      "How You Get There",
      "Next Available Clicks",
      "Screenshot",
      "Confusion Notes"
    ],
    "rows": [
      {
        "screenId": "F01",
        "url": "/dashboard",
        "how": "Sidebar: Dashboard",
        "next": "Open Contacts, Open Discover",
        "screenshot": "/absolute/path/to/F01_dashboard-home.png",
        "screenshotLabel": "F01_dashboard-home.png",
        "notes": "Primary family home."
      }
    ]
  }
}
```

Use absolute screenshot paths whenever possible.

## Minimal manifest pattern

For a one-user audit, keep the schema the same with a single role in `roles` and a single object in `roleReports`.
