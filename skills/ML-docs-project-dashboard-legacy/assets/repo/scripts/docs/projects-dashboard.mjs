#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DASHBOARD_MARKER = "<!-- docs-project-dashboard:generated -->";
const DOCS_ROOT_CANDIDATES = ["DOCS", "docs", "documentation"];
const LANE_ORDER = ["active", "in-review", "blocked", "completed", "backlog", "stale"];
const STATUS_ALIASES = new Map([
  ["active", "active"],
  ["in-progress", "active"],
  ["in progress", "active"],
  ["in-review", "in-review"],
  ["review", "in-review"],
  ["blocked", "blocked"],
  ["completed", "completed"],
  ["done", "completed"],
  ["backlog", "backlog"],
  ["stale", "stale"],
  ["paused", "stale"],
]);

function main() {
  const repoRoot = process.cwd();
  const docsRootName = process.argv[2];
  const docsRoot = resolveDocsRoot(repoRoot, docsRootName);
  const projectsRoot = resolveProjectsRoot(docsRoot);
  const projects = collectProjects(projectsRoot);
  const dashboardPath = path.join(projectsRoot, "dashboard.html");
  const output = buildDashboard({
    docsRootName: path.basename(docsRoot),
    projects,
  });

  fs.writeFileSync(dashboardPath, output, "utf8");
  console.log(`Wrote ${path.relative(repoRoot, dashboardPath)}`);
}

function resolveDocsRoot(repoRoot, explicitName) {
  if (explicitName) {
    const explicitPath = path.join(repoRoot, explicitName);
    if (!isDirectory(explicitPath)) {
      throw new Error(`Docs root not found: ${explicitPath}`);
    }
    return explicitPath;
  }

  const candidates = DOCS_ROOT_CANDIDATES
    .map((name) => path.join(repoRoot, name))
    .filter((candidate) => isDirectory(candidate));

  if (candidates.length === 0) {
    throw new Error("Could not find DOCS/, docs/, or documentation/.");
  }

  if (candidates.length === 1) {
    return candidates[0];
  }

  const ranked = candidates
    .map((candidate) => ({
      candidate,
      score:
        (hasChildDir(candidate, "PROJECTS") ? 10 : 0) +
        (exists(path.join(candidate, "README.md")) ? 2 : 0) +
        (exists(path.join(candidate, "index.md")) ? 1 : 0),
    }))
    .sort((a, b) => a.score - b.score);

  const best = ranked[ranked.length - 1];
  const secondBest = ranked[ranked.length - 2];

  if (secondBest && secondBest.score === best.score) {
    throw new Error("Multiple docs roots matched with the same score. Pass the docs root explicitly.");
  }

  return best.candidate;
}

function resolveProjectsRoot(docsRoot) {
  const entries = fs.readdirSync(docsRoot, { withFileTypes: true });
  const match = entries.find((entry) => entry.isDirectory() && entry.name.toLowerCase() === "projects");
  if (!match) {
    throw new Error(`Could not find PROJECTS/ under ${docsRoot}.`);
  }
  return path.join(docsRoot, match.name);
}

function collectProjects(projectsRoot) {
  const laneDirs = new Map();
  for (const entry of fs.readdirSync(projectsRoot, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      laneDirs.set(entry.name.toLowerCase(), entry.name);
    }
  }

  const projects = [];

  for (const lane of LANE_ORDER) {
    const actualLane = laneDirs.get(lane);
    if (!actualLane) {
      continue;
    }

    const laneRoot = path.join(projectsRoot, actualLane);
    for (const entry of fs.readdirSync(laneRoot, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) {
        continue;
      }
      if (entry.name === "README.md" || entry.name === "NNNN_project_template.md") {
        continue;
      }

      const filePath = path.join(laneRoot, entry.name);
      const source = fs.readFileSync(filePath, "utf8");
      const frontmatter = parseFrontmatter(source);
      projects.push(buildProjectRecord(projectsRoot, lane, filePath, source, frontmatter));
    }
  }

  return projects.sort(compareProjects);
}

