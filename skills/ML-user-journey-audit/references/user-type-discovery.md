# User-Type Discovery

Use this reference when the user wants a journey audit but has not yet given the user types to include.

## Goal

Suggest a practical, audit-sized list of user types based on evidence in the repo or deployed product.

Do not invent a huge taxonomy. The goal is to identify the meaningful navigation branches that deserve separate walkthroughs.

## Evidence sources

Check these in order:

1. Auth and demo fixtures
- seeded accounts
- login hints
- test helpers for role login
- role enums in auth/session code

2. Sidebar and top-level navigation
- different nav shells
- different workspace titles
- different dashboard cards or queue labels

3. Route families
- role-owned list pages
- role-owned settings pages
- role-specific redirects or aliases

4. E2E and smoke tests
- role-specific setup helpers
- fixtures that log in as different users
- parity tests that branch by role

## Suggestion heuristics

Suggest a user type when at least one of these is true:
- it has a distinct nav shell
- it has a distinct dashboard home
- it has distinct route families or settings pages
- it has distinct permissions that materially change reachable screens

Do not split user types only because data differs. Split them when the navigation or reachable route graph differs enough to justify a separate walkthrough.

## Output pattern

When the user did not already specify the user types, suggest them briefly:

- `Family`
- `Donor`
- `Clinic`

Or, in another repo:

- `Member`
- `Admin`
- `Partner`

Then ask one short confirmation question such as:

`I found three distinct navigation branches: Family, Donor, and Clinic. Do you want the audit to include all three?`

If the user already named the user types, do not re-open that decision unless the repo clearly shows another distinct branch they are likely to care about.
