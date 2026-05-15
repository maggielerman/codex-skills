import Link from "next/link";
import { ArrowRight, CircleHelp, ClipboardCheck, Coffee, GitFork, PackageOpen, Wrench } from "lucide-react";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CatalogCard } from "@/components/site/catalog-card";
import { PageShell } from "@/components/site/shell";
import { allCatalogItems, catalogStats, pluginItems, skillItems } from "@/lib/catalog";

const repoHref = "https://github.com/maggielerman/codex-skills";

const setupSteps = [
  {
    title: "Read the source",
    body: "Start from the public repo and inspect the skill folder before copying it into your own Codex setup.",
  },
  {
    title: "Keep folders intact",
    body: "Scripts, references, assets, and metadata are part of the workflow. A flattened prompt loses useful context.",
  },
  {
    title: "Run in a real repo",
    body: "Open the target project, read its agent instructions, and invoke the skill with the specific outcome you want.",
  },
  {
    title: "Adapt deliberately",
    body: "Treat these as reference workflows. Keep what fits, adjust repo-specific conventions, and verify the output.",
  },
];

const faqs = [
  {
    q: "Is access gated?",
    a: "No. The direction is public repo first: share the workflows, explain how they work, and make support optional.",
  },
  {
    q: "Can I copy these skills into my own Codex setup?",
    a: "Yes, assuming the repository license and any bundled third-party notices permit your use case. Keep each folder intact so relative scripts and references still resolve.",
  },
  {
    q: "What is the point of a skill instead of a prompt?",
    a: "A skill packages trigger metadata, procedural rules, examples, scripts, and verification habits. That makes the workflow easier to repeat and improve over time.",
  },
  {
    q: "How should I support the work?",
    a: "Use the repo, star it, open issues when something is unclear, share useful adaptations, and use the support link once the public support destination is finalized.",
  },
];

export default function DocsPage() {
  return (
    <PageShell>
      <main>
        <section className="hero-wash border-b border-border/70">
          <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-16 sm:px-8 lg:py-20">
            <Badge variant="secondary" className="w-fit rounded-full px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.12em] text-primary">Library docs</Badge>
            <h1 className="max-w-4xl font-heading text-5xl font-extrabold leading-[1.05] tracking-[-0.055em] sm:text-6xl">
              Learn the workflow, then copy what is useful.
            </h1>
            <p className="max-w-3xl text-lg leading-8 text-muted-foreground sm:text-xl">
              These docs explain the public skill catalog, plugin backups, install shape, and practical operating assumptions behind Maggie Lerman&apos;s Codex workflows.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href={repoHref} className="inline-flex items-center gap-2 text-sm font-semibold text-primary">
                Open the public repo
                <ArrowRight aria-hidden="true" className="size-4" />
              </Link>
              <Link href="#all-skills" className="inline-flex items-center gap-2 text-sm font-semibold text-primary">
                Jump to catalog
                <ArrowRight aria-hidden="true" className="size-4" />
              </Link>
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-12 sm:px-8 lg:grid-cols-4">
          {setupSteps.map((step, index) => (
            <Card key={step.title} className="rounded-2xl border-border/80 bg-card/86 p-1 shadow-sm">
              <CardHeader className="p-5">
                <div className="flex size-10 items-center justify-center rounded-2xl bg-secondary text-sm font-bold text-primary">0{index + 1}</div>
                <CardTitle className="text-xl font-bold leading-tight tracking-[-0.03em]">{step.title}</CardTitle>
              </CardHeader>
              <CardContent className="p-5 pt-0">
                <p className="text-sm leading-6 text-muted-foreground">{step.body}</p>
              </CardContent>
            </Card>
          ))}
        </section>

        <section id="support" className="section-rule bg-card/35">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 lg:grid-cols-[0.85fr_1.15fr]">
            <div className="flex flex-col gap-5">
              <div className="flex size-12 items-center justify-center rounded-2xl bg-accent text-accent-foreground"><Wrench aria-hidden="true" /></div>
              <h2 className="font-heading text-4xl font-extrabold leading-tight tracking-[-0.05em]">A practical support model.</h2>
              <p className="text-lg leading-8 text-muted-foreground">
                The docs should help people evaluate and use the repo without a sales funnel. Support can happen through issues, contributions, and a simple buy-me-a-coffee style link once the public destination is final.
              </p>
            </div>
            <Accordion className="rounded-3xl border border-border/80 bg-card/86 p-4 shadow-sm" defaultValue={["item-0"]}>
              {faqs.map((faq, index) => (
                <AccordionItem key={faq.q} value={`item-${index}`}>
                  <AccordionTrigger>{faq.q}</AccordionTrigger>
                  <AccordionContent><p className="leading-6 text-muted-foreground">{faq.a}</p></AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>

        <section id="all-skills" className="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-14 sm:px-8">
          <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div className="flex flex-col gap-3">
              <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-primary"><PackageOpen aria-hidden="true" /></div>
              <h2 className="font-heading text-4xl font-extrabold tracking-[-0.05em]">Skill catalog</h2>
              <p className="max-w-3xl text-muted-foreground">{catalogStats.skills} skill guides generated from the suite manifest. Each page explains what the workflow is for and how to get a useful first run.</p>
            </div>
            <Link href="#plugins" className="inline-flex items-center gap-2 text-sm font-semibold text-primary">
              Jump to plugins
              <ArrowRight aria-hidden="true" className="size-4" />
            </Link>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {skillItems.map((item) => (
              <CatalogCard key={item.slug} item={item} compact />
            ))}
          </div>
        </section>

        <section id="plugins" className="mx-auto flex max-w-7xl flex-col gap-8 px-5 pb-16 sm:px-8">
          <div className="flex flex-col gap-3">
            <div className="flex size-12 items-center justify-center rounded-2xl bg-accent text-accent-foreground"><CircleHelp aria-hidden="true" /></div>
            <h2 className="font-heading text-4xl font-extrabold tracking-[-0.05em]">Plugin backups</h2>
            <p className="max-w-3xl text-muted-foreground">{pluginItems.length} custom plugin guides for larger local Codex surfaces that need plugin metadata, assets, scripts, or bundled skills.</p>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {pluginItems.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
          <Card className="rounded-3xl border-primary/20 bg-secondary/70 shadow-sm">
            <CardContent className="grid gap-4 p-6 md:grid-cols-[1fr_auto] md:items-center">
              <div>
                <h3 className="font-heading text-2xl font-bold tracking-[-0.035em]">The public catalog follows the repo.</h3>
                <p className="mt-2 text-sm text-muted-foreground">This docs site exposes {allCatalogItems.length} items generated from source metadata, not hand-maintained marketing pages.</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary" className="w-fit rounded-full"><ClipboardCheck aria-hidden="true" /> Source-backed</Badge>
                <Badge variant="outline" className="w-fit rounded-full"><GitFork aria-hidden="true" /> Public repo</Badge>
                <Badge variant="outline" className="w-fit rounded-full"><Coffee aria-hidden="true" /> Optional support</Badge>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>
    </PageShell>
  );
}