function buildProjectRecord(projectsRoot, lane, filePath, source, frontmatter) {
  const title = frontmatter.title || humanizeFilename(path.basename(filePath, ".md"));
  const id = projectIdFromPath(filePath, title);
  const nextTargets = extractFirstBulletListAfterHeading(source, "Next Checkpoint Targets");
  const completedBullets = extractFirstBulletListAfterHeading(source, "Completed Since Prior Checkpoint");
  const openQuestions = extractSectionBullets(source, "Open Questions");
  const risks = extractSectionBullets(source, "Risks");
  const maggieTodos = extractMaggieTodos(source);
  const description = frontmatter.description || "";
  const relativePath = path.relative(projectsRoot, filePath).replaceAll(path.sep, "/");
  const status = frontmatter.status || "";
  const normalizedStatus = normalizeStatus(status);
  const focusText =
    maggieTodos[0] ||
    nextTargets[0] ||
    openQuestions[0] ||
    completedBullets[0] ||
    description ||
    "Open the planning doc for the latest checkpoint targets.";

  return {
    id,
    title,
    lane,
    status,
    normalizedStatus,
    priority: frontmatter.priority || "",
    owner: frontmatter.owner || "",
    parentProject: frontmatter.parentProject || "",
    programTrack: frontmatter.programTrack || "",
    lastUpdated: frontmatter.lastUpdated || "",
    lastUpdatedSort: sortableTimestamp(frontmatter.lastUpdated || ""),
    description,
    relativePath,
    nextTargets,
    completedBullets,
    maggieTodos,
    maggieTodoCount: maggieTodos.length,
    openQuestionCount: openQuestions.length,
    riskCount: risks.length,
    focusText,
    drift: normalizedStatus && normalizedStatus !== lane ? status : "",
    searchIndex: [
      id,
      title,
      lane,
      status,
      frontmatter.priority || "",
      frontmatter.owner || "",
      frontmatter.parentProject || "",
      frontmatter.programTrack || "",
      description,
      maggieTodos.join(" "),
      focusText,
    ]
      .join(" ")
      .toLowerCase(),
  };
}

