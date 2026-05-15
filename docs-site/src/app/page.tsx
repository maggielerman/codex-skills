import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  Boxes,
  Coffee,
  FolderKanban,
  GitFork,
  HeartHandshake,
  Library,
  NotebookTabs,
  PackageOpen,
  Sparkles,
  Wrench,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { CatalogCard, FeaturedResource } from "@/components/site/catalog-card";
import { PageShell } from "@/components/site/shell";
import { catalogStats, pluginItems, skillItems } from "@/lib/catalog";
import { cn } from "@/lib/utils";

const repoHref = "https://github.com/maggielerman/codex-skills";
const supportHref = `${repoHref}#support-direction`;

const notes = [
  {
    title: "Repo-native context layers",
    body: "How I structure docs, evidence, project memory, and agent instructions so humans and Codex can share state.",
    icon: NotebookTabs,
  },
  {
    title: "Reusable workflows over one-off prompts",
    body: "Skills are small operating procedures: trigger metadata, references, scripts, and quality checks packaged together.",
    icon: Wrench,
  },
  {
    title: "Practical automation boundaries",
    body: "The useful line is not full autonomy. It is knowing which work should be scripted, reviewed, delegated, or stopped.",
    icon: FolderKanban,
  },
];

const stats = [
  { value: catalogStats.skills.toString(), label: "Skills", body: "Portable workflow folders" },
  { value: catalogStats.plugins.toString(), label: "Plugins", body: "Custom local plugin backups" },
  { value: "Open", label: "Repository", body: "Public learning and reuse" },
  { value: "Living", label: "Notes", body: "Updated as the workflows evolve" },
];

