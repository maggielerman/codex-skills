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
    title: "Unpack without flattening folders",
    body: "Skills and plugins rely on nearby scripts, references, assets, and metadata. Keep each delivered folder self-contained when copying it into a customer environment.",
  },
  {
    title: "Refresh Codex visibility",
    body: "Restart or refresh Codex after installation so new skills, plugin metadata, and trigger descriptions are loaded before the first customer workflow run.",
  },
  {
    title: "Invoke against a target repo",
    body: "Open the customer repository, read its agent instructions, and invoke the skill with a concrete result such as scaffold docs, split work, audit journeys, or create Shopify app modules.",
  },
  {
    title: "Review before adoption",
    body: "Treat generated docs, scripts, and code as implementation proposals. Run local checks and adapt customer-specific policies before committing changes.",
  },
];

const faqs = [
  {
    q: "Codex did not trigger the skill. What should I do?",
    a: "Invoke the skill by name and include the target outcome. Trigger metadata is optimized for natural language, but explicit invocation is the fastest path when a repo has unusual terminology.",
  },
  {
    q: "A docs scaffold sounds too internal for customers.",
    a: "Restate the audience before rerunning: customer-facing setup, implementation, and troubleshooting. Do not ask for repo operations docs unless the customer actually needs internal governance scaffolding.",
  },
  {
    q: "A bundled script cannot find files.",
    a: "Run scripts from the target repo root unless the skill says otherwise, and confirm the copied skill/plugin retained its scripts, references, assets, and metadata folders.",
  },
  {
    q: "How should we choose between skills?",
    a: "Start from the customer workflow outcome. Use docs-system skills for operating structure, review skills for audits, tranche skills for managed execution, and commerce skills for Shopify/catalog work.",
  },
];

export default function DocsPage() {
  return (
    <PageShell>
      <main>
        <section className="grain-field border-b border-border/70">
          <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-16 sm:px-8 lg:py-24">
            <Badge variant="secondary" className="w-fit rounded-full">Purchased pack implementation</Badge>
            <h1 className="max-w-4xl font-heading text-5xl font-semibold leading-none tracking-[-0.05em] sm:text-7xl">
              Customer docs for installing and operating skills packs.
            </h1>
            <p className="max-w-3xl text-lg leading-8 text-muted-foreground">
              Use these pages when you have purchased or received the skills pack and want to apply it inside your own repositories, teams, and Codex workflows. This site intentionally avoids internal repository maintenance instructions.
            </p>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-14 sm:px-8 lg:grid-cols-4">
          {setupSteps.map((step, index) => (
            <Card key={step.title} className="bg-card/85">
              <CardHeader>
                <div className="flex size-11 items-center justify-center rounded-2xl bg-primary text-primary-foreground">{index + 1}</div>
                <CardTitle className="text-xl">{step.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-6 text-muted-foreground">{step.body}</p>
              </CardContent>
            </Card>
          ))}
        </section>

        <section className="border-y border-border/70 bg-card/45">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="flex flex-col gap-5">
              <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground"><Wrench aria-hidden="true" /></div>
              <h2 className="font-heading text-4xl font-semibold tracking-[-0.04em]">Troubleshooting flow</h2>
              <p className="text-lg leading-8 text-muted-foreground">
                Most implementation friction comes from missing context, flattened folders, or asking a repo-operating skill to produce public docs. Work through these checks before assuming the pack is broken.
              </p>
            </div>
            <Accordion className="rounded-3xl border border-border/70 bg-card/85 p-4" defaultValue={["item-0"]}>
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
              <div className="flex size-12 items-center justify-center rounded-2xl bg-primary text-primary-foreground"><PackageOpen aria-hidden="true" /></div>
              <h2 className="font-heading text-4xl font-semibold tracking-[-0.04em]">All skill docs</h2>
              <p className="max-w-3xl text-muted-foreground">{catalogStats.skills} customer-facing skill guides generated from the suite catalog.</p>
            </div>
            <Link href="#plugins" className="inline-flex items-center gap-2 text-sm font-semibold text-primary">
              Jump to plugins
              <ArrowRight aria-hidden="true" />
            </Link>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {skillItems.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
        </section>

        <section id="plugins" className="mx-auto flex max-w-7xl flex-col gap-8 px-5 pb-16 sm:px-8">
          <div className="flex flex-col gap-3">
            <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground"><CircleHelp aria-hidden="true" /></div>
            <h2 className="font-heading text-4xl font-semibold tracking-[-0.04em]">Plugin docs</h2>
            <p className="max-w-3xl text-muted-foreground">{pluginItems.length} custom plugin guides focused on installability and customer workflow setup.</p>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {pluginItems.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
          <Card className="bg-secondary/50">
            <CardContent className="flex flex-col gap-3 p-6 md:flex-row md:items-center md:justify-between">
              <div>
                <h3 className="font-heading text-2xl font-semibold">Catalog source</h3>
                <p className="mt-1 text-sm text-muted-foreground">These docs currently expose {allCatalogItems.length} items from generated metadata.</p>
              </div>
              <Badge variant="outline" className="w-fit"><ClipboardCheck aria-hidden="true" /> Generated, not hand-copied</Badge>
            </CardContent>
          </Card>
        </section>
      </main>
    </PageShell>
  );
}