function buildDashboard({ docsRootName, projects }) {
  const timestamp = easternTimestamp();
  const counts = new Map(LANE_ORDER.map((lane) => [lane, 0]));
  const laneProjects = new Map(LANE_ORDER.map((lane) => [lane, []]));
  const maggieTodoProjects = projects
    .filter((project) => project.maggieTodoCount > 0)
    .sort((a, b) => b.lastUpdatedSort.localeCompare(a.lastUpdatedSort));
  const recent = [...projects].sort((a, b) => b.lastUpdatedSort.localeCompare(a.lastUpdatedSort)).slice(0, 12);
  const trackProjects = [...projects]
    .filter((project) => project.parentProject || project.programTrack)
    .sort((a, b) => {
      const left = `${a.parentProject || trackPrefix(a.programTrack)} ${a.programTrack} ${a.id}`;
      const right = `${b.parentProject || trackPrefix(b.programTrack)} ${b.programTrack} ${b.id}`;
      return left.localeCompare(right, undefined, { numeric: true });
    });
  const driftProjects = projects.filter((project) => project.drift);

  for (const project of projects) {
    counts.set(project.lane, (counts.get(project.lane) || 0) + 1);
    laneProjects.get(project.lane)?.push(project);
  }

  const summaryCards = LANE_ORDER.map((lane) => {
    const laneList = [...(laneProjects.get(lane) || [])].sort((a, b) => b.lastUpdatedSort.localeCompare(a.lastUpdatedSort));
    const latest = laneList[0]?.lastUpdated || "None";
    return `
      <article class="summary-card lane-${lane}">
        <div class="summary-label">${escapeHtml(prettyLane(lane))}</div>
        <div class="summary-count">${counts.get(lane) || 0}</div>
        <div class="summary-meta">Latest update: ${escapeHtml(latest)}</div>
      </article>
    `;
  }).join("");

  const attentionColumns = [
    renderAttentionLane("Blocked", "blocked", laneProjects.get("blocked") || []),
    renderAttentionLane("In Review", "in-review", laneProjects.get("in-review") || []),
    renderAttentionLane("Active", "active", laneProjects.get("active") || []),
  ].join("");

  const maggieTodoTable = maggieTodoProjects.length === 0
    ? `<div class="empty-state">No unresolved MAGGIE TODO callouts found.</div>`
    : `
      <div class="table-shell">
        <table>
          <thead>
            <tr>
              <th>Project</th>
              <th>Lane</th>
              <th>MAGGIE TODO</th>
              <th>Updated</th>
              <th>Doc</th>
            </tr>
          </thead>
          <tbody>
            ${maggieTodoProjects.map((project) => project.maggieTodos.map((todo, index) => `
              <tr>
                <td>${index === 0 ? escapeHtml(project.title) : ""}</td>
                <td>${index === 0 ? `<span class="lane-badge lane-${project.lane}">${escapeHtml(prettyLane(project.lane))}</span>` : ""}</td>
                <td>${escapeHtml(truncate(todo, 180))}</td>
                <td>${index === 0 ? escapeHtml(project.lastUpdated || "Unknown") : ""}</td>
                <td>${index === 0 ? `<a href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">Open doc</a>` : ""}</td>
              </tr>
            `).join("")).join("")}
          </tbody>
        </table>
      </div>
    `;

  const tracksTable = trackProjects.length === 0
    ? `<div class="empty-state">No grouped program tracks found.</div>`
    : `
      <div class="table-shell">
        <table>
          <thead>
            <tr>
              <th>Parent</th>
              <th>Track</th>
              <th>Lane</th>
              <th>Project</th>
              <th>Updated</th>
              <th>Doc</th>
            </tr>
          </thead>
          <tbody>
            ${trackProjects.map((project) => `
              <tr>
                <td>${escapeHtml(project.parentProject || trackPrefix(project.programTrack) || "None")}</td>
                <td>${escapeHtml(project.programTrack || "None")}</td>
                <td><span class="lane-badge lane-${project.lane}">${escapeHtml(prettyLane(project.lane))}</span></td>
                <td>${escapeHtml(project.title)}</td>
                <td>${escapeHtml(project.lastUpdated || "Unknown")}</td>
                <td><a href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">Open doc</a></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;

  const recentTable = recent.length === 0
    ? `<div class="empty-state">No project docs found.</div>`
    : `
      <div class="table-shell">
        <table>
          <thead>
            <tr>
              <th>Updated</th>
              <th>Lane</th>
              <th>Project</th>
              <th>Focus</th>
              <th>Doc</th>
            </tr>
          </thead>
          <tbody>
            ${recent.map((project) => `
              <tr>
                <td>${escapeHtml(project.lastUpdated || "Unknown")}</td>
                <td><span class="lane-badge lane-${project.lane}">${escapeHtml(prettyLane(project.lane))}</span></td>
                <td>${escapeHtml(project.title)}</td>
                <td>${escapeHtml(truncate(project.focusText, 120))}</td>
                <td><a href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">Open doc</a></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;

  const driftTable = driftProjects.length === 0
    ? `<div class="empty-state">No lane/frontmatter drift detected.</div>`
    : `
      <div class="table-shell">
        <table>
          <thead>
            <tr>
              <th>Project</th>
              <th>Lane</th>
              <th>Frontmatter Status</th>
              <th>Doc</th>
            </tr>
          </thead>
          <tbody>
            ${driftProjects.map((project) => `
              <tr>
                <td>${escapeHtml(project.title)}</td>
                <td><span class="lane-badge lane-${project.lane}">${escapeHtml(prettyLane(project.lane))}</span></td>
                <td>${escapeHtml(project.status || "Unknown")}</td>
                <td><a href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">Open doc</a></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;

  const registerRows = [...projects]
    .sort((a, b) => `${a.id} ${a.title}`.localeCompare(`${b.id} ${b.title}`, undefined, { numeric: true }))
    .map((project) => `
      <tr data-lane="${escapeAttribute(project.lane)}" data-search="${escapeAttribute(project.searchIndex)}">
        <td>${escapeHtml(project.id)}</td>
        <td>
          <div class="register-title">${escapeHtml(project.title)}</div>
          <div class="register-subtitle">${escapeHtml(truncate(project.description || project.focusText, 120))}</div>
        </td>
        <td><span class="lane-badge lane-${project.lane}">${escapeHtml(prettyLane(project.lane))}</span></td>
        <td>${escapeHtml(project.priority || "None")}</td>
        <td>${escapeHtml(project.lastUpdated || "Unknown")}</td>
        <td>${escapeHtml(project.owner || "Unknown")}</td>
        <td>${project.openQuestionCount}</td>
        <td>${project.riskCount}</td>
        <td><a href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">Open doc</a></td>
      </tr>
    `)
    .join("");

  const totalMaggieTodos = maggieTodoProjects.reduce((count, project) => count + project.maggieTodoCount, 0);

  return `${DASHBOARD_MARKER}
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Project Dashboard</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f4efe7;
        --panel: rgba(255, 252, 248, 0.92);
        --panel-strong: #fffaf4;
        --line: rgba(77, 55, 29, 0.12);
        --text: #2b1f14;
        --muted: #6e5a45;
        --accent: #0f6d68;
        --accent-soft: rgba(15, 109, 104, 0.12);
        --blocked: #a63c22;
        --blocked-soft: rgba(166, 60, 34, 0.12);
        --review: #8b5e00;
        --review-soft: rgba(139, 94, 0, 0.12);
        --active: #0f6d68;
        --active-soft: rgba(15, 109, 104, 0.12);
        --completed: #42612b;
        --completed-soft: rgba(66, 97, 43, 0.12);
        --backlog: #5b5f8a;
        --backlog-soft: rgba(91, 95, 138, 0.12);
        --stale: #7b617c;
        --stale-soft: rgba(123, 97, 124, 0.12);
        --shadow: 0 18px 45px rgba(71, 48, 23, 0.08);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
        background:
          radial-gradient(circle at top left, rgba(255, 255, 255, 0.8), transparent 38%),
          linear-gradient(180deg, #f8f1e6 0%, var(--bg) 100%);
        color: var(--text);
      }

      a {
        color: var(--accent);
        text-decoration: none;
      }

      a:hover {
        text-decoration: underline;
      }

      .page {
        width: min(1380px, calc(100vw - 32px));
        margin: 24px auto 48px;
      }

      .hero {
        background: linear-gradient(135deg, rgba(255, 250, 244, 0.96), rgba(242, 233, 219, 0.92));
        border: 1px solid var(--line);
        border-radius: 28px;
        padding: 28px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
      }

      .hero::after {
        content: "";
        position: absolute;
        inset: auto -10% -30% auto;
        width: 320px;
        height: 320px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(15, 109, 104, 0.14), transparent 68%);
        pointer-events: none;
      }

      .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(77, 55, 29, 0.08);
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
      }

      h1 {
        margin: 16px 0 10px;
        font-size: clamp(2.2rem, 5vw, 4.2rem);
        line-height: 0.96;
        letter-spacing: -0.04em;
      }

      .hero p {
        max-width: 70ch;
        margin: 0;
        color: var(--muted);
        font-size: 1.05rem;
      }

      .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 18px;
      }

      .meta-pill {
        padding: 10px 14px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.74);
        border: 1px solid rgba(77, 55, 29, 0.08);
        font-size: 0.94rem;
      }

      .section {
        margin-top: 22px;
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 22px;
        box-shadow: var(--shadow);
      }

      .section-header {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: baseline;
        gap: 12px;
        margin-bottom: 16px;
      }

      .section-header h2 {
        margin: 0;
        font-size: 1.45rem;
        letter-spacing: -0.03em;
      }

      .section-header p {
        margin: 0;
        color: var(--muted);
      }

      .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 14px;
      }

      .summary-card {
        background: var(--panel-strong);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 18px;
      }

      .summary-label {
        font-size: 0.9rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }

      .summary-count {
        font-size: 2.4rem;
        line-height: 1;
        margin: 10px 0 8px;
      }

      .summary-meta {
        color: var(--muted);
        font-size: 0.92rem;
      }

      .attention-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
      }

      .attention-lane {
        background: var(--panel-strong);
        border-radius: 20px;
        border: 1px solid var(--line);
        padding: 16px;
        min-height: 220px;
      }

      .lane-heading {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        align-items: center;
        margin-bottom: 12px;
      }

      .lane-heading h3 {
        margin: 0;
        font-size: 1rem;
      }

      .lane-count {
        font-size: 0.85rem;
        color: var(--muted);
      }

      .project-card {
        display: block;
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 14px;
        margin-top: 10px;
      }

      .project-card:hover {
        text-decoration: none;
        border-color: rgba(15, 109, 104, 0.32);
        transform: translateY(-1px);
      }

      .project-title {
        font-weight: 700;
        color: var(--text);
        margin-bottom: 8px;
      }

      .project-meta {
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 8px;
      }

      .project-focus {
        color: var(--text);
        font-size: 0.95rem;
        line-height: 1.4;
      }

      .table-shell {
        overflow: auto;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.72);
      }

      table {
        width: 100%;
        border-collapse: collapse;
        min-width: 720px;
      }

      th,
      td {
        padding: 12px 14px;
        border-bottom: 1px solid var(--line);
        text-align: left;
        vertical-align: top;
      }

      th {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
        background: rgba(247, 240, 231, 0.92);
        position: sticky;
        top: 0;
      }

      tbody tr:hover {
        background: rgba(255, 255, 255, 0.66);
      }

      .lane-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.03em;
      }

      .lane-active { background: var(--active-soft); color: var(--active); }
      .lane-in-review { background: var(--review-soft); color: var(--review); }
      .lane-blocked { background: var(--blocked-soft); color: var(--blocked); }
      .lane-completed { background: var(--completed-soft); color: var(--completed); }
      .lane-backlog { background: var(--backlog-soft); color: var(--backlog); }
      .lane-stale { background: var(--stale-soft); color: var(--stale); }

      .filters {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 16px;
      }

      .filter-input,
      .filter-select {
        appearance: none;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 12px 14px;
        background: rgba(255, 255, 255, 0.9);
        color: var(--text);
        font: inherit;
      }

      .filter-input {
        min-width: 280px;
        flex: 1 1 280px;
      }

      .register-title {
        font-weight: 700;
        margin-bottom: 4px;
      }

      .register-subtitle {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.35;
      }

      .empty-state {
        padding: 18px;
        border: 1px dashed rgba(77, 55, 29, 0.18);
        border-radius: 16px;
        color: var(--muted);
        background: rgba(255, 255, 255, 0.54);
      }

      .register-footer {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 12px;
        color: var(--muted);
        font-size: 0.94rem;
      }

      @media (max-width: 980px) {
        .attention-grid {
          grid-template-columns: 1fr;
        }
      }

      @media (max-width: 720px) {
        .page {
          width: min(100vw - 20px, 1380px);
          margin-top: 10px;
        }

        .hero,
        .section {
          padding: 18px;
          border-radius: 18px;
        }
      }
    </style>
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="eyebrow">Docs Native PM View</div>
        <h1>Project Dashboard</h1>
        <p>
          Generated from <code>${escapeHtml(docsRootName)}/PROJECTS</code>. The source of truth remains the markdown
          planning docs in this repository.
        </p>
        <div class="hero-meta">
          <div class="meta-pill">Regenerate with <code>node scripts/docs/projects-dashboard.mjs ${escapeHtml(docsRootName)}</code></div>
          <div class="meta-pill">Generated ${escapeHtml(timestamp)}</div>
          <div class="meta-pill">${projects.length} tracked project${projects.length === 1 ? "" : "s"}</div>
          <div class="meta-pill">${totalMaggieTodos} MAGGIE TODO item${totalMaggieTodos === 1 ? "" : "s"}</div>
        </div>
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Portfolio Snapshot</h2>
          <p>Lane counts and freshest movement across the portfolio.</p>
        </div>
        <div class="summary-grid">${summaryCards}</div>
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Attention Queue</h2>
          <p>Immediate scanning lanes for blocked work, sign-off work, and active execution.</p>
        </div>
        <div class="attention-grid">${attentionColumns}</div>
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Maggie TODO</h2>
          <p>Manual input, evidence gathering, testing, approvals, or external work that still needs Maggie.</p>
        </div>
        ${maggieTodoTable}
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Program Tracks</h2>
          <p>Grouped child streams using <code>parentProject</code> and <code>programTrack</code>.</p>
        </div>
        ${tracksTable}
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Recently Updated</h2>
          <p>The newest frontmatter timestamps across all project lanes.</p>
        </div>
        ${recentTable}
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Status Drift</h2>
          <p>Cases where the lane folder and frontmatter status disagree.</p>
        </div>
        ${driftTable}
      </section>

      <section class="section">
        <div class="section-header">
          <h2>Full Register</h2>
          <p>Search and filter the full project set without leaving the local file.</p>
        </div>
        <div class="filters">
          <input id="register-search" class="filter-input" type="search" placeholder="Search title, owner, focus, track, or description" />
          <select id="register-lane" class="filter-select" aria-label="Filter register by lane">
            <option value="">All lanes</option>
            ${LANE_ORDER.map((lane) => `<option value="${escapeAttribute(lane)}">${escapeHtml(prettyLane(lane))}</option>`).join("")}
          </select>
        </div>
        <div class="table-shell">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Project</th>
                <th>Lane</th>
                <th>Priority</th>
                <th>Updated</th>
                <th>Owner</th>
                <th>Questions</th>
                <th>Risks</th>
                <th>Doc</th>
              </tr>
            </thead>
            <tbody id="register-body">
              ${registerRows}
            </tbody>
          </table>
        </div>
        <div class="register-footer">
          <div id="register-count">${projects.length} row${projects.length === 1 ? "" : "s"} shown</div>
          <div>Click any doc link to open the underlying markdown source.</div>
        </div>
      </section>
    </main>

    <script>
      const searchInput = document.getElementById("register-search");
      const laneSelect = document.getElementById("register-lane");
      const rowCount = document.getElementById("register-count");
      const rows = Array.from(document.querySelectorAll("#register-body tr"));

      function applyFilters() {
        const query = searchInput.value.trim().toLowerCase();
        const lane = laneSelect.value;
        let visible = 0;

        for (const row of rows) {
          const matchesQuery = !query || row.dataset.search.includes(query);
          const matchesLane = !lane || row.dataset.lane === lane;
          const show = matchesQuery && matchesLane;
          row.hidden = !show;
          if (show) {
            visible += 1;
          }
        }

        rowCount.textContent = visible + " row" + (visible === 1 ? "" : "s") + " shown";
      }

      searchInput.addEventListener("input", applyFilters);
      laneSelect.addEventListener("change", applyFilters);
    </script>
  </body>
</html>`;
}