export default function Home() {
  const featuredSkills = skillItems.slice(0, 6);
  const featuredPlugins = pluginItems.slice(0, 4);

  return (
    <PageShell>
      <main>
        <section className="hero-wash relative overflow-hidden border-b border-border/70">
          <div className="absolute inset-0 soft-grid opacity-45" aria-hidden="true" />
          <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-24">
            <div className="flex flex-col gap-8">
              <Badge variant="secondary" className="w-fit rounded-full px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.12em] text-primary">
                Public Codex skills library
              </Badge>
              <div className="flex flex-col gap-5">
                <h1 className="max-w-4xl font-heading text-5xl font-extrabold leading-[1.02] tracking-[-0.055em] sm:text-6xl lg:text-7xl">
                  Workflow notes, reusable skills, and agent operating patterns.
                </h1>
                <p className="max-w-2xl text-lg leading-8 text-muted-foreground sm:text-xl">
                  I&apos;m sharing the Codex skills and plugin patterns I use to run real implementation work: context layers, review boards, Shopify scaffolds, Jamstack deploys, docs systems, and practical agent workflows.
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <Link className={cn(buttonVariants({ size: "lg" }), "rounded-full px-5 shadow-sm")} href="/docs">
                  Browse the library
                  <ArrowRight data-icon="inline-end" aria-hidden="true" />
                </Link>
                <Link className={cn(buttonVariants({ variant: "outline", size: "lg" }), "rounded-full bg-card/80 px-5")} href={repoHref}>
                  <GitFork aria-hidden="true" />
                  Open GitHub
                </Link>
              </div>
            </div>

            <div className="glass-card rounded-3xl border border-border/80 p-5">
              <div className="mb-5 flex items-center justify-between gap-4">
                <div>
                  <p className="font-mono text-[0.68rem] font-semibold uppercase tracking-[0.16em] text-muted-foreground">Current focus</p>
                  <h2 className="mt-2 font-heading text-2xl font-extrabold tracking-[-0.04em]">Building in public</h2>
                </div>
                <Badge variant="outline" className="rounded-full">Maggie Lerman</Badge>
              </div>
              <div className="grid gap-3">
                {notes.map((item) => (
                  <div key={item.title} className="grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-border/80 bg-background/78 p-4 shadow-sm">
                    <span className="flex size-11 items-center justify-center rounded-2xl bg-secondary text-primary">
                      <item.icon aria-hidden="true" />
                    </span>
                    <div>
                      <h3 className="font-heading text-base font-bold tracking-[-0.02em]">{item.title}</h3>
                      <p className="mt-1 text-sm leading-6 text-muted-foreground">{item.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-10 sm:px-8 md:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.label} className="rounded-2xl border border-border/80 bg-card/82 p-5 shadow-sm">
              <div className="font-heading text-3xl font-extrabold tracking-[-0.04em] text-foreground">{stat.value}</div>
              <div className="mt-1 text-sm font-bold text-foreground">{stat.label}</div>
              <p className="mt-1 text-sm leading-6 text-muted-foreground">{stat.body}</p>
            </div>
          ))}
        </section>

        <section id="notes" className="mx-auto grid max-w-7xl gap-5 px-5 py-12 sm:px-8 lg:grid-cols-3">
          <FeaturedResource title="Why I package workflows" body="A good skill is a reusable working agreement. It carries instructions, source references, scripts, examples, and verification habits in one folder." />
          <FeaturedResource title="What this repo is for" body="The repo is a public reference point for people building serious Codex workflows, plus a backup of the local tools I actually use." />
          <FeaturedResource title="How support works" body="Use the repo, adapt what helps, open issues when something is unclear, and support the work if the patterns save you time." />
        </section>

        <section id="catalog" className="section-rule bg-card/35">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.78fr_1.22fr]">
            <SectionIntro
              eyebrow="Catalog"
              title="A browsable library of skills and plugin patterns."
              body="The catalog is generated from the repository metadata so the public docs stay aligned with the actual folders. Start with a guide, then inspect the source."
              icon={Library}
            />
            <div className="grid gap-5 md:grid-cols-2">
              {featuredSkills.map((item) => (
                <CatalogCard key={item.slug} item={item} compact />
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.9fr_1.1fr]">
          <SectionIntro
            eyebrow="Plugin bundles"
            title="Larger surfaces stay packaged."
            body="Some workflows need plugin metadata, bundled skills, MCP config, scripts, or assets. Those live as plugin backups rather than one-off snippets."
            icon={PackageOpen}
          />
          <div className="grid gap-5 md:grid-cols-2">
            {featuredPlugins.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
        </section>

        <section id="support" className="section-rule bg-card/35">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[1fr_1fr] lg:items-center">
            <div className="flex flex-col gap-5">
              <div className="flex size-12 items-center justify-center rounded-2xl bg-accent text-accent-foreground">
                <Coffee aria-hidden="true" />
              </div>
              <h2 className="font-heading text-4xl font-extrabold leading-tight tracking-[-0.05em] sm:text-5xl">Use it freely. Support it if it helps.</h2>
              <p className="text-lg leading-8 text-muted-foreground">
                This is a public repo and personal knowledge base for useful Codex workflows. The support model is simple: read, adapt, contribute, and back continued maintenance when the work saves real time.
              </p>
              <div className="flex flex-col gap-3 sm:flex-row">
                <Link className={cn(buttonVariants({ size: "lg" }), "rounded-full px-5 shadow-sm")} href={supportHref}>
                  Support the work
                  <HeartHandshake data-icon="inline-end" aria-hidden="true" />
                </Link>
                <Link className={cn(buttonVariants({ variant: "outline", size: "lg" }), "rounded-full bg-card/80 px-5")} href={repoHref}>
                  <GitFork aria-hidden="true" />
                  Star or fork
                </Link>
              </div>
            </div>
            <Card className="rounded-3xl border-border/80 bg-card/86 p-1 shadow-sm">
              <CardContent className="grid gap-4 p-5">
                {[
                  ["Read", "Browse the catalog and implementation notes before copying anything."],
                  ["Adapt", "Use the folders that match your stack, then adjust them to your repo’s conventions."],
                  ["Contribute", "Open issues for unclear docs, missing examples, or workflow gaps."],
                  ["Support", "Back maintenance when the repo saves real time."],
                ].map(([label, body]) => (
                  <div key={label} className="grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-border/80 bg-background/70 p-4">
                    <span className="flex size-10 items-center justify-center rounded-2xl bg-secondary text-sm font-bold text-primary">{label.slice(0, 1)}</span>
                    <p className="text-sm leading-6 text-muted-foreground"><strong className="text-foreground">{label}.</strong> {body}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </section>
      </main>
    </PageShell>
  );
}

function SectionIntro({ eyebrow, title, body, icon: Icon }: { eyebrow: string; title: string; body: string; icon: LucideIcon }) {
  return (
    <div className="flex max-w-3xl flex-col gap-4">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.13em] text-primary">
        <Icon aria-hidden="true" className="size-4" />
        {eyebrow}
      </div>
      <h2 className="font-heading text-4xl font-extrabold leading-tight tracking-[-0.05em] sm:text-5xl">{title}</h2>
      <p className="text-lg leading-8 text-muted-foreground">{body}</p>
      <div className="flex flex-wrap gap-3 text-sm font-semibold text-muted-foreground">
        <span className="inline-flex items-center gap-2"><BookOpen aria-hidden="true" className="size-4 text-primary" /> Learn</span>
        <span className="inline-flex items-center gap-2"><Boxes aria-hidden="true" className="size-4 text-primary" /> Install</span>
        <span className="inline-flex items-center gap-2"><Sparkles aria-hidden="true" className="size-4 text-primary" /> Remix</span>
      </div>
    </div>
  );
}
