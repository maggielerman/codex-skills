import Link from "next/link";
import { ArrowLeft, CheckCircle2, ClipboardList, LifeBuoy, PackageCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { PageShell } from "@/components/site/shell";
import type { CatalogItem } from "@/lib/catalog-types";

export function DetailPage({ item }: { item: CatalogItem }) {
  return (
    <PageShell>
      <main>
        <section className="grain-field border-b border-border/70">
          <div className="mx-auto flex max-w-7xl flex-col gap-7 px-5 py-16 sm:px-8 lg:py-22">
            <Link href="/docs" className="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground transition hover:text-foreground">
              <ArrowLeft aria-hidden="true" />
              Back to docs hub
            </Link>
            <div className="flex flex-wrap gap-2">
              <Badge>{item.kind}</Badge>
              <Badge variant="secondary">{item.status}</Badge>
              <Badge variant="outline">{item.category}</Badge>
            </div>
            <div className="flex max-w-4xl flex-col gap-5">
              <h1 className="font-heading text-5xl font-semibold leading-none tracking-[-0.05em] sm:text-7xl">{item.title}</h1>
              <p className="text-lg leading-8 text-muted-foreground">{item.summary}</p>
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 lg:grid-cols-[0.75fr_1.25fr]">
          <aside className="flex flex-col gap-5">
            <Card className="bg-card/85">
              <CardHeader>
                <CardTitle className="text-xl">Pack metadata</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col gap-4 text-sm">
                <MetaRow label="Folder" value={item.folder} />
                <MetaRow label="Type" value={item.kind} />
                <MetaRow label="Status" value={item.status} />
                {item.path ? <MetaRow label="Source path" value={item.path} /> : null}
                <Separator />
                <div className="flex flex-wrap gap-2">
                  {item.resources.map((resource) => (
                    <Badge key={resource} variant="outline">{resource}</Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card className="bg-secondary/50">
              <CardContent className="flex flex-col gap-3 p-5">
                <div className="flex size-10 items-center justify-center rounded-2xl bg-primary text-primary-foreground"><LifeBuoy aria-hidden="true" /></div>
                <h2 className="font-heading text-2xl font-semibold tracking-tight">Support note</h2>
                <p className="text-sm leading-6 text-muted-foreground">
                  This page is for customer implementation. If you need to change the pack itself, use the repository maintenance docs instead.
                </p>
              </CardContent>
            </Card>
          </aside>

          <div className="flex flex-col gap-8">
            <Card className="bg-card/85">
              <CardHeader>
                <div className="flex size-12 items-center justify-center rounded-2xl bg-primary text-primary-foreground"><ClipboardList aria-hidden="true" /></div>
                <CardTitle className="font-heading text-3xl tracking-tight">When to use it</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="flex flex-col gap-3">
                  {item.useCases.map((useCase) => (
                    <li key={useCase} className="grid grid-cols-[auto_1fr] gap-3 text-sm leading-6 text-muted-foreground">
                      <CheckCircle2 aria-hidden="true" className="mt-0.5 text-primary" />
                      <span>{useCase}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <GuideSection title="Getting started" icon={<PackageCheck aria-hidden="true" />} items={item.gettingStarted} />
            <GuideSection title="Troubleshooting" icon={<LifeBuoy aria-hidden="true" />} items={item.troubleshooting} />

            <Card className="bg-card/85">
              <CardHeader>
                <CardTitle className="font-heading text-3xl tracking-tight">Implementation framing</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-7 text-muted-foreground">{item.description}</p>
              </CardContent>
            </Card>
          </div>
        </section>
      </main>
    </PageShell>
  );
}

function MetaRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs font-semibold uppercase tracking-[0.18em] text-muted-foreground">{label}</span>
      <span className="font-mono text-xs text-foreground">{value}</span>
    </div>
  );
}

function GuideSection({ title, icon, items }: { title: string; icon: React.ReactNode; items: readonly string[] }) {
  return (
    <Card className="bg-card/85">
      <CardHeader>
        <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground">{icon}</div>
        <CardTitle className="font-heading text-3xl tracking-tight">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="flex flex-col gap-4">
          {items.map((item, index) => (
            <li key={item} className="grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-border/70 bg-background/50 p-4">
              <span className="flex size-8 items-center justify-center rounded-xl bg-primary text-sm font-bold text-primary-foreground">{index + 1}</span>
              <span className="text-sm leading-6 text-muted-foreground">{item}</span>
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}