function renderAttentionLane(title, lane, projects) {
  const sorted = [...projects].sort((a, b) => b.lastUpdatedSort.localeCompare(a.lastUpdatedSort));
  const cards = sorted.length === 0
    ? `<div class="empty-state">No ${escapeHtml(title.toLowerCase())} projects right now.</div>`
    : sorted.map((project) => `
      <a class="project-card" href="./${escapeAttribute(project.relativePath)}" target="_blank" rel="noreferrer">
        <div class="project-title">${escapeHtml(project.title)}</div>
        <div class="project-meta">
          ${escapeHtml(project.lastUpdated || "Unknown")}
          ${project.priority ? ` · priority ${escapeHtml(project.priority)}` : ""}
          ${project.programTrack ? ` · track ${escapeHtml(project.programTrack)}` : ""}
        </div>
        <div class="project-focus">${escapeHtml(truncate(project.focusText, 160))}</div>
      </a>
    `).join("");

  return `
    <section class="attention-lane">
      <div class="lane-heading">
        <h3><span class="lane-badge lane-${lane}">${escapeHtml(title)}</span></h3>
        <div class="lane-count">${sorted.length} item${sorted.length === 1 ? "" : "s"}</div>
      </div>
      ${cards}
    </section>
  `;
}

function parseFrontmatter(source) {
  if (!source.startsWith("---\n")) {
    return {};
  }

  const end = source.indexOf("\n---\n", 4);
  if (end === -1) {
    return {};
  }

  const block = source.slice(4, end);
  const result = {};

  for (const line of block.split("\n")) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) {
      continue;
    }

    const [, key, rawValue] = match;
    let value = rawValue.trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }

  return result;
}

