---
name: repo-implementation-review
description: Custom skill created by Maggie Lerman. Review and compare 2-3 repositories that implement the same product idea, then generate a downloadable HTML comparison artifact with pros/cons, feature gaps, scores, recommendation paths, and CSV/PDF export options. Use when a user asks for side-by-side technical assessment of multiple implementation repos or wants a recommendation between competing codebases.
---

# Repo Implementation Review

Custom skill created by Maggie Lerman.

Assess two or three repositories independently and comparatively, then produce a report artifact the user can open and download.

## Quick Start

1. Set the skill root:
```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/repo-implementation-review"
```

2. Generate a review scaffold from repo paths and collect verification evidence (tests/build/docs/endpoints):
```bash
python3 "$SKILL_ROOT/scripts/prepare_review_input.py" \
  --project-name "<project idea>" \
  --repo "Implementation A=/absolute/path/to/repo-a" \
  --repo "Implementation B=/absolute/path/to/repo-b" \
  --repo "Implementation C=/absolute/path/to/repo-c" \
  --output /tmp/repo-review-input.json
```
Use exactly 2 or 3 `--repo` arguments.

3. Fill the scaffold with findings from your deep review:
- Add `starting_goal`.
- For each repo, complete `goal_alignment.success_assessment` and `goal_alignment.completion_score`.
- Keep `feature_status` outcome-focused (capabilities), not vendor/tool-focused.
- Refine pros/cons/risks/recommendation using evidence from checks/docs/endpoints.

4. Build the HTML artifact:
```bash
python3 "$SKILL_ROOT/scripts/build_report.py" \
  --input /tmp/repo-review-input.json \
  --output-dir /tmp/repo-review-artifact \
  --pdf auto
```

## Review Workflow

1. Validate scope:
- Require 2-3 repositories only.
- Confirm each repo is meant to solve the same core problem.
- Confirm any priority dimensions (speed, maintainability, delivery risk, etc.).

2. Review each repository independently before cross-comparison:
- Use `references/review_rubric.md` for scoring dimensions and evidence prompts.
- Capture explicit evidence for claims (file paths, test/build command output, endpoint behavior, docs quality).
- Fill each repo section completely: `summary`, `scores`, `goal_alignment`, `verification`, `pros`, `cons`, `notable_features`, `missing_features`, `risks`, `feature_status`.

3. Compare across repositories:
- Populate `cross_repo_findings` with concrete tradeoffs.
- Normalize feature names in `feature_status` so the matrix is clean and capability-based (`"Core workflow complete"` vs tool labels).
- Set `recommended_path` with one recommended option, rationale bullets, and executable next steps.

4. Generate and share artifact outputs:
- `report.html` (interactive view with export buttons)
- `comparison.csv` (spreadsheet export)
- `review-data.json` (machine-readable source)
- `report.pdf` when `wkhtmltopdf` is available and `--pdf` permits generation

## Required Output Behavior

When using this skill in a user request:

1. Produce the artifact files first.
2. Report absolute file paths for generated outputs.
3. Summarize recommendation and top tradeoffs in chat, including:
- starting goal
- which repos actually achieved it
- what verification evidence passed/failed/skipped
4. If PDF generation is unavailable, state that the HTML file still supports `Export PDF` via browser print.

## Resources

- `scripts/prepare_review_input.py`: Build structured JSON input with auto-discovered repo signals.
- `scripts/build_report.py`: Render HTML/CSV/JSON outputs and optionally generate PDF.
- `references/review_rubric.md`: Deep-review rubric and scoring anchors.
- `references/report_schema.md`: Input schema details and example payload.
