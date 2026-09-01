---
name: hyphenomenon-project-intake
description: Custom skill created by Maggie Lerman. Create a Hyphenomenon import-ready project intake package (single markdown dossier plus 4-8 screenshots) for a software repository. Use when a user asks to prepare a repo for import as a project + graph nodes, especially when they require exact dossier section headers, screenshot gallery links, hydration artifacts, workflow summaries, and a handoff checklist.
---

# Hyphenomenon Project Intake

Custom skill created by Maggie Lerman.

Build a repeatable dossier + screenshot package for Hyphenomenon import.

Forward artifact rule: create project intake artifacts in the Hyphenomenon repo under `DOCS/intake/runs/projects/<date>-<project-slug>/`. Do not write generated Hyphenomenon intake dossiers or screenshots into the source repo.

This skill covers the project intake lane. It does not cover chat/session intake; use `hyphenomenon-chat-intake` for AI conversation transcripts, chat artifacts, created-skill/project/repository capture, and chat route sync. In the Hyphenomenon repo, branch lifecycle and merge/delete policy for committed intake artifacts is documented in `DOCS/intake/README.md`.

## Quick Start

1. Set the skill root:
```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/hyphenomenon-project-intake"
SOURCE_REPO_ROOT="/path/to/source-repo"
HYPHENOMENON_ROOT="/path/to/hyphenomenon"
```

2. Generate scaffold files in the Hyphenomenon repo:
```bash
python3 "$SKILL_ROOT/scripts/create_intake_scaffold.py" \
  --project-name "Family Shapes" \
  --repo-url "https://github.com/maggielerman/family-shapes" \
  --live-url "https://familyshapes.com" \
  --source-repo-path "$SOURCE_REPO_ROOT" \
  --repo-root "$HYPHENOMENON_ROOT" \
  --output "DOCS/intake/runs/projects/2026-06-01-family-shapes/dossier.md" \
  --screenshots-dir "DOCS/intake/runs/projects/2026-06-01-family-shapes/screenshots"
```

3. Capture screenshots into the run directory's `screenshots/` folder (use browser automation tools):
- `01-home.png`
- `02-primary-workflow.png`
- `03-key-feature.png`
- `04-admin-or-settings.png`
- Optionally `05-08` for additional relevant screens

4. Fill the dossier with source-backed summaries and links.

5. Validate requirements:
```bash
python3 "$SKILL_ROOT/scripts/verify_intake.py" \
  --repo-root "$HYPHENOMENON_ROOT" \
  --repo-url "https://github.com/maggielerman/family-shapes" \
  --live-url "https://familyshapes.com"
```

## Workflow

1. Read local governance files first.
- Prioritize `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md` when present.
- Prefer source-backed claims; never infer factual details that can be read directly.

2. Capture product context.
- Identify product type, personas, major routes/workflows, stack, operations, and AI/automation guidance.
- Pull evidence from docs + code (README, docs hub, route files, package/tooling, CI workflows).

3. Produce required artifacts.
- Create `DOCS/intake/runs/projects/<date>-<project-slug>/dossier.md`.
- Create `DOCS/intake/runs/projects/<date>-<project-slug>/screenshots/`.
- Save 4-8 screenshots with clear names; include home, primary workflow, key feature, and admin/settings equivalent.
- Create `DOCS/intake/runs/projects/<date>-<project-slug>/project-page-packet.json` for public project-page proof sections, product surfaces, tech stack, key dates, data-model highlights, and first-class data-model artifacts when useful.
- Create `DOCS/intake/runs/projects/<date>-<project-slug>/workflow-packet.json` when the project depends on visible process, automation, AI collaboration, human review, or repeatable operations.

4. Enforce exact dossier structure.
- Use the exact required headers:
  - `# Project Intake - [PROJECT_NAME]`
  - `## 1) Executive Summary`
  - `## 2) Project Type and Domain`
  - `## 3) Repository and Live URLs`
  - `## 4) Product/User Journey Summary`
  - `## 5) Architecture and Stack Summary`
  - `## 6) Key Workflows and Operational Flows`
  - `## 7) AI Context: Prompts, Chats, Agent Workflows`
  - `## 8) Supporting Docs and External Resources`
  - `## 9) Screenshot Gallery (with relative links + captions)`
  - `## 10) Candidate Import Nodes and Relationships`
  - `## 11) Risks, Gaps, and Unknowns`
  - `## 12) Handoff Checklist for Hyphenomenon Import`

5. Populate hydration artifacts correctly.
- Under section 8, include `### Hydration Source Artifacts`.
- Add 1-8 candidates with:
  - relative repo path link
  - canonical URL when available
  - artifact type label (`markdown | text | docx | pdf | image`)
  - short note explaining hydration value
- Include at least one markdown/text source and one image source.
- If no `.docx`/`.pdf` exists, state that explicitly in risks/gaps.

6. Keep output quality strict.
- Use concise, specific language.
- Mark unknown facts as `Unknown`.
- Verify screenshot links resolve from the dossier location.
- Treat the target output as a public logbook/proof record, not a glossy case study. The packet should show artifacts, workflows/process, decisions/tradeoffs, AI or automation use, human review, failures/limits, and enough narrative context to understand what happened.
- Avoid intake-framed public headings such as `What This Fresh Intake Proves`; write headings for readers inspecting the work and its evidence.
- Treat the dossier as source material, not public copy. Manually review the repository evidence, then author the project-page packet as the actual project record. Do not paste the dossier/checklist into the packet, and keep run mechanics such as pre-apply status, local preview waivers, source-branch correction, and screenshot-capture blockers out of the public project narrative unless the project itself is an intake/tooling project.
- Workflow packets should include at least four concrete steps, one decision/subprocess step, artifact or dry-run proof, a human/operator review point, project linkage, and source provenance.
- End the completion message with:
  - `files created/updated`
  - `unresolved unknowns`
  - `verification performed`

7. Hand off branch lifecycle explicitly.
- When the generated intake artifacts are committed on a dedicated branch, apply the target Hyphenomenon repo's `DOCS/intake/README.md` lifecycle standard before recommending merge or deletion.
- Project intake branches should merge only after validation, dry-run review, intentional apply, `ops:knowledge:drift`, and route/provenance verification.
- If the branch contains private review material, superseded artifacts, or unapplied diagnostics that should not become source history, do not recommend merging it.

## Source Priority

Prioritize these sources when available:
1. Repository docs (`DOCS/`, root governance files)
2. Route definitions and page components
3. Build/test/deploy/tooling configs
4. Live site behavior/screenshots
5. External references (only when materially useful)

## Resources

- `scripts/create_intake_scaffold.py`: Create intake markdown scaffold and screenshot directory.
- `scripts/verify_intake.py`: Validate required sections, files, and links.
- `references/template-hydration-artifacts.md`: Table template for hydration artifacts.
