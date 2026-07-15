# Accessibility And Performance Policy

Motion design is not complete until accessibility and performance are addressed.

## Reduced Motion

Every expressive animation must have reduced-motion behavior.

Allowed reduced-motion strategies:

- Instant state change.
- Opacity-only reveal.
- Short utility transition without spatial travel.
- Static final state for decorative motion.

Reduced motion must preserve meaning. If motion explains a state transition, provide text, layout, or persistent visual continuity so the user still understands what changed.

## Responsive Behavior

- Verify desktop and one mobile width when practical.
- Reduce parallax, long pinning, and large travel on small screens.
- Do not let text overlap, clip, or wrap incoherently during animation.
- Keep touch targets usable during and after motion.

## Performance

- Prefer transform and opacity for high-frequency animation.
- Avoid layout-heavy animation unless the motion's meaning depends on layout continuity.
- Use GSAP performance guidance for batching, ScrollTrigger refresh, and cleanup.
- Do not run pointer-following animation through repeated heavyweight tween creation.
- Clean up animations on component unmount in React/Next.

## Browser QA

For rendered motion work, check:

- Page is not blank.
- No framework error overlay.
- Console has no relevant errors.
- Initial viewport and target interaction render correctly.
- Desktop and mobile composition is legible.
- Reduced-motion behavior is present.
- Motion does not cause scroll traps, layout shift, clipping, or content collision.

Automated tests are not enough for motion-heavy UI because timing, overlap, pacing, and perceived quality are rendered behaviors.
