# Motion Patterns

Use these as taste-level patterns. For GSAP syntax, delegate through `gsap-delegation-map.md`.

## Entrance Reveal

Use when a section or component enters view and needs hierarchy.

Taste defaults:

- Primary object enters first or has the clearest movement.
- Headline can move slightly more than body copy.
- Body copy should not exceed `tasteRules.bodyTextMaxY`.
- Supporting details stagger after the primary object.
- Controls must not wait behind decorative motion.

Avoid:

- Identical timing for every child.
- Large vertical travel on body text.
- Repeating the same reveal pattern on every section.

Implementation routing:

- Use `gsap-core` or `gsap-timeline`.
- Use `gsap-react` for React/Next.
- Use `gsap-scrolltrigger` only if viewport entry or scroll progress drives the reveal.

## Exit Or Dismiss

Use when content leaves because the user changed state.

Taste defaults:

- Exit should be faster than entrance.
- Direction should match the state change.
- Preserve focus and accessibility state.

Avoid:

- Slow exits before a user can continue.
- Decorative exits for repeated task flows.

## Scroll Narrative

Use when scroll position controls a story, sequence, or spatial transition.

Taste defaults:

- Pin only when the scene needs sustained attention.
- Keep progress understandable without requiring exact scroll speed.
- Leave a visible hint of the next section when possible.
- Verify small viewport behavior.

Avoid:

- Capturing scroll for long stretches without payoff.
- Making text unreadable while scroll-scrubbed objects pass over it.
- Treating the timeline as final without viewport screenshots.

Implementation routing:

- Use `gsap-scrolltrigger`.
- Use `gsap-timeline` for scene sequencing.
- Use `gsap-performance` for pinning, refresh, batching, and layout concerns.

## Mask Reveal

Use when revealing media or composition through a shaped transition.

Taste defaults:

- The mask shape should relate to the content or interaction.
- Text should not be hidden by a decorative mask unless that is the stated effect.
- The reveal should finish before inspection is needed.

Avoid:

- Masking body copy.
- Animating layout-heavy properties when transform or SVG mask animation will work.

Implementation routing:

- Use `gsap-core`, `gsap-timeline`, and possibly `gsap-plugins`.
- Use `gsap-performance` for rendering concerns.

## Morph Or Continuity Transition

Use when one object becomes another or layout state changes need continuity.

Taste defaults:

- The source and destination objects must be visually connected.
- Keep the viewer oriented through scale, position, shared shape, or shared content.
- Reduce other motion while the transformation is happening.

Avoid:

- Random morphs that do not clarify state.
- Multiple simultaneous transformations competing for attention.

Implementation routing:

- Use `gsap-plugins` for Flip, MorphSVG, or related plugin decisions.
- Use `gsap-timeline` for staged transitions.

## Path Motion

Use when an object guides attention through a route, diagram, or story path.

Taste defaults:

- The path should have a reason: progress, attention, navigation, or object continuity.
- Keep speed readable and avoid sudden turns unless intentionally tactile.
- Do not let paths or guide objects cross readable content.

Implementation routing:

- Use `gsap-plugins` for MotionPath.
- Use `gsap-scrolltrigger` if scroll drives progress.

## Parallax And Depth

Use when spatial depth clarifies hierarchy or creates atmosphere.

Taste defaults:

- Move background elements less than foreground focus objects.
- Keep text stable or nearly stable.
- Reduce heavily on mobile and reduced motion.

Avoid:

- Scroll sickness from large opposing movements.
- Depth effects in dense forms, tables, or repeated task screens.

Implementation routing:

- Use `gsap-scrolltrigger`, `gsap-utils`, and `gsap-performance`.

## Tactile Interaction

Use for direct user input: hover, press, drag, focus, toggle, and card response.

Taste defaults:

- Response starts immediately.
- Motion is short and reversible.
- Feedback should not change layout unless the control is designed for it.

Avoid:

- Hover-only meaning.
- Long easing after pointer movement stops.

Implementation routing:

- Use `gsap-core`.
- Use `gsap-utils` and `gsap-plugins` for high-frequency pointer, Observer, Draggable, or snapping behavior.
