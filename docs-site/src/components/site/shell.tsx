"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  Home,
  FileText,
  Puzzle,
  ArrowUpRight,
  GitFork,
  Link as LinkIcon,
} from "lucide-react";

const navigation = [
  { href: "/", label: "Overview", icon: Home },
  { href: "/docs", label: "Browse library", icon: BookOpen },
  { href: "/getting-started", label: "Getting started", icon: FileText },
];
const plugins = [
  { href: "/plugins/context-layer", label: "Context Layer" },
  { href: "/plugins/rps-etsy-ops", label: "RPS Etsy Ops" },
  { href: "/plugins/motion-design-director", label: "Motion Design" },
];
export function PageShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname().replace(/\/$/, "") || "/";
  return (
    <div className="workspace">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <aside className="sidebar">
        <Link href="/" className="brand" aria-label="Codex Skills home">
          <span className="brand-mark" aria-hidden="true">
            <i />
          </span>
          <strong>Codex Skills</strong>
        </Link>
        <nav className="primary-nav" aria-label="Primary navigation">
          {navigation.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              aria-current={pathname === href ? "page" : undefined}
            >
              <Icon size={19} aria-hidden="true" />
              {label}
            </Link>
          ))}
        </nav>
        <nav className="plugin-nav" aria-label="Featured plugins">
          <p>Plugins</p>
          {plugins.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              aria-current={pathname === href ? "page" : undefined}
            >
              <Puzzle size={19} aria-hidden="true" />
              {label}
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <a href="https://github.com/maggielerman/codex-skills">
            <GitFork size={17} aria-hidden="true" />
            Open on GitHub <ArrowUpRight size={14} aria-hidden="true" />
          </a>
          <a href="https://maggielerman.com">
            <LinkIcon size={17} aria-hidden="true" />
            maggielerman.com <ArrowUpRight size={14} aria-hidden="true" />
          </a>
        </div>
      </aside>
      <div className="content-shell">
        <header className="topbar">
          <span>
            Library <span className="slash">/</span>{" "}
            {pathname === "/"
              ? "Overview"
              : pathname === "/docs"
                ? "Catalog"
                : pathname === "/getting-started"
                  ? "Getting started"
                  : pathname.startsWith("/plugins")
                    ? "Plugins"
                    : "Skills"}
          </span>
          <a href="https://github.com/maggielerman/codex-skills">
            View source <ArrowUpRight size={16} aria-hidden="true" />
          </a>
        </header>
        {children}
        <footer className="site-footer">
          <span>Built and maintained by Maggie Lerman.</span>
          <a href="https://github.com/maggielerman/codex-skills/blob/main/README.md#license">
            License & attribution <ArrowUpRight size={13} aria-hidden="true" />
          </a>
        </footer>
      </div>
    </div>
  );
}
