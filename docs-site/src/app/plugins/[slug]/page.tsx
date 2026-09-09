import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { DetailPage } from "@/components/site/detail-page";
import { getCatalogItem, pluginItems } from "@/lib/catalog";

export function generateStaticParams() {
  return pluginItems.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const item = getCatalogItem("plugin", slug);
  if (!item) return {};
  return {
    title: `${item.title} | Codex Skills`,
    description: item.summary,
  };
}

export default async function PluginPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const item = getCatalogItem("plugin", slug);
  if (!item) notFound();
  return <DetailPage item={item} />;
}
