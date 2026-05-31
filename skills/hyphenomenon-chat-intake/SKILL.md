---
name: hyphenomenon-chat-intake
author: Maggie Lerman
description: Intake a ChatGPT, Codex, Cursor, Gemini, or other AI conversation into Hyphenomenon as a chat object. Use when a user asks to capture, import, archive, or publish a chat/session/transcript, especially when raw transcripts, created skills, created projects, created repos, related projects, validation, sync, or rendered chat routes are involved.
---

# Hyphenomenon Chat Intake

Create a durable, transcript-backed Hyphenomenon chat intake artifact.

This skill covers chat/session/conversation intake. For repository/project dossiers, use `hyphenomenon-project-intake`.

## Workflow

1. Orient in the Hyphenomenon repo.
- Read `AGENTS.md`, `CHANGELOG.md`, `ROADMAP.md`, `DOCS/intake/README.md`, `DOCS/features/chats.md`, and `scripts/intake/chat/README.md`.
- Keep project `1059` in mind for chat intake contract changes unless a newer project supersedes it.

2. Capture the raw transcript.
- Store every intaked chat transcript in git under `scripts/intake/chat/runs/transcripts/`.
- Name it predictably, for example `<date>-<provider>-<session-or-share-id>-<slug>-transcript.txt`.
- The private transcript archive must be a complete source record, not a hand-written summary or curated retelling.
- Preserve the full turn/event sequence. Include tool calls and tool outputs in parseable form; summarize tool-output sections only when raw output is too large/noisy, and mark the section with raw-output size/hash or equivalent provenance.
- Mark every redaction explicitly. If there are no redactions, say so in the archive.
- For Codex local sessions, prefer the repo helper `npm run intake:chat:transcript:codex-jsonl -- --jsonl "/abs/path/to/rollout-...jsonl" --out "/abs/path/to/transcript.txt" --thread-id "<id>"`, which writes source metadata plus the complete JSONL event stream.
- For non-Codex exports, preserve speaker turns in parseable text such as `User:`, `Assistant:`, `Tool:`, and `System:`.
- Do not commit inline raw transcript text in JSON. Use `transcriptSourcePath`.

3. Build the JSON artifact.
- Save the run artifact under `scripts/intake/chat/runs/*.json`.
- Set `transcriptSourcePath` relative to the artifact file, normally `transcripts/<file>.txt`.
- Set `transcriptReviewedAt` after reviewing/redacting the transcript.
- Keep public content curated: `summary`, `highlights`, `decisions`, `contentBodyMarkdown`, verified `sourceExtracts`, optional `conversationRender.featuredMoment`, and public-safe links.
- Public summaries belong only in the JSON artifact/public fields; never use a public summary as the private transcript archive.
- `sourceExtracts[].excerpt` and `conversationRender.turns[].content` must be verbatim public-safe transcript excerpts, not summaries.

4. Capture created work.
- Use `createdArtifacts` for reusable artifacts created in the chat.
- Supported `type` values are `custom_skill`, `project`, and `repository`.
- Use `relatedProjects` for existing or newly created Hyphenomenon project context, with `created_from_conversation` or `created_from_decision` when appropriate.
- Keep private repo paths out of public link fields; `href` must be a site path or public non-GitHub URL.

5. Use screenshots only when they are real evidence.
- Real screenshots are good when they show an artifact, UI state, rendered route, diagram, product surface, or external visual proof created or discussed in the chat.
- Do not generate images of transcript text, source text, or quote cards as a substitute for provenance.
- If no real visual artifact exists, omit `featureImage` and `evidenceImages`.

6. Validate and sync.
```bash
npm run intake:validate:chat -- --artifact "scripts/intake/chat/runs/<artifact>.json"
npm run intake:sync:chat -- --artifact "scripts/intake/chat/runs/<artifact>.json"
npm run intake:sync:chat:apply -- --artifact "scripts/intake/chat/runs/<artifact>.json"
```

7. Verify the rendered route.
- Check `/chats/<slug>` after apply.
- Confirm the page renders curated public-safe content, optional real screenshots, related projects, and created artifacts.
- Confirm the page does not render or link the raw transcript by default.

8. Commit and push intake records.
- Commit the JSON artifact and transcript archive together.
- Commit optional real screenshot media only when it is public-safe and relevant.
- Push the branch when the user wants remote-backed transcript retention.
