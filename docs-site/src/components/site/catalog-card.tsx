import Link from "next/link";
import { ArrowUpRight, Boxes, FolderKanban, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { CatalogItem } from "@/lib/catalog-types";

const iconMap = {
  skill: FolderKanban,
  plugin: Boxes,
};

export function CatalogCard({ item, compact = false }: { item: CatalogItem; compact?: boolean }) {
  const Icon = iconMap[item.kind];
  const href = item.kind === "skill" ? `/skills/${item.slug}` : `/plugins/${item.slug}`;

  return (
    <Card className="group min-h-full rounded-2xl border border-border/80 bg-card/86 p-1 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:border-primary/25 hover:shadow-lg">
      <CardHeader className={compact ? "gap-3 p-4" : "gap-4 p-5"}>
        <div className="flex items-start justify-between gap-4">
          <span className="flex size-11 items-center justify-center rounded-2xl bg-secondary text-primary">
            <Icon aria-hidden="true" />
          </span>
          <Badge variant={item.status === "deprecated" ? "outline" : "secondary"} className="rounded-full capitalize">{item.status}</Badge>
        </div>
        <CardTitle className="text-xl font-bold leading-tight tracking-[-0.025em]">{item.title}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-5 p-5 pt-0">
        <p className="text-sm leading-6 text-muted-foreground">{item.summary}</p>
        {!compact ? (
          <div className="flex flex-wrap gap-2">
            {item.resources.slice(0, 3).map((resource) => (
              <Badge key={resource} variant="outline" className="rounded-full text-[0.72rem] capitalize">{resource}</Badge>
            ))}
          </div>
        ) : null}
        <Link href={href} className="mt-auto inline-flex items-center gap-2 text-sm font-semibold text-primary">
          Read guide
          <ArrowUpRight aria-hidden="true" className="size-4 transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </Link>
      </CardContent>
    </Card>
  );
}

export function FeaturedResource({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-border/80 bg-card/82 p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg">
      <div className="mb-5 flex size-11 items-center justify-center rounded-2xl bg-accent text-accent-foreground">
        <Sparkles aria-hidden="true" />
      </div>
      <h3 className="font-heading text-2xl font-bold tracking-[-0.035em]">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">{body}</p>
    </div>
  );
}
