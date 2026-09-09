import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { PageShell } from "@/components/site/shell";
import { LibraryBrowser } from "@/components/site/library-browser";
import { allCatalogItems, catalogStats } from "@/lib/catalog";
const featured = [
  "rps-print-order",
  "context-layer",
  "motion-design-director",
  "catalog-review",
];
const items = [...allCatalogItems].sort((a, b) => {
  const x = featured.indexOf(a.slug),
    y = featured.indexOf(b.slug);
  return (x < 0 ? 99 : x) - (y < 0 ? 99 : y);
});
export default function HomePage() {
  return (
    <PageShell>
      <main id="main">
        <section className="intro">
          <h1>
            Better context.
            <br />
            More useful agents.
          </h1>
          <p>
            The skills and plugins I use to build products, run a print
            business,
            <br className="desktop-break" /> and keep human–agent work
            organized.
          </p>
        </section>
        <section className="context-feature" aria-labelledby="context-title">
          <div>
            <p className="feature-label">Start here</p>
            <h2 id="context-title">Context Layer</h2>
            <p>
              Project memory, decisions, and evidence
              <br className="desktop-break" /> that stay with your repository.
            </p>
            <Link href="/plugins/context-layer">
              Explore the plugin <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
          <pre aria-label="Example repository context structure">{`DOCS/\n├── PROJECTS/\n│   ├── active/\n│   └── in-review/\n├── evidence/\n└── development/`}</pre>
        </section>
        <section className="catalog-section" id="catalog">
          <div className="section-heading">
            <h2>Explore the library</h2>
            <span>
              {catalogStats.skills} skills · {catalogStats.plugins} plugins
            </span>
          </div>
          <LibraryBrowser items={items} />
        </section>
      </main>
    </PageShell>
  );
}
