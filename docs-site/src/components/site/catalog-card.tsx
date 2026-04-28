import Link from "next/link";
import { ArrowUpRight, Boxes, Hammer, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { CatalogItem } from "@/lib/catalog-types";

const iconMap = {
  skill: Hammer,
  plugin: Boxes,
};

export function CatalogCard({ item }: { item: CatalogItem }) {
  const Icon = iconMap[item.kind];
  const href = item.kind === "skill" ? `/skills/${item.slug}` : `/plugins/${item.slug}`;

  return (
    <Card className="group relative min-h-full border-border/80 bg-card/85 transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_90px_var(--shadow-soft)]">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <span className="flex size-11 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground">
            <Icon aria-hidden="true" />
          </span>
          <Badge variant={item.status === "deprecated" ? "outline" : "secondary"}>{item.status}</Badge>
        </div>
        <CardTitle className="text-xl tracking-tight">{item.title}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-5">
        <p className="text-sm leading-6 text-muted-foreground">{item.summary}</p>
        <div className="flex flex-wrap gap-2">
          {item.resources.slice(0, 3).map((resource) => (
            <Badge key={resource} variant="outline" className="rounded-full">{resource}</Badge>
          ))}
        </div>
        <Link href={href} className="mt-auto inline-flex items-center gap-2 text-sm font-semibold text-primary">
          Implementation guide
          <ArrowUpRight aria-hidden="true" className="transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </Link>
      </CardContent>
      <div className="pointer-events-none absolute inset-x-6 bottom-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent opacity-0 transition group-hover:opacity-100" />
    </Card>
  );
}

export function FeaturedResource({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-3xl border border-border/70 bg-card/80 p-6 shadow-[0_18px_70px_var(--shadow-soft)]">
      <div className="mb-5 flex size-11 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
        <Sparkles aria-hidden="true" />
      </div>
      <h3 className="font-heading text-2xl font-semibold tracking-tight">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">{body}</p>
    </div>
  );
}
