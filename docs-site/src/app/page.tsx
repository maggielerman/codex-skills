import Link from "next/link";
import { ArrowRight, Boxes, CheckCircle2, ClipboardList, FileText, FolderKanban, LifeBuoy, Play, ShieldCheck, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { CatalogCard, FeaturedResource } from "@/components/site/catalog-card";
import { PageShell } from "@/components/site/shell";
import { catalogStats, pluginItems, skillItems } from "@/lib/catalog";
import { cn } from "@/lib/utils";

const workflowPreview = [
  { title: "Docs scaffolding", body: "Create implementation guides and project memory.", icon: FolderKanban },
  { title: "Tranche orchestration", body: "Plan and execute work in safer batches.", icon: Play },
  { title: "Shopify setup", body: "Stand up commerce workflows with clear steps.", icon: Boxes },
  { title: "UX audit", body: "Review journeys, screens, and quality evidence.", icon: ShieldCheck },
];

const stats = [
  { value: catalogStats.skills.toString(), label: "Skills", body: "Installable workflow folders" },
  { value: catalogStats.plugins.toString(), label: "Plugins", body: "Bundled product surfaces" },
  { value: "27", label: "Guides", body: "Generated customer pages" },
  { value: "4", label: "Starts", body: "Setup, catalog, plugin, support" },
];

const docCards = [
  {
    title: "Getting started",
    body: "Quick setup guides to install a pack and run your first workflow.",
    icon: ClipboardList,
    href: "/docs",
  },
  {
    title: "Skill catalog",
    body: "Browse skills by workflow, use case, lifecycle, and capability.",
    icon: FolderKanban,
    href: "#catalog",
  },
  {
    title: "Plugin bundles",
    body: "Understand plugin-backed workflows that need a larger install surface.",
    icon: Boxes,
    href: "#plugins",
  },
  {
    title: "Troubleshooting",
    body: "Answers for install friction, wrong audience, and first-run issues.",
    icon: LifeBuoy,
    href: "/docs#support",
  },
];

const trustedBy = ["Implementation teams", "Product operators", "Shopify builders", "Docs maintainers"];

export default function Home() {
  const featuredSkills = skillItems.slice(0, 4);
  const popularSkills = skillItems.slice(0, 5);

  return (
    <PageShell>
      <main>
        <section className="hero-wash relative overflow-hidden border-b border-border/70">
          <div className="absolute inset-0 soft-grid opacity-45" aria-hidden="true" />
          <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-24">
            <div className="flex flex-col gap-8">
              <Badge variant="secondary" className="w-fit rounded-full px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.12em] text-primary">Codex Skills Packs</Badge>
              <div className="flex flex-col gap-5">
                <h1 className="max-w-4xl font-heading text-5xl font-extrabold leading-[1.02] tracking-[-0.055em] sm:text-6xl lg:text-7xl">
                  Reusable Codex workflows for real customer repos.
                </h1>
                <p className="max-w-2xl text-lg leading-8 text-muted-foreground sm:text-xl">
                  Installable skills, plugin bundles, setup guides, and troubleshooting docs for teams putting Codex to work.
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <Link className={cn(buttonVariants({ size: "lg" }), "rounded-full px-5 shadow-sm")} href="/docs">
                  Explore the docs
                  <ArrowRight data-icon="inline-end" aria-hidden="true" />
                </Link>
                <Link className={cn(buttonVariants({ variant: "outline", size: "lg" }), "rounded-full bg-card/80 px-5")} href="#catalog">
                  Browse skills
                </Link>
              </div>
            </div>

            <div className="glass-card rounded-3xl border border-border/80 p-4 sm:p-5">
              <div className="mb-4 flex items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <span className="size-2.5 rounded-full bg-destructive/45" />
                  <span className="size-2.5 rounded-full bg-chart-3/55" />
                  <span className="size-2.5 rounded-full bg-accent" />
                </div>
                <Badge variant="outline" className="rounded-full">Workflow preview</Badge>
              </div>
              <div className="grid gap-3">
                {workflowPreview.map((item) => (
                  <div key={item.title} className="grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-border/80 bg-background/78 p-4 shadow-sm">
                    <span className="flex size-11 items-center justify-center rounded-2xl bg-secondary text-primary">
                      <item.icon aria-hidden="true" />
                    </span>
                    <div>
                      <h2 className="font-heading text-base font-bold tracking-[-0.02em]">{item.title}</h2>
                      <p className="mt-1 text-sm leading-6 text-muted-foreground">{item.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-10 sm:px-8">
          <div className="flex flex-wrap items-center gap-3 text-xs font-semibold uppercase tracking-[0.12em] text-muted-foreground">
            <span>Built for</span>
            {trustedBy.map((item) => (
              <span key={item} className="rounded-full border border-border/80 bg-card/80 px-3 py-1 normal-case tracking-normal text-foreground/72">{item}</span>
            ))}
          </div>
          <div className="grid overflow-hidden rounded-3xl border border-border/80 bg-card/78 shadow-sm md:grid-cols-4">
            {stats.map((stat) => (
              <div key={stat.label} className="border-b border-border/70 p-5 last:border-b-0 md:border-b-0 md:border-r md:last:border-r-0">
                <div className="font-heading text-3xl font-extrabold tracking-[-0.04em] text-foreground">{stat.value}</div>
                <div className="mt-1 text-sm font-bold text-foreground">{stat.label}</div>
                <p className="mt-1 text-sm text-muted-foreground">{stat.body}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="included" className="mx-auto grid max-w-7xl gap-5 px-5 py-12 sm:px-8 lg:grid-cols-4">
          {docCards.map((card) => (
            <Link key={card.title} href={card.href} className="group rounded-2xl border border-border/80 bg-card/84 p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg">
              <span className="flex size-11 items-center justify-center rounded-2xl bg-secondary text-primary">
                <card.icon aria-hidden="true" />
              </span>
              <h2 className="mt-5 font-heading text-xl font-bold tracking-[-0.03em]">{card.title}</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{card.body}</p>
              <span className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-primary">
                Open guide
                <ArrowRight className="size-4 transition group-hover:translate-x-0.5" aria-hidden="true" />
              </span>
            </Link>
          ))}
        </section>

        <section id="catalog" className="section-rule bg-card/35">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.78fr_1.22fr]">
            <SectionIntro
              eyebrow="Popular skills"
              title="Start with the workflows customers use first."
              body="The full docs hub includes every active, legacy, and deprecated item with setup notes and troubleshooting guidance. These are the quick entry points."
            />
            <div className="rounded-3xl border border-border/80 bg-card/86 p-3 shadow-sm">
              {popularSkills.map((item) => (
                <Link key={item.slug} href={`/skills/${item.slug}`} className="group grid grid-cols-[auto_1fr_auto] items-center gap-4 rounded-2xl p-4 transition hover:bg-secondary/70">
                  <span className="flex size-10 items-center justify-center rounded-2xl bg-secondary text-primary">
                    <FolderKanban aria-hidden="true" className="size-5" />
                  </span>
                  <span>
                    <span className="block font-heading text-base font-bold tracking-[-0.02em]">{item.title}</span>
                    <span className="mt-1 line-clamp-1 block text-sm text-muted-foreground">{item.summary}</span>
                  </span>
                  <ArrowRight className="size-4 text-muted-foreground transition group-hover:translate-x-0.5 group-hover:text-primary" aria-hidden="true" />
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-16 sm:px-8">
          <SectionIntro
            eyebrow="Skill guides"
            title="Each shipped workflow gets a customer guide."
            body="Catalog pages explain what the skill is for, how to run it for the first time, and what to check when the output misses the mark."
          />
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {featuredSkills.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
          <div className="rounded-3xl border border-primary/20 bg-secondary/70 p-6 sm:flex sm:items-center sm:justify-between sm:gap-6">
            <div>
              <h3 className="font-heading text-2xl font-bold tracking-[-0.035em]">Browse the complete implementation catalog.</h3>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">See all {catalogStats.skills} skill guides and {catalogStats.plugins} plugin guides generated from the shipped pack metadata.</p>
            </div>
            <Link href="/docs#all-skills" className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-primary sm:mt-0">
              View all docs
              <ArrowRight aria-hidden="true" className="size-4" />
            </Link>
          </div>
        </section>

        <section id="plugins" className="section-rule bg-card/35">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.85fr_1.15fr]">
            <SectionIntro
              eyebrow="Plugin bundles"
              title="Larger workflow surfaces are documented clearly."
              body="Some products ship as custom plugin bundles because they need metadata, scripts, assets, or bundled skills. The customer docs make that install shape explicit."
            />
            <div className="grid gap-5 md:grid-cols-2">
              {pluginItems.map((item) => (
                <CatalogCard key={item.slug} item={item} />
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-16 sm:px-8 lg:grid-cols-3">
          <FeaturedResource title="Setup without guesswork" body="Customers can start from install, first run, catalog selection, or troubleshooting depending on where they are in the workflow." />
          <FeaturedResource title="Generated from the shipped pack" body="Catalog pages come from suite metadata, so public docs stay aligned with what the buyer actually receives." />
          <FeaturedResource title="Support-oriented language" body="The site explains what to do next when a workflow is not triggered, produces the wrong audience, or needs repo context." />
        </section>
      </main>
    </PageShell>
  );
}

function SectionIntro({ eyebrow, title, body }: { eyebrow: string; title: string; body: string }) {
  return (
    <div className="flex max-w-3xl flex-col gap-4">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.13em] text-primary">
        <Sparkles aria-hidden="true" className="size-4" />
        {eyebrow}
      </div>
      <h2 className="font-heading text-4xl font-extrabold leading-tight tracking-[-0.05em] sm:text-5xl">{title}</h2>
      <p className="text-lg leading-8 text-muted-foreground">{body}</p>
      <div className="flex flex-wrap gap-3 text-sm font-semibold text-muted-foreground">
        <span className="inline-flex items-center gap-2"><CheckCircle2 aria-hidden="true" className="size-4 text-primary" /> Installable</span>
        <span className="inline-flex items-center gap-2"><FileText aria-hidden="true" className="size-4 text-primary" /> Documented</span>
        <span className="inline-flex items-center gap-2"><ShieldCheck aria-hidden="true" className="size-4 text-primary" /> Support-ready</span>
      </div>
    </div>
  );
}