function extractFirstBulletListAfterHeading(source, heading) {
  const lines = source.split("\n");
  const headingLine = `#### ${heading}`;
  const start = lines.findIndex((line) => line.trim() === headingLine);
  if (start === -1) {
    return [];
  }

  const bullets = [];
  let collecting = false;

  for (let index = start + 1; index < lines.length; index += 1) {
    const trimmed = lines[index].trim();

    if (!collecting) {
      if (!trimmed) {
        continue;
      }
      collecting = true;
    }

    if (trimmed.startsWith("### ") || trimmed.startsWith("#### ") || trimmed.startsWith("## ")) {
      break;
    }

    if (trimmed.startsWith("- ")) {
      bullets.push(trimmed.slice(2).trim());
      continue;
    }

    if (trimmed && bullets.length > 0) {
      break;
    }
  }

  return bullets;
}

function extractSectionBullets(source, sectionTitle) {
  const lines = source.split("\n");
  const headingLine = `## ${sectionTitle}`;
  const start = lines.findIndex((line) => line.trim() === headingLine);
  if (start === -1) {
    return [];
  }

  const bullets = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    const trimmed = lines[index].trim();
    if (trimmed.startsWith("## ")) {
      break;
    }
    if (trimmed.startsWith("- ")) {
      bullets.push(trimmed.slice(2).trim());
    }
  }
  return bullets;
}

