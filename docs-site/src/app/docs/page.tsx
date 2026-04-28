import Link from "next/link";
import { ArrowRight, CircleHelp, ClipboardCheck, PackageOpen, Wrench } from "lucide-react";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CatalogCard } from "@/components/site/catalog-card";
import { PageShell } from "@/components/site/shell";
import { allCatalogItems, catalogStats, pluginItems, skillItems } from "@/lib/catalog";

const setupSteps = [
  {
    title: "Install the complete folder",
    body: "Keep each skill or plugin intact. Scripts, references, assets, and metadata are part of the workflow, not optional extras.",
  },
  {
    title: "Start in the target repo",
    body: "Open the customer repository first, read its agent instructions, and describe the outcome you want Codex to produce.",
  },
  {
    title: "Pick by outcome",
    body: "Choose the workflow for the job: planning, docs, Shopify setup, UX audit, environment sync, handoff, or implementation orchestration.",
  },
  {
    title: "Review the first run",
    body: "Inspect changed files, run generated checks, and adapt any docs, scripts, or code before adopting the output.",
  },
];

const faqs = [
  {
    q: "Is this a prompt library?",
    a: "No. The pack is a collection of installable Codex skills and custom plugin bundles. The value is the repeatable workflow around the prompt: trigger metadata, scripts, references, assets, operating rules, and implementation docs.",
  },
  {
    q: "Where do I install a purchased skill?",
    a: "Install it wherever your Codex environment loads custom skills. Keep the full skill folder intact so relative references and bundled scripts still resolve.",
  },
  {
    q: "Why did a skill write for the wrong audience?",
    a: "Some workflows can create either internal project memory or public customer docs. State the audience before rerunning and point Codex at the surface you want improved.",
  },
  {
    q: "How do I know which workflow to run first?",
    a: "If the repo is unclear, start with planning or docs scaffolding. If the scope is already known, use cluster or tranche workflows. If the repo needs quality evidence, use audit or review workflows.",
  },
];

export default function DocsPage() {
  return (
    <PageShell>
      <main>
        <section className="hero-wash border-b border-border/70">
          <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-16 sm:px-8 lg:py-20">
            <Badge variant="secondary" className="w-fit rounded-full px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.12em] text-primary">Customer docs</Badge>
            <h1 className="max-w-4xl font-heading text-5xl font-extrabold leading-[1.05] tracking-[-0.055em] sm:text-6xl">
              Put the skills pack to work in a real customer repo.
            </h1>
            <p className="max-w-3xl text-lg leading-8 text-muted-foreground sm:text-xl">
              Use these guides to install the pack, choose the right workflow, run a useful first pass, and troubleshoot common implementation issues.
            </p>
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
              <h2 className="font-heading text-4xl font-extrabold leading-tight tracking-[-0.05em]">Troubleshooting starts with context.</h2>
              <p className="text-lg leading-8 text-muted-foreground">
                Most issues come from incomplete installs, vague requests, missing repo instructions, or unclear audience. These checks help customers recover quickly.
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
              <p className="max-w-3xl text-muted-foreground">{catalogStats.skills} skill guides generated from the suite manifest. These pages explain what each workflow is for and how to start inside a customer repository.</p>
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
            <h2 className="font-heading text-4xl font-extrabold tracking-[-0.05em]">Plugin bundles</h2>
            <p className="max-w-3xl text-muted-foreground">{pluginItems.length} custom plugin guides for larger Codex workflow surfaces that need plugin metadata, assets, scripts, or bundled skills.</p>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {pluginItems.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
          <Card className="rounded-3xl border-primary/20 bg-secondary/70 shadow-sm">
            <CardContent className="flex flex-col gap-3 p-6 md:flex-row md:items-center md:justify-between">
              <div>
                <h3 className="font-heading text-2xl font-bold tracking-[-0.035em]">The public catalog follows the shipped pack.</h3>
                <p className="mt-2 text-sm text-muted-foreground">This docs site currently exposes {allCatalogItems.length} items from source metadata.</p>
              </div>
              <Badge variant="secondary" className="w-fit rounded-full"><ClipboardCheck aria-hidden="true" /> Source-backed</Badge>
            </CardContent>
          </Card>
        </section>
      </main>
    </PageShell>
  );
}
