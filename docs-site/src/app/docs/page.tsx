import { PageShell } from "@/components/site/shell";
import { LibraryBrowser } from "@/components/site/library-browser";
import { allCatalogItems, catalogStats } from "@/lib/catalog";
export default function DocsPage() {
  return (
    <PageShell>
      <main id="main">
        <section className="intro compact">
          <h1>The library.</h1>
          <p>
            {catalogStats.skills} curated skills and {catalogStats.plugins}{" "}
            custom plugins. Find a workflow,
            <br className="desktop-break" /> understand what it does, and
            explore its source.
          </p>
        </section>
        <LibraryBrowser items={allCatalogItems} />
      </main>
    </PageShell>
  );
}
