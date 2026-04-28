# Invocation Recipe

Use these patterns when starting a fresh audit in a new repo.

## Best default prompt

```text
Use $ML-user-journey-audit to create a current-state navigation audit for this repo.
Prefer the live deployment if it is available, use the codebase and tests for coverage verification, keep the work current-state only, capture screenshots for each landed screen, and export the final report as a PDF in the docs folder.
If the user types are not obvious, inspect the repo and suggest which ones to include before auditing.
```

## One-user version

```text
Use $ML-user-journey-audit to audit the current-state journey for the Admin user in this repo.
Prefer the live site, capture click-by-click screenshots, verify route coverage against the codebase and tests, and export a final PDF report in the docs folder.
Do not do any future-state synthesis.
```

## Multi-user version

```text
Use $ML-user-journey-audit to audit the current-state journeys for these user types in this repo: Member, Admin, and Partner.
Prefer the live site, capture click-by-click screenshots for each landed screen, verify route coverage against the codebase and tests, and export a final PDF report in the docs folder.
Keep the report current-state only and include a coverage-verification section.
```

## When the user did not give the user types

Start with:

```text
Use $ML-user-journey-audit to inspect this repo and suggest which user types should be included in a current-state navigation audit.
Prefer evidence from auth flows, seeded users, sidebar shells, route families, and E2E tests.
After suggesting the user types, continue the audit only after the user confirms the list.
```

## Recommended execution order

1. Identify the primary audit source: live site first, repo second.
2. Confirm the user types if they were not already provided.
3. Create the audit folder and manifest scaffold.
4. Capture the role walkthroughs and screenshots.
5. Verify route coverage.
6. Render the PDF.
7. Preserve the final PDF in the audit docs folder.

## Good final deliverable wording

When closing out the work, the result should point the user to:
- the final PDF in the docs folder
- the audit source docs
- the screenshots folder
- the coverage verification file

Keep the closeout concise and explicit about whether coverage is complete or only partial.
