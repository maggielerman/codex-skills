export type CatalogKind = "skill" | "plugin";

export type CatalogItem = {
  slug: string;
  kind: CatalogKind;
  title: string;
  folder: string;
  status: string;
  summary: string;
  description: string;
  category: string;
  path: string | null;
  resources: readonly string[];
  useCases: readonly string[];
  gettingStarted: readonly string[];
  troubleshooting: readonly string[];
};
