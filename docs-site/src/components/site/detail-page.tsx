import Link from "next/link";
import { ArrowLeft, ArrowUpRight } from "lucide-react";
import { existsSync, readdirSync } from "node:fs";
import { resolve, relative } from "node:path";
import { PageShell } from "@/components/site/shell";
import type { CatalogItem } from "@/lib/catalog-types";
const repo = "https://github.com/maggielerman/codex-skills";
function sourceFiles(item: CatalogItem) {
  const root = existsSync(resolve(process.cwd(), "skills/SUITE_SKILLS.txt"))
    ? process.cwd()
    : resolve(process.cwd(), "..");
  const folder = resolve(
    root,
    item.kind === "skill" ? `skills/${item.folder}` : `plugins/${item.folder}`,
  );
  const inner = resolve(
    folder,
    item.kind === "plugin" ? "skills" : "references",
  );
  if (!existsSync(inner)) return [];
  return readdirSync(inner, { withFileTypes: true })
    .filter((entry) =>
      item.kind === "plugin" ? entry.isDirectory() : entry.isFile(),
    )
    .map((entry) => ({
      label: entry.name.replace(/\.md$/, ""),
      path: relative(
        root,
        resolve(inner, entry.name, item.kind === "plugin" ? "SKILL.md" : ""),
      ),
    }));
}
export function DetailPage({ item }: { item: CatalogItem }) {
  const files = sourceFiles(item);
  const path = `${item.kind}s/${item.folder}`;
  const source = `${repo}/tree/main/${path}`;
  return (
    <PageShell>
      <main id="main">
        <header className="detail-head">
          <Link href="/docs" className="back-link">
            <ArrowLeft size={15} aria-hidden="true" />
            Back to library
          </Link>
          <div className="detail-meta">
            <span className={`type-label ${item.kind}`}>{item.kind}</span>
            <span>{item.status}</span>
          </div>
          <h1>{item.title}</h1>
          <p>
            {item.summary !== "|"
              ? item.summary
              : "Read the workflow instructions and source files."}
          </p>
          <a className="source-link" href={source}>
            View complete source <ArrowUpRight size={16} aria-hidden="true" />
          </a>
        </header>
        <div className="detail-layout">
          <article className="article-body">
            <section id="overview">
              <h2>What it does</h2>
              <p>
                {item.description !== "|"
                  ? item.description
                  : "This workflow is maintained in the repository. Read its SKILL.md for the full instructions."}
              </p>
            </section>
            <section id="use">
              <h2>Try it when you need to…</h2>
              <ol>
                {item.useCases.map((text) => (
                  <li key={text}>{text}</li>
                ))}
              </ol>
            </section>
            <section id="start">
              <h2>Your first run</h2>
              <ol>
                {item.gettingStarted.map((text) => (
                  <li key={text}>{text}</li>
                ))}
              </ol>
              <p>
                New to this collection? Read{" "}
                <Link href="/getting-started">Getting started</Link> for package
                structure, setup, and license notes.
              </p>
            </section>
            {files.length > 0 && (
              <section id="included">
                <h2>
                  {item.kind === "plugin"
                    ? "Included skills"
                    : "Reference guides"}
                </h2>
                <ul className="file-links">
                  {files.map((file) => (
                    <li key={file.path}>
                      <a href={`${repo}/blob/main/${file.path}`}>
                        {file.label}
                        <ArrowUpRight size={15} aria-hidden="true" />
                      </a>
                    </li>
                  ))}
                </ul>
              </section>
            )}
            <section id="troubleshooting">
              <h2>If something gets stuck</h2>
              {item.troubleshooting.map((text, i) => (
                <details key={text}>
                  <summary>
                    {i === 0
                      ? "The workflow is unavailable"
                      : i === 1
                        ? "Files or results are missing"
                        : "The result needs adjusting"}
                  </summary>
                  <p>{text}</p>
                </details>
              ))}
            </section>
          </article>
          <aside className="detail-aside">
            <p>On this page</p>
            <a href="#overview">What it does</a>
            <a href="#use">When to use it</a>
            <a href="#start">Your first run</a>
            {files.length > 0 && <a href="#included">Included resources</a>}
            <a href="#troubleshooting">Troubleshooting</a>
            <dl>
              <dt>Category</dt>
              <dd>{item.category}</dd>
              <dt>Source folder</dt>
              <dd>{path}</dd>
            </dl>
          </aside>
        </div>
      </main>
    </PageShell>
  );
}
