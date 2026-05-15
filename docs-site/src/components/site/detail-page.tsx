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
        <section className="hero-wash border-b border-border/70">
          <div className="mx-auto flex max-w-7xl flex-col gap-7 px-5 py-14 sm:px-8 lg:py-18">
            <Link href="/docs" className="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground transition hover:text-primary">
              <ArrowLeft aria-hidden="true" className="size-4" />
              Back to library
            </Link>
            <div className="flex flex-wrap gap-2">
              <Badge className="rounded-full capitalize">{item.kind}</Badge>
              <Badge variant="secondary" className="rounded-full capitalize">{item.status}</Badge>
              <Badge variant="outline" className="rounded-full capitalize">{item.category}</Badge>
            </div>
            <div className="flex max-w-4xl flex-col gap-5">
              <h1 className="font-heading text-5xl font-extrabold leading-[1.05] tracking-[-0.055em] sm:text-6xl">{item.title}</h1>
              <p className="text-lg leading-8 text-muted-foreground sm:text-xl">{item.summary}</p>
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 lg:grid-cols-[0.72fr_1.28fr]">
          <aside className="flex flex-col gap-5">
            <Card className="rounded-3xl border-border/80 bg-card/86 p-1 shadow-sm">
              <CardHeader className="p-5">
                <CardTitle className="text-xl font-bold tracking-[-0.03em]">Source metadata</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col gap-4 p-5 pt-0 text-sm">
                <MetaRow label="Folder" value={item.folder} />
                <MetaRow label="Asset type" value={item.kind} />
                <MetaRow label="Lifecycle" value={item.status} />
                {item.path ? <MetaRow label="Source path" value={item.path} /> : null}
                <Separator />
                <div className="flex flex-wrap gap-2">
                  {item.resources.map((resource) => (
                    <Badge key={resource} variant="outline" className="rounded-full capitalize">{resource}</Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card className="rounded-3xl border-primary/20 bg-secondary/70 shadow-sm">
              <CardContent className="flex flex-col gap-3 p-5">
                <div className="flex size-11 items-center justify-center rounded-2xl bg-primary text-primary-foreground"><LifeBuoy aria-hidden="true" /></div>
                <h2 className="font-heading text-2xl font-bold tracking-[-0.035em]">Library note</h2>
                <p className="text-sm leading-6 text-muted-foreground">
                  This page explains when the workflow is useful, what ships with it, and how to adapt it in your own repo.
                </p>
              </CardContent>
            </Card>
          </aside>

          <div className="flex flex-col gap-8">
            <Card className="rounded-3xl border-border/80 bg-card/86 p-1 shadow-sm">
              <CardHeader className="p-5">
                <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-primary"><ClipboardList aria-hidden="true" /></div>
                <CardTitle className="font-heading text-3xl font-extrabold tracking-[-0.045em]">Use this when</CardTitle>
              </CardHeader>
              <CardContent className="p-5 pt-0">
                <ul className="grid gap-3 md:grid-cols-2">
                  {item.useCases.map((useCase) => (
                    <li key={useCase} className="grid grid-cols-[auto_1fr] gap-3 rounded-2xl border border-border/80 bg-background/70 p-4 text-sm leading-6 text-muted-foreground">
                      <CheckCircle2 aria-hidden="true" className="mt-0.5 size-4 text-primary" />
                      <span>{useCase}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <GuideSection title="First run" icon={<PackageCheck aria-hidden="true" />} items={item.gettingStarted} />
            <GuideSection title="If it gets stuck" icon={<LifeBuoy aria-hidden="true" />} items={item.troubleshooting} />

            <Card className="rounded-3xl border-border/80 bg-card/86 p-1 shadow-sm">
              <CardHeader className="p-5">
                <CardTitle className="font-heading text-3xl font-extrabold tracking-[-0.045em]">Source description</CardTitle>
              </CardHeader>
              <CardContent className="p-5 pt-0">
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
      <span className="font-mono text-[0.66rem] font-semibold uppercase tracking-[0.14em] text-muted-foreground">{label}</span>
      <span className="break-words font-mono text-xs text-foreground/78">{value}</span>
    </div>
  );
}

function GuideSection({ title, icon, items }: { title: string; icon: React.ReactNode; items: readonly string[] }) {
  return (
    <Card className="rounded-3xl border-border/80 bg-card/86 p-1 shadow-sm">
      <CardHeader className="p-5">
        <div className="flex size-12 items-center justify-center rounded-2xl bg-accent text-accent-foreground">{icon}</div>
        <CardTitle className="font-heading text-3xl font-extrabold tracking-[-0.045em]">{title}</CardTitle>
      </CardHeader>
      <CardContent className="p-5 pt-0">
        <ol className="grid gap-4">
          {items.map((item, index) => (
            <li key={item} className="grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-border/80 bg-background/70 p-4">
              <span className="flex size-8 items-center justify-center rounded-full bg-secondary text-xs font-bold text-primary">{index + 1}</span>
              <span className="text-sm leading-6 text-muted-foreground">{item}</span>
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}
