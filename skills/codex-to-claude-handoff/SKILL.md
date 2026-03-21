---
name: "codex-to-claude-handoff"
description: "Prepare a repository for Claude Code Desktop by generating CLAUDE.md, .claude/rules/*.md, and .claude/settings.json from existing Codex instruction files (especially AGENTS.md and .github/copilot-instructions.md). Use when migrating or handing off a repo from Codex to Claude while preserving operating rules and safety guardrails."
---

# Codex to Claude Handoff

Create Claude Code project files that mirror Codex repository rules.
Use this skill when the user wants Claude Code to follow the same repo policies Codex uses.

## Quick start

Run a dry run first:

```bash
python3 "$HOME/.codex/skills/codex-to-claude-handoff/scripts/setup_claude_repo.py" \
  --repo /absolute/path/to/repo \
  --dry-run
```

Apply changes:

```bash
python3 "$HOME/.codex/skills/codex-to-claude-handoff/scripts/setup_claude_repo.py" \
  --repo /absolute/path/to/repo
```

Force overwrite generated files after source changes:

```bash
python3 "$HOME/.codex/skills/codex-to-claude-handoff/scripts/setup_claude_repo.py" \
  --repo /absolute/path/to/repo \
  --force
```

## Workflow

1. Identify Codex source instructions.
2. Run the generator script with `--dry-run` first.
3. Re-run without `--dry-run` to write files.
4. Verify `CLAUDE.md` imports the intended source files.
5. Review `.claude/settings.json` allow/ask/deny rules and tighten if needed.
6. If the repo has a docs system, update docs so contributors know Claude setup and governance.
7. Record the change in project tracking docs (`CHANGELOG`, active project log/checkpoint) if the repo uses them.

## Source discovery rules

If `--source` is not provided, the script searches in this order:
1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. Any `AGENTS.md` found recursively in the repo

Use `--source` (repeatable) to pin exact files:

```bash
python3 "$HOME/.codex/skills/codex-to-claude-handoff/scripts/setup_claude_repo.py" \
  --repo /absolute/path/to/repo \
  --source AGENTS.md \
  --source docs/engineering/agent-rules.md
```

## Generated files

- `CLAUDE.md`: Claude entrypoint with `@...` imports to Codex source files and generated rule file.
- `.claude/rules/00-codex-parity.md`: Extracted policy-style rules from source instructions.
- `.claude/settings.json`: Project-level Claude permission defaults (skipped with `--skip-settings`).

## Required parity checks

To match the full handoff flow used in `shopify-bulk-editor-app`, do all of the following after generation:

1. Confirm `CLAUDE.md` clearly points Claude to canonical source rules (`AGENTS.md` and any repo-specific policy files).
2. Confirm `.claude/settings.json` includes:
   - safe defaults (`defaultMode`, `disableBypassPermissionsMode`)
   - low-risk commands in `allow`
   - push/merge actions in `ask`
   - destructive commands in `deny`
3. If `docs/` exists, add or update a Claude setup page (for example `docs/development/claude-code-setup.md`) describing:
   - policy precedence (`AGENTS.md` first)
   - the role of `CLAUDE.md`
   - the role of `.claude/settings.json`
4. Update docs navigation/index pages that should surface the Claude setup page.
5. Update project tracking docs used by the repo (for example `CHANGELOG.md` and active checkpoint logs).
6. Run a docs build check when docs structure changed.

## Output expectations

- Keep source instruction files authoritative.
- Generate minimal, readable Claude files that are safe to regenerate.
- Avoid manual duplication drift by re-running the script after source updates.

Read [references/claude-file-map.md](references/claude-file-map.md) when you need file-role details.
