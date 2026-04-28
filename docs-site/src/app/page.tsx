import Link from "next/link";
import { ArrowRight, CheckCircle2, FileText, GitBranch, ShieldCheck, WandSparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { CatalogCard, FeaturedResource } from "@/components/site/catalog-card";
import { PageShell } from "@/components/site/shell";
import { catalogStats, pluginItems, skillItems } from "@/lib/catalog";
import { cn } from "@/lib/utils";

const heroProof = [
  "Portable skill folders",
  "Customer setup docs",
  "Workflow-level troubleshooting",
];

const implementationSteps = [
  {
    title: "Install the pack",
    body: "Copy the delivered skill or plugin folders into the Codex environment your team uses, keeping bundled scripts and references intact.",
  },
  {
    title: "Point at a real repo",
    body: "Open the customer repository, read its local agent rules, and invoke the skill against a concrete business outcome.",
  },
  {
    title: "Adapt with evidence",
    body: "Use the generated docs, scripts, checkpoints, and review artifacts as the operating layer for the customer workflow.",
  },
];

export default function Home() {
  const featuredSkills = skillItems.slice(0, 6);

  return (
    <PageShell>
      <main>
        <section className="grain-field relative overflow-hidden border-b border-border/70">
          <div className="absolute inset-0 ruled-paper opacity-40" aria-hidden="true" />
          <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-28">
            <div className="flex flex-col gap-8">
              <div className="flex flex-wrap gap-2">
                {heroProof.map((item) => (
                  <Badge key={item} variant="secondary" className="rounded-full">{item}</Badge>
                ))}
              </div>
              <div className="flex flex-col gap-6">
                <h1 className="max-w-4xl font-heading text-5xl font-semibold leading-[0.95] tracking-[-0.055em] sm:text-7xl lg:text-8xl">
                  Agent workflows you can sell, install, and support.
                </h1>
                <p className="max-w-2xl text-lg leading-8 text-muted-foreground sm:text-xl">
                  A customer-facing home for the Codex skills packs: marketing, implementation docs, per-skill guides, plugin setup, and troubleshooting that helps buyers make the workflows work inside their own repositories.
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <Link className={cn(buttonVariants({ size: "lg" }), "rounded-full")} href="/docs">
                  Start implementing
                  <ArrowRight data-icon="inline-end" aria-hidden="true" />
                </Link>
                <Link className={cn(buttonVariants({ variant: "outline", size: "lg" }), "rounded-full bg-card/70")} href="#skills">
                  Browse the catalog
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="absolute -inset-6 rounded-[3rem] bg-primary/10 blur-3xl" aria-hidden="true" />
              <Card className="relative overflow-hidden border-border/80 bg-card/90 shadow-[0_35px_120px_var(--shadow-soft)]">
                <CardHeader className="border-b border-border/70 bg-secondary/45">
                  <div className="flex items-center justify-between gap-4">
                    <CardTitle className="font-heading text-3xl tracking-tight">Pack console</CardTitle>
                    <Badge>{catalogStats.skills} skills</Badge>
                  </div>
                </CardHeader>
                <CardContent className="flex flex-col gap-5 p-5">
                  {implementationSteps.map((step, index) => (
                    <div key={step.title} className="grid grid-cols-[auto_1fr] gap-4 rounded-3xl border border-border/70 bg-background/60 p-4">
                      <span className="flex size-10 items-center justify-center rounded-2xl bg-primary text-sm font-bold text-primary-foreground">{index + 1}</span>
                      <div className="flex flex-col gap-1">
                        <h2 className="font-heading text-xl font-semibold tracking-tight">{step.title}</h2>
                        <p className="text-sm leading-6 text-muted-foreground">{step.body}</p>
                      </div>
                    </div>
                  ))}
                  <Separator />
                  <div className="grid gap-3 sm:grid-cols-3">
                    <Metric label="Skills" value={catalogStats.skills.toString()} />
                    <Metric label="Plugins" value={catalogStats.plugins.toString()} />
                    <Metric label="Audience" value="buyers" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-16 sm:px-8 lg:grid-cols-3" id="support">
          <FeaturedResource title="Getting started that respects real repos" body="The docs are written for customers installing packs into existing repositories with their own rules, risks, branches, and human approval loops." />
          <FeaturedResource title="Troubleshooting without archaeology" body="Each guide explains common failure modes: missing triggers, misplaced bundled scripts, vague prompts, and docs that need a customer-facing audience reset." />
          <FeaturedResource title="Catalog pages from source metadata" body="The public docs are generated from the suite manifest and plugin.json files so customer pages stay aligned with what is actually shipped." />
        </section>

        <section className="border-y border-border/70 bg-card/45" id="skills">
          <div className="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-16 sm:px-8">
            <SectionIntro icon={<WandSparkles aria-hidden="true" />} title="Skill guides" body="Each skill page turns internal trigger metadata into buyer-facing implementation guidance: what the workflow is for, how to start, and what to check when it misfires." />
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {featuredSkills.map((item) => (
                <CatalogCard key={item.slug} item={item} />
              ))}
            </div>
            <Link href="/docs#all-skills" className="inline-flex items-center gap-2 self-start text-sm font-semibold text-primary">
              See all skill docs
              <ArrowRight aria-hidden="true" />
            </Link>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.85fr_1.15fr]" id="plugins">
          <SectionIntro icon={<GitBranch aria-hidden="true" />} title="Plugin support" body="Plugin pages focus on installation, expected capabilities, and keeping plugin folders self-contained when customers move them into their own Codex setup." />
          <div className="grid gap-5 md:grid-cols-2">
            {pluginItems.map((item) => (
              <CatalogCard key={item.slug} item={item} />
            ))}
          </div>
        </section>
      </main>
    </PageShell>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-border/70 bg-card p-4">
      <div className="font-heading text-3xl font-semibold tracking-tight">{value}</div>
      <div className="mt-1 text-xs font-semibold uppercase tracking-[0.18em] text-muted-foreground">{label}</div>
    </div>
  );
}

function SectionIntro({ icon, title, body }: { icon: React.ReactNode; title: string; body: string }) {
  return (
    <div className="flex max-w-3xl flex-col gap-4">
      <div className="flex size-12 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground">{icon}</div>
      <h2 className="font-heading text-4xl font-semibold tracking-[-0.035em] sm:text-5xl">{title}</h2>
      <p className="text-lg leading-8 text-muted-foreground">{body}</p>
      <div className="flex gap-3 text-sm font-medium text-muted-foreground">
        <span className="inline-flex items-center gap-2"><CheckCircle2 aria-hidden="true" /> Buyer-facing</span>
        <span className="inline-flex items-center gap-2"><FileText aria-hidden="true" /> Generated from catalog</span>
        <span className="inline-flex items-center gap-2"><ShieldCheck aria-hidden="true" /> Support-ready</span>
      </div>
    </div>
  );
}
