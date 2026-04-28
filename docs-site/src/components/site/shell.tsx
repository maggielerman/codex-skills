import Link from "next/link";
import { ArrowUpRight, BookOpen, PackageCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/docs", label: "Docs" },
  { href: "/#catalog", label: "Skills" },
  { href: "/#plugins", label: "Plugins" },
  { href: "/docs#support", label: "Support" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/70 bg-background/82 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-5 py-4 sm:px-8">
        <Link href="/" className="flex min-w-0 items-center gap-3" aria-label="Codex Skills Packs home">
          <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
            <PackageCheck className="size-5" aria-hidden="true" />
          </span>
          <span className="flex min-w-0 flex-col leading-none">
            <span className="truncate font-heading text-base font-extrabold tracking-[-0.03em] sm:text-lg">Codex Skills Packs</span>
            <span className="mt-1 font-mono text-[0.58rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">Maggie Lerman</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-1 rounded-full border border-border/80 bg-card/82 p-1 shadow-sm md:flex" aria-label="Primary navigation">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="rounded-full px-4 py-2 text-sm font-semibold text-muted-foreground transition hover:bg-secondary hover:text-foreground">
              {item.label}
            </Link>
          ))}
        </nav>
        <Link className={cn(buttonVariants({ size: "lg" }), "hidden rounded-full px-4 shadow-sm md:inline-flex")} href="/docs">
          Explore the docs
          <ArrowUpRight data-icon="inline-end" aria-hidden="true" />
        </Link>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-border/70 bg-card/70">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-10 sm:px-8 lg:grid-cols-[1fr_auto] lg:items-end">
        <div className="flex flex-col gap-3">
          <Badge variant="secondary" className="w-fit rounded-full">Customer-facing docs</Badge>
          <p className="max-w-3xl text-sm leading-6 text-muted-foreground">
            Guides for customers evaluating, installing, and operating Maggie Lerman&apos;s Codex skills and custom plugin bundles in their own repositories.
          </p>
        </div>
        <Link className="inline-flex items-center gap-2 text-sm font-semibold text-primary" href="/docs">
          Start with the docs
          <BookOpen aria-hidden="true" />
        </Link>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen text-foreground">
      <SiteHeader />
      {children}
      <SiteFooter />
    </div>
  );
}
