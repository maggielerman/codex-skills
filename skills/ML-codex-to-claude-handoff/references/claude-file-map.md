# Claude File Map

Use this map when preparing a repository for Claude Code.

## Core files
- `CLAUDE.md`: Project instruction memory file loaded by Claude Code.
- `.claude/rules/*.md`: Rule modules that can be imported from `CLAUDE.md`.
- `.claude/settings.json`: Project-level permission policy (allow/deny for tools/commands).

## Docs integration files (when repo has docs)
- `docs/development/claude-code-setup.md`: Contributor-facing setup and governance guidance.
- Docs indexes/manifests (repo-specific): Add links so the setup page is discoverable.
- Project tracking docs (repo-specific): Record the governance/setup update in changelog/checkpoint logs.

## Import pattern
- Use `@relative/path` lines in `CLAUDE.md` to import canonical instruction files.
- Keep `AGENTS.md` (or equivalent Codex source files) authoritative when possible.

## Parity strategy
- Import source files directly where possible.
- Generate an extracted rule summary in `.claude/rules/` for fast scanning and Claude-native organization.
- Regenerate files whenever source instruction files change.
- Keep contributor docs and project logs in sync with generated Claude files.
