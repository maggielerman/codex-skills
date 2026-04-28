import Link from "next/link";
import { ArrowUpRight, BookOpen, PackageCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/docs", label: "Docs" },
  { href: "/#skills", label: "Skills" },
  { href: "/#plugins", label: "Plugins" },
  { href: "/#support", label: "Support" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/70 bg-background/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-4 sm:px-8">
        <Link href="/" className="flex items-center gap-3" aria-label="Codex Skills Packs home">
          <span className="flex size-10 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-[0_18px_55px_var(--shadow-primary)]">
            <PackageCheck aria-hidden="true" />
          </span>
          <span className="flex flex-col leading-none">
            <span className="font-heading text-lg font-semibold tracking-tight">Codex Skills Packs</span>
            <span className="text-xs font-medium uppercase tracking-[0.22em] text-muted-foreground">Installable agent workflows</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-1 rounded-full border border-border/70 bg-card/70 p-1 md:flex" aria-label="Primary navigation">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="rounded-full px-4 py-2 text-sm font-medium text-muted-foreground transition hover:bg-secondary hover:text-foreground">
              {item.label}
            </Link>
          ))}
        </nav>
        <Link className={cn(buttonVariants({ size: "lg" }), "hidden rounded-full md:inline-flex")} href="/docs">
          View pack docs
          <ArrowUpRight data-icon="inline-end" aria-hidden="true" />
        </Link>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-border/70 bg-card/60">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-10 sm:px-8 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-col gap-2">
          <Badge variant="secondary" className="w-fit">Customer docs preview</Badge>
          <p className="max-w-2xl text-sm text-muted-foreground">
            These pages are for people implementing purchased skills packs in their own repositories and workflows. Internal repo maintenance docs stay separate.
          </p>
        </div>
        <Link className="inline-flex items-center gap-2 text-sm font-semibold text-foreground" href="/docs">
          Open getting started
          <BookOpen aria-hidden="true" />
        </Link>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <SiteHeader />
      {children}
      <SiteFooter />
    </div>
  );
}
