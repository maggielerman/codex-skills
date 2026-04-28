#!/usr/bin/env node

import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const args = { input: null, output: null };
  for (let index = 2; index < argv.length; index += 1) {
    const current = argv[index];
    if (current === "--input") {
      args.input = argv[index + 1];
      index += 1;
    } else if (current === "--output") {
      args.output = argv[index + 1];
      index += 1;
    }
  }
  if (!args.input || !args.output) {
    throw new Error("Usage: render_journey_audit_pdf.mjs --input <manifest.json> --output <report.pdf>");
  }
  return args;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function mdInlineToHtml(text) {
  let html = escapeHtml(text ?? "");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label) => {
    return `<span class="file-ref">${escapeHtml(label)}</span>`;
  });
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  return html;
}

function normalizeColor(color, fallback) {
  if (typeof color === "string" && color.trim()) return color.trim();
  return fallback;
}

function hexToRgba(hex, alpha) {
  const normalized = hex.replace("#", "");
  const full = normalized.length === 3
    ? normalized.split("").map((char) => `${char}${char}`).join("")
    : normalized;
  const value = Number.parseInt(full, 16);
  const r = (value >> 16) & 255;
  const g = (value >> 8) & 255;
  const b = value & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function buildRolePalette(roles) {
  const fallbacks = ["#b74f2e", "#0b7a70", "#2b5fc7", "#8a3ffc", "#6e4c1e"];
  return roles.map((role, index) => {
    const color = normalizeColor(role.color, fallbacks[index % fallbacks.length]);
    return {
      ...role,
      color,
      bg: hexToRgba(color, 0.10),
      border: hexToRgba(color, 0.28),
    };
  });
}

function renderBasicTable(table, options = {}) {
  const headers = table?.headers ?? [];
  const rows = table?.rows ?? [];
  return `
    <table class="audit-table ${options.tableClass ?? ""}">
      <thead>
        <tr>${headers.map((header) => `<th>${mdInlineToHtml(header)}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows
          .map(
            (row) => `
              <tr>
                ${row
                  .map((cell) => `<td>${mdInlineToHtml(cell)}</td>`)
                  .join("")}
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function renderBulletList(items) {
  return `<ul class="findings-list">${(items ?? [])
    .map((item) => `<li>${mdInlineToHtml(item)}</li>`)
    .join("")}</ul>`;
}

function renderRouteReuseTable(routeReuse, roles) {
  const rows = (routeReuse ?? [])
    .map((row) => {
      const roleCells = roles
        .map((role) => {
          const paths = row.rolePaths?.[role.id] ?? [];
          return `
            <td class="route-role-cell role-${role.id}">
              <span class="role-chip role-${role.id}">${escapeHtml(role.label)}</span>
              <div class="path-chip-wrap">
                ${paths
                  .map(
                    (entry) =>
                      `<span class="path-chip role-${role.id}">${escapeHtml(entry)}</span>`,
                  )
                  .join("")}
              </div>
            </td>
          `;
        })
        .join("");

      return `
        <tr>
          <td class="route-col"><code>${escapeHtml(row.route)}</code></td>
          <td>${mdInlineToHtml(row.observedPurpose)}</td>
          ${roleCells}
        </tr>
      `;
    })
    .join("");

  return `
    <table class="audit-table route-reuse-table">
      <thead>
        <tr>
          <th>Route Pattern</th>
          <th>Observed Purpose</th>
          ${roles.map((role) => `<th class="role-${role.id}">${escapeHtml(role.label)} Entry Paths</th>`).join("")}
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderInventoryTable(inventory, role) {
  const rows = inventory?.rows ?? [];
  return `
    <table class="audit-table inventory-table">
      <thead>
        <tr>${(inventory?.headers ?? []).map((header) => `<th>${mdInlineToHtml(header)}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows
          .map((row) => {
            const screenshotHref = row.screenshot
              ? pathToFileURL(path.resolve(row.screenshot)).href
              : null;
            return `
              <tr>
                <td class="screen-id-cell"><span class="screen-id role-${role.id}">${escapeHtml(row.screenId)}</span></td>
                <td><code>${escapeHtml(row.url)}</code></td>
                <td>${mdInlineToHtml(row.how)}</td>
                <td>${mdInlineToHtml(row.next)}</td>
                <td class="screenshot-cell">
                  ${
                    screenshotHref
                      ? `<img class="thumb" src="${screenshotHref}" alt="${escapeHtml(row.screenId)} screenshot" />`
                      : ""
                  }
                  <div class="screenshot-label">${escapeHtml(row.screenshotLabel ?? "")}</div>
                </td>
                <td>${mdInlineToHtml(row.notes)}</td>
              </tr>
            `;
          })
          .join("")}
      </tbody>
    </table>
  `;
}

function renderRoleSection(roleReport, role) {
  return `
    <section class="role-section role-${role.id}">
      <div class="role-banner">
        <div>
          <div class="eyebrow">${escapeHtml(role.label)} current-state walkthrough</div>
          <h2>${escapeHtml(roleReport.title)}</h2>
          <p class="account-used">${mdInlineToHtml(roleReport.accountUsed ?? "")}</p>
        </div>
        <div class="role-meta">
          <span class="role-pill role-${role.id}">${escapeHtml(role.label)}</span>
          <span>Last updated: ${escapeHtml(roleReport.lastUpdated ?? "")}</span>
        </div>
      </div>
      <h3>Route Maps</h3>
      ${(roleReport.diagrams ?? [])
        .map(
          (diagram) => `
            <section class="diagram-block">
              <h4>${escapeHtml(diagram.title)}</h4>
              <div class="diagram-shell role-${role.id}">
                <div class="mermaid">${escapeHtml(diagram.mermaid)}</div>
              </div>
            </section>
          `,
        )
        .join("")}
      <h3>Current-State Findings</h3>
      ${renderBulletList(roleReport.findings ?? [])}
      <h3>Screen Inventory With Thumbnails</h3>
      ${renderInventoryTable(roleReport.inventory, role)}
    </section>
  `;
}

async function loadChromium() {
  const requireFromCwd = createRequire(path.join(process.cwd(), "__journey_audit_resolver__.js"));
  const candidates = ["@playwright/test", "playwright"];

  for (const candidate of candidates) {
    try {
      const resolvedPath = requireFromCwd.resolve(candidate);
      const imported = await import(pathToFileURL(resolvedPath).href);
      if (imported.chromium) {
        return imported.chromium;
      }
      if (imported.default?.chromium) {
        return imported.default.chromium;
      }
      if (imported["module.exports"]?.chromium) {
        return imported["module.exports"].chromium;
      }
    } catch {
      // Try the next candidate.
    }
  }

  throw new Error(
    "Unable to resolve Playwright from the current workspace. Install '@playwright/test' or 'playwright' in the repo before using the PDF renderer.",
  );
}

async function main() {
  const args = parseArgs(process.argv);
  const manifestPath = path.resolve(args.input);
  const outputPdf = path.resolve(args.output);
  const tmpDir = path.join(path.dirname(outputPdf), ".journey-audit-tmp");
  const htmlPath = path.join(tmpDir, "journey-audit-report.html");

  await fs.mkdir(path.dirname(outputPdf), { recursive: true });
  await fs.mkdir(tmpDir, { recursive: true });

  const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
  const roles = buildRolePalette(manifest.roles ?? []);

  const roleVars = roles
    .map(
      (role) => `
        --${role.id}: ${role.color};
        --${role.id}-bg: ${role.bg};
        --${role.id}-border: ${role.border};
      `,
    )
    .join("\n");

  const html = `
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>${escapeHtml(manifest.title)}</title>
        <style>
          @page {
            size: letter landscape;
            margin: 0.45in;
          }
          :root {
            color-scheme: light;
            --text: #172033;
            --muted: #56607a;
            --line: #d7ddea;
            --panel: #ffffff;
            --panel-soft: #f7f9fc;
            --danger-bg: #fff1f0;
            ${roleVars}
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            color: var(--text);
            background: #f4f6fb;
            line-height: 1.45;
          }
          .page-intro, .role-section {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 24px;
            margin: 0 0 22px;
            box-shadow: 0 14px 35px rgba(32, 51, 91, 0.08);
          }
          .cover-kicker, .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 10px;
            font-weight: 700;
            color: var(--muted);
          }
          h1 { font-size: 28px; line-height: 1.15; margin: 8px 0 12px; }
          h2 { font-size: 24px; margin: 0; }
          h3 { font-size: 18px; margin: 24px 0 12px; }
          h4 { font-size: 14px; margin: 0 0 8px; }
          p { margin: 0 0 12px; }
          .summary-grid {
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            gap: 18px;
            align-items: start;
          }
          .legend, .callout, .method-box {
            background: var(--panel-soft);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 14px;
          }
          .callout.current-state { background: #f7fbff; border-color: #cfe0ff; }
          .legend-row { display: flex; align-items: center; gap: 8px; margin: 6px 0; }
          .swatch {
            width: 16px; height: 16px; border-radius: 999px; border: 1px solid rgba(0,0,0,0.08);
          }
          .swatch.danger { background: var(--danger-bg); border-color: #efb6b3; }
          ${roles
            .map(
              (role) => `
                .swatch.${role.id} { background: var(--${role.id}-bg); border-color: var(--${role.id}-border); }
              `,
            )
            .join("\n")}
          .audit-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 18px;
            font-size: 10.5px;
            background: #fff;
          }
          .audit-table th, .audit-table td {
            border: 1px solid var(--line);
            padding: 8px 9px;
            text-align: left;
            vertical-align: top;
          }
          .audit-table thead th {
            background: #edf2fb;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
          }
          .route-col { width: 15%; }
          .path-chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
          .path-chip, .role-chip, .role-pill, .screen-id {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            font-weight: 700;
            line-height: 1;
          }
          .path-chip { padding: 6px 8px; font-size: 9.5px; border: 1px solid transparent; }
          .role-chip, .role-pill { padding: 6px 10px; font-size: 10px; }
          .screen-id { padding: 6px 9px; font-size: 10px; }
          ${roles
            .map(
              (role) => `
                .role-${role.id}.path-chip,
                .role-${role.id}.role-chip,
                .role-${role.id}.role-pill,
                .screen-id.role-${role.id},
                .diagram-shell.role-${role.id} {
                  background: var(--${role.id}-bg);
                  color: var(--${role.id});
                  border-color: var(--${role.id}-border);
                }
                .route-role-cell.role-${role.id},
                th.role-${role.id} {
                  background: var(--${role.id}-bg) !important;
                }
              `,
            )
            .join("\n")}
          .role-banner {
            display: flex;
            justify-content: space-between;
            align-items: start;
            gap: 16px;
            border-bottom: 1px solid var(--line);
            padding-bottom: 14px;
            margin-bottom: 14px;
          }
          .role-meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 10px;
            color: var(--muted);
            text-align: right;
          }
          .diagram-shell {
            border: 1px solid currentColor;
            border-radius: 16px;
            padding: 12px;
            overflow: hidden;
          }
          .mermaid { display: flex; justify-content: center; }
          .mermaid svg {
            max-width: 100%;
            max-height: 6.8in;
            height: auto !important;
            width: auto !important;
            display: block;
            margin: 0 auto;
          }
          .findings-list { margin: 0; padding-left: 20px; }
          .findings-list li { margin: 0 0 7px; }
          .inventory-table { table-layout: fixed; }
          .inventory-table th:nth-child(1), .inventory-table td:nth-child(1) { width: 7%; }
          .inventory-table th:nth-child(2), .inventory-table td:nth-child(2) { width: 19%; }
          .inventory-table th:nth-child(3), .inventory-table td:nth-child(3) { width: 16%; }
          .inventory-table th:nth-child(4), .inventory-table td:nth-child(4) { width: 16%; }
          .inventory-table th:nth-child(5), .inventory-table td:nth-child(5) { width: 22%; }
          .inventory-table th:nth-child(6), .inventory-table td:nth-child(6) { width: 20%; }
          .screenshot-cell { text-align: center; }
          .thumb {
            width: auto;
            max-width: 210px;
            max-height: 145px;
            border-radius: 10px;
            border: 1px solid var(--line);
            box-shadow: 0 8px 16px rgba(23, 32, 51, 0.08);
            background: #fff;
            object-fit: contain;
          }
          .screenshot-label { font-size: 9.5px; color: var(--muted); margin-top: 6px; overflow-wrap: anywhere; }
          .subtle-text { color: var(--muted); }
          code, .file-ref { font-family: "SFMono-Regular", "Menlo", monospace; font-size: 0.95em; }
          .page-break { page-break-before: always; }
        </style>
      </head>
      <body>
        <main>
          <section class="page-intro">
            <div class="cover-kicker">Current-state production audit</div>
            <h1>${escapeHtml(manifest.title)}</h1>
            <div class="summary-grid">
              <div>
                <p>${mdInlineToHtml(manifest.intro ?? "")}</p>
                <div class="callout current-state">
                  <strong>Scope lock:</strong> ${mdInlineToHtml(manifest.scopeLock ?? "")}
                </div>
              </div>
              <div class="legend">
                <strong>Color legend</strong>
                ${roles
                  .map(
                    (role) => `
                      <div class="legend-row"><span class="swatch ${role.id}"></span> ${escapeHtml(role.label)} route entries and screen IDs</div>
                    `,
                  )
                  .join("")}
                <div class="legend-row"><span class="swatch danger"></span> Broken or untrusted live routes</div>
              </div>
            </div>
            <div class="method-box">
              <p><strong>Generated at:</strong> ${escapeHtml(manifest.generatedAt ?? "")}</p>
              <p><strong>Audit root:</strong> <code>${escapeHtml(manifest.auditRoot ?? "")}</code></p>
            </div>
          </section>

          <section class="page-intro">
            <h2>Cross-Role Current-State Tables</h2>
            <h3>Cross-Role Comparison</h3>
            ${renderBasicTable(manifest.crossRoleComparison)}
            <h3>Route Reuse With Color-Coded Entry Paths</h3>
            ${renderRouteReuseTable(manifest.routeReuse, roles)}
            <h3>Redundancy Matrix</h3>
            ${renderBasicTable(manifest.redundancyMatrix)}
            <h3>Terminology Matrix</h3>
            ${renderBasicTable(manifest.terminologyMatrix)}
            <h3>Broken Or Untrusted Live Routes</h3>
            ${renderBasicTable(manifest.brokenRoutes)}
            <h3>Highest-Signal Production Findings</h3>
            ${renderBulletList(manifest.findings)}
            <h3>Prioritized Untangle Next</h3>
            ${renderBulletList(manifest.priorities)}
          </section>

          <section class="page-intro">
            <h2>Coverage Verification</h2>
            <p class="subtle-text">Last updated: ${escapeHtml(manifest.coverage?.updatedAt ?? "")}</p>
            <h3>Verdict</h3>
            ${renderBulletList(manifest.coverage?.verdict ?? [])}
            <h3>What The Current Audit Already Covers Well</h3>
            ${renderBasicTable(manifest.coverage?.covered)}
            <h3>Missing Current-State Dashboard Variants</h3>
            ${renderBasicTable(manifest.coverage?.missingDashboard)}
            <h3>Missing Reachable Public, Token, And Auth Handoff Routes</h3>
            ${renderBasicTable(manifest.coverage?.missingPublic)}
            <h3>What This Means For The Audit</h3>
            ${renderBulletList(manifest.coverage?.implications ?? [])}
          </section>

          <div class="page-break"></div>
          ${(manifest.roleReports ?? [])
            .map((roleReport, index) => {
              const role = roles.find((entry) => entry.id === roleReport.id) ?? roles[index];
              return `${index === 0 ? "" : '<div class="page-break"></div>'}${renderRoleSection(roleReport, role)}`;
            })
            .join("")}
        </main>

        <script type="module">
          import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
          try {
            mermaid.initialize({
              startOnLoad: false,
              theme: "neutral",
              securityLevel: "loose",
              flowchart: { htmlLabels: false, curve: "basis" },
            });
            await mermaid.run({ querySelector: ".mermaid" });
            window.__reportReady = true;
          } catch (error) {
            window.__reportError = String(error);
          }
        </script>
      </body>
    </html>
  `;

  await fs.writeFile(htmlPath, html, "utf8");

  const chromium = await loadChromium();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__reportReady === true || window.__reportError, null, {
    timeout: 30000,
  });
  const reportError = await page.evaluate(() => window.__reportError || null);
  if (reportError) {
    throw new Error(`Mermaid render failed: ${reportError}`);
  }

  await page.pdf({
    path: outputPdf,
    format: "Letter",
    landscape: true,
    printBackground: true,
    margin: { top: "0.35in", right: "0.35in", bottom: "0.5in", left: "0.35in" },
    displayHeaderFooter: true,
    headerTemplate: "<div></div>",
    footerTemplate: `
      <div style="width:100%;font-size:8px;padding:0 16px;color:#56607a;display:flex;justify-content:space-between;">
        <span>${escapeHtml(manifest.title)}</span>
        <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
      </div>
    `,
  });

  await browser.close();
  console.log(JSON.stringify({ input: manifestPath, output: outputPdf }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
