---
name: working-modes
description: Custom skill created by Maggie Lerman. Lightweight index of custom working modes. Use when the user asks what modes exist, wants to switch modes, mentions mode switcher, working modes, custom modes, pressure testing mode, critical thinking mode, rapid iteration mode, echo-chamber reset, or needs help choosing between critical deliberation, rapid iteration, and drift correction. This is an index, not a dispatcher plugin.
---

# Working Modes

Custom skill created by Maggie Lerman.

## Purpose

Provide a lightweight inventory of custom modes without creating a heavy mode system. Use this skill to choose the right posture, then apply the named mode normally.

Do not make the user operate a mode dashboard. Natural-language triggers are enough.

## Modes

### `critical-thinking-partner`

Use for deliberation: brainstorming, planning, choosing direction, pressure-testing, product/design/strategy judgment, workflow architecture, skill/plugin packaging, and "what do you think?" conversations.

Posture: critical sounding board. Challenge assumptions, surface tradeoffs, avoid echoing, and recommend a sharper path. Stop debating when the user gives execution direction.

Common triggers:

- `critical thinking partner`
- `critical thinking mode`
- `pressure testing mode`
- `pressure-test this`
- `be a sounding board`
- `help me think this through`
- `what am I missing?`
- `does this make sense?`

### `rapid-iteration-mode`

Use for fast, concrete iteration: small visual, product, copy, UI, UX, layout, image, or implementation passes where the goal is to try, inspect, and adjust quickly.

Posture: small reversible edits, cheap verification, tight feedback loop, branch/change hygiene.

Common triggers:

- `rapid iteration mode`
- `try a few variants`
- `quick pass`
- `tighter loop`
- visual finetuning or small UI/content adjustments

### `echo-chamber-drift-check`

Use as a reset when the assistant is mirroring, over-validating, polishing instead of judging, or repeating the user's point back.

Posture: stop the drift, re-answer with independent judgment, and include a missing risk, disagreement, or alternative frame.

Common triggers:

- `echo chamber`
- `you're echoing me`
- `stop mirroring`
- `reset`
- `harden this`
- `you're just repeating me`

## Choosing A Mode

Use the lightest useful mode:

- If the user is talking something through, use `critical-thinking-partner`.
- If the user is executing and wants fast changes, use `rapid-iteration-mode`.
- If the assistant has drifted into reflection or validation, use `echo-chamber-drift-check`.
- If the user gives a concrete task list, do the task. Do not introduce mode overhead unless a material risk requires it.

The default goal is simple interaction with strong agent judgment, not more process.
