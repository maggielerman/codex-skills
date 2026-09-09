import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { DetailPage } from "@/components/site/detail-page";
import { getCatalogItem, skillItems } from "@/lib/catalog";

export function generateStaticParams() {
  return skillItems.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const item = getCatalogItem("skill", slug);
  if (!item) return {};
  return {
    title: `${item.title} | Codex Skills`,
    description: item.summary,
  };
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const item = getCatalogItem("skill", slug);
  if (!item) notFound();
  return <DetailPage item={item} />;
}