function extractMaggieTodos(source) {
  const seen = new Set();
  const todos = [];

  for (const line of source.split("\n")) {
    const match = line.match(/^\s*(?:[-*]\s+|>\s*)?MAGGIE TODO:\s*(.+?)\s*$/);
    if (!match) {
      continue;
    }

    const value = match[1].replace(/\s+/g, " ").trim();
    if (!value) {
      continue;
    }

    const dedupeKey = value.toLowerCase();
    if (seen.has(dedupeKey)) {
      continue;
    }

    seen.add(dedupeKey);
    todos.push(value);
  }

  return todos;
}

function normalizeStatus(status) {
  return STATUS_ALIASES.get(String(status || "").trim().toLowerCase()) || String(status || "").trim().toLowerCase();
}

function sortableTimestamp(value) {
  const match = String(value || "").match(/^(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?/);
  if (!match) {
    return "0000-00-00 00:00";
  }
  const [, datePart, timePart = "00:00"] = match;
  return `${datePart} ${timePart}`;
}

function projectIdFromPath(filePath, title) {
  const basename = path.basename(filePath);
  const filenameMatch = basename.match(/^(\d{4,})/);
  if (filenameMatch) {
    return filenameMatch[1];
  }
  const titleMatch = title.match(/^(\d{4,})/);
  if (titleMatch) {
    return titleMatch[1];
  }
  return basename.replace(/\.md$/, "");
}

function humanizeFilename(value) {
  return value
    .replace(/^\d+_/, "")
    .replaceAll("_", " ")
    .replace(/\s+/g, " ")
    .trim();
}

function prettyLane(lane) {
  if (lane === "in-review") {
    return "In Review";
  }
  return lane.charAt(0).toUpperCase() + lane.slice(1);
}

function easternTimestamp() {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/New_York",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).formatToParts(new Date());

  const get = (type) => parts.find((part) => part.type === type)?.value || "00";
  return `${get("year")}-${get("month")}-${get("day")} ${get("hour")}:${get("minute")} ET (America/New_York)`;
}

function trackPrefix(programTrack) {
  if (!programTrack || !String(programTrack).includes("-")) {
    return "";
  }
  return String(programTrack).split("-")[0];
}

function truncate(value, maxLength) {
  const compact = String(value || "").replace(/\s+/g, " ").trim();
  if (compact.length <= maxLength) {
    return compact;
  }
  return `${compact.slice(0, maxLength - 3).trimEnd()}...`;
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

function exists(targetPath) {
  return fs.existsSync(targetPath);
}

function isDirectory(targetPath) {
  return exists(targetPath) && fs.statSync(targetPath).isDirectory();
}

function hasChildDir(parent, name) {
  return fs
    .readdirSync(parent, { withFileTypes: true })
    .some((entry) => entry.isDirectory() && entry.name.toLowerCase() === name.toLowerCase());
}

function compareProjects(left, right) {
  const laneComparison = LANE_ORDER.indexOf(left.lane) - LANE_ORDER.indexOf(right.lane);
  if (laneComparison !== 0) {
    return laneComparison;
  }
  return left.title.localeCompare(right.title, undefined, { numeric: true });
}

main();
