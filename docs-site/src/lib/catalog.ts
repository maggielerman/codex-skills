import { catalog } from "./catalog.generated";
import type { CatalogItem } from "./catalog-types";

const catalogItems = catalog.items as readonly CatalogItem[];

export const allCatalogItems = [...catalogItems].sort((a, b) =>
  a.title.localeCompare(b.title),
);

export const skillItems = allCatalogItems.filter(
  (item) => item.kind === "skill",
);

export const pluginItems = allCatalogItems.filter(
  (item) => item.kind === "plugin",
);

export const catalogStats = {
  skills: catalog.skillCount,
  plugins: catalog.pluginCount,
  generatedBy: catalog.generatedBy,
};

export function getCatalogItem(kind: CatalogItem["kind"], slug: string) {
  return allCatalogItems.find((item) => item.kind === kind && item.slug === slug);
}

export function getCategories() {
  return Array.from(new Set(allCatalogItems.map((item) => item.category))).sort();
}
