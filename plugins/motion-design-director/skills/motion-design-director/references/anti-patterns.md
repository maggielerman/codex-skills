# Motion Anti-Patterns

Avoid these unless the user explicitly asks for them and the tradeoff is documented.

## Decorative Delay

Primary controls, filters, forms, and navigation wait while decorative elements finish animating.

Fix:

- Make controls available immediately.
- Move decorative animation behind or after usable state.
- Use shorter utility tokens for task UI.

## Equal-Timing Fade-Up Everywhere

Every section, card, and text block uses the same opacity and y animation.

Fix:

- Establish hierarchy.
- Use different distances for media, headings, and body copy.
- Remove repeated reveals from low-priority content.

## Scroll Capture Without Payoff

Pinned scenes hold the user for too long or make progress feel stuck.

Fix:

- Reduce pin distance.
- Show visible progress.
- Preserve a hint of the next section.
- Disable or simplify on mobile.

## Content Collision

Lines, path-following objects, masks, sticky nav, or parallax elements overlap readable text or counts.

Fix:

- Route decorative geometry away from text.
- Add spatial constraints.
- Verify at multiple viewport widths.
- Treat this as a QA blocker.

## Layout-Heavy Animation

Animation changes layout properties repeatedly without a clear reason.

Fix:

- Prefer transform and opacity.
- Use GSAP performance guidance.
- Measure or inspect layout shift when layout animation is necessary.

## Missing Reduced Motion

Full motion runs for users who request reduced motion.

Fix:

- Provide opacity-only, instant, or simplified variants.
- Check `prefers-reduced-motion`.
- Keep essential state changes clear without motion.

## Magic Without Continuity

Objects appear, morph, or travel without a readable relationship.

Fix:

- Make source and destination visible.
- Use shared geometry, path, mask, or scale continuity.
- Reduce competing effects during the transition.
