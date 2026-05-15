# Visual Design Critique Rubric

Use this reference when a review needs more structure than the core skill body.

## What To Emulate

- NN/g heuristic evaluation: independent inspection against durable usability principles, followed by issue consolidation and prioritization.
- WCAG-style testability: turn accessibility claims into observable checks across full pages, responsive variants, and complete task flows.
- Platform design guidance: use layout, typography, color, controls, and accessibility conventions so the UI feels native to its medium.
- Mature design-system reviews: judge components as reusable systems with states, spacing, semantics, and documented exceptions.
- Existing local skills: pair this skill with `frontend-app-builder` for concept-to-code fidelity, `review-board-operating-pattern` for numbered visual evidence, and `ux-ui-bug-intake` for durable defect capture.

## Scoring Model

Use three levels unless the repo has its own severity model:

- `Must fix`: blocks trust, task completion, accessibility, or sign-off.
- `Should fix`: damages clarity, polish, or product credibility but has a reasonable workaround.
- `Polish`: improves sophistication, coherence, or delight after the essentials are sound.

Also mark scope:

- `Local`: isolated to one screen or component instance.
- `Repeated`: appears across multiple screens but can be fixed with a clear pattern.
- `Systemic`: rooted in design tokens, component architecture, IA, copy model, or product workflow.

## Complete Audit Report Template

Use this structure for a complete design audit:

```md
# Design Audit

## Executive Verdict
- Overall rating:
- Readiness:
- Biggest risks:
- Highest-leverage fixes:

## Scope And Evidence
- Routes/screens:
- Viewports:
- Flows:
- States:
- Evidence paths:
- Exclusions:

## Findings
| ID | Severity | Scope | Surface | Finding | Evidence | Recommendation | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DA-001 | Must fix | Systemic | Example | Example issue | Screenshot/path | Concrete fix | Recheck route/state |

## Systemic Themes
- Theme:
- Affected surfaces:
- Recommended component/token/process fix:

## Quick Wins
- Fix:
- Why it matters:

## Deeper Redesign Candidates
- Candidate:
- Reason:
- Suggested exploration:

## Verification Plan
- Screens/routes to re-capture:
- States to retest:
- Accessibility checks:
- Human sign-off needed:
```

## Review Checklist

### Product Read

- The first viewport or primary screen makes the product category and main task obvious.
- The primary action has enough prominence and the secondary actions are not competing with it.
- Brand tone matches the audience: utilitarian for operational tools, expressive for creative/editorial surfaces, concrete for commerce/product inspection.

### Layout And Composition

- Alignment creates scan paths instead of scattered islands.
- Spacing communicates grouping, importance, and rhythm.
- The container model fits the surface: tables for comparison, lists for repeated actions, panels for tools, cards only when item framing is useful.
- First viewport leaves a hint of continuation when the page needs scrolling.

### Typography

- Headings, body, captions, labels, and control text have distinct roles.
- Type size is appropriate to the container; compact UI chrome does not use hero-scale type.
- Line length, wrapping, and truncation are deliberate across desktop and mobile.
- Font weight and contrast support legibility rather than fashionable faintness.

### Color, Contrast, And Material

- Color has semantic discipline: status, action, selection, and brand roles do not blur together.
- The palette has enough range and neutral support; it does not collapse into one hue family by accident.
- Surfaces, borders, shadows, and depth are consistent and purposeful.
- Contrast is checked for text, icons, controls, focus states, and non-text UI indicators.

### Components And Interaction

- Components have complete states: default, hover, focus, active/selected, disabled, loading, empty, error, and success when relevant.
- Icons match metaphor, stroke/fill style, optical size, and alignment.
- Forms explain requirements, preserve user input, prevent errors, and recover gracefully.
- Destructive, expensive, or irreversible actions have confirmation, undo, or a clear escape path.

### Responsive And Accessibility

- Touch targets and spacing survive mobile.
- Keyboard navigation, focus visibility, and reading order are coherent.
- Motion supports hierarchy and respects reduced-motion needs.
- Responsive variants preserve content priority instead of merely stacking everything.

## OS Scaffold Language

Use this language in repo operating docs when useful:

> For significant user-facing UI, run a visual design critique before sign-off. Treat the critique as an evidence-backed quality gate covering hierarchy, composition, typography, color, component states, interaction clarity, accessibility, responsive behavior, and product fit. Record the outcome in the owning project doc and preserve screenshots or review packets only when they are needed as durable evidence.

## Research Sources

- NN/g, "10 Usability Heuristics for User Interface Design": https://www.nngroup.com/articles/ten-usability-heuristics/
- NN/g, "Heuristic Evaluations: How to Conduct": https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2": https://www.w3.org/TR/WCAG22/
- Apple Human Interface Guidelines, "Color": https://developer.apple.com/design/human-interface-guidelines/color
- Apple Human Interface Guidelines, "Layout": https://developer.apple.com/design/human-interface-guidelines/layout
- Apple Human Interface Guidelines, "Typography": https://developer.apple.com/design/human-interface-guidelines/typography
