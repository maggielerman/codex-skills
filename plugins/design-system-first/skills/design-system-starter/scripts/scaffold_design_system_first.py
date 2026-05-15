#!/usr/bin/env python3
"""Scaffold a design-system-first Next.js starter project."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import textwrap
from pathlib import Path


STARTER_SCRIPT = Path(__file__).resolve()
STARTER_SKILL_DIR = STARTER_SCRIPT.parents[1]
PLUGIN_DIR = STARTER_SCRIPT.parents[3]

DOCS_SKILL_CANDIDATES = [
    Path.home() / ".codex" / "skills" / "docs-system-scaffold",
    Path((Path.home() / ".codex").expanduser()) / "skills" / "docs-system-scaffold",
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def relative_files(root: Path) -> list[str]:
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


class PackageManager:
    def __init__(self, name: str) -> None:
        self.name = name
        self.create_next_flag = {
            "npm": "--use-npm",
            "pnpm": "--use-pnpm",
            "yarn": "--use-yarn",
            "bun": "--use-bun",
        }[name]
        self.exec_prefix = {
            "npm": ["npx", "--yes"],
            "pnpm": ["pnpm", "dlx"],
            "yarn": ["yarn", "dlx"],
            "bun": ["bunx", "--bun"],
        }[name]
        self.dev_install = {
            "npm": ["npm", "install", "-D"],
            "pnpm": ["pnpm", "add", "-D"],
            "yarn": ["yarn", "add", "-D"],
            "bun": ["bun", "add", "-d"],
        }[name]

    def run_script(self, script_name: str) -> str:
        return {
            "npm": f"npm run {script_name}",
            "pnpm": f"pnpm {script_name}",
            "yarn": f"yarn {script_name}",
            "bun": f"bun run {script_name}",
        }[self.name]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, help="Destination directory for the new project.")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["marketing-only", "app-shell"],
        help="Starter mode to scaffold.",
    )
    parser.add_argument(
        "--addons",
        default="",
        help="Comma-separated add-ons. Supported: docs,testing",
    )
    parser.add_argument(
        "--package-manager",
        choices=["npm", "pnpm", "yarn", "bun"],
        default="npm",
        help="Package manager to use for scaffolding and installs.",
    )
    parser.add_argument(
        "--name",
        help="Optional display name for the starter. Defaults to the folder name.",
    )
    return parser.parse_args()


def parse_addons(raw_addons: str) -> list[str]:
    if not raw_addons.strip():
        return []

    addons = []
    for value in raw_addons.split(","):
        addon = value.strip()
        if not addon:
            continue
        if addon not in {"docs", "testing"}:
            raise SystemExit(f"Unsupported addon: {addon}")
        addons.append(addon)

    return sorted(set(addons))


def ensure_target_is_empty(target_dir: Path) -> None:
    if target_dir.exists():
        if any(target_dir.iterdir()):
            raise SystemExit(f"Target directory is not empty: {target_dir}")
    else:
        target_dir.parent.mkdir(parents=True, exist_ok=True)


def scaffold_next_app(target_dir: Path, project_name: str, package_manager: PackageManager) -> None:
    run(
        [
            "npx",
            "--yes",
            "create-next-app@latest",
            str(target_dir),
            "--ts",
            "--tailwind",
            "--eslint",
            "--app",
            "--src-dir",
            "--import-alias",
            "@/*",
            "--yes",
            "--disable-git",
            package_manager.create_next_flag,
        ]
    )


def shadcn_components_for_mode(mode: str) -> list[str]:
    base = ["button", "card", "badge", "separator"]
    if mode == "app-shell":
        return base + ["input"]
    return base


def initialize_shadcn(target_dir: Path, mode: str, package_manager: PackageManager) -> None:
    run(package_manager.exec_prefix + ["shadcn@latest", "init", "-d", "-y", "-c", str(target_dir)])
    run(
        package_manager.exec_prefix
        + ["shadcn@latest", "add", "-y", "-c", str(target_dir), *shadcn_components_for_mode(mode)]
    )


def site_description(mode: str) -> str:
    if mode == "marketing-only":
        return "A marketing starter shaped around bold hierarchy, reusable tokens, and a real design system from the first commit."
    return "An app-shell starter with shared tokens, strong surface primitives, and a clear workspace hierarchy from day one."


def render_layout(project_name: str, description: str) -> str:
    return textwrap.dedent(
        f"""
        import type {{ Metadata }} from "next";
        import "./globals.css";
        import {{ siteConfig }} from "@/lib/site-config";

        export const metadata: Metadata = {{
          title: siteConfig.name,
          description: siteConfig.description,
        }};

        export default function RootLayout({{
          children,
        }}: Readonly<{{ children: React.ReactNode }}>) {{
          return (
            <html lang="en">
              <body>
                {{children}}
              </body>
            </html>
          );
        }}
        """
    )


def render_globals_css() -> str:
    return textwrap.dedent(
        """
        @import "tailwindcss";

        :root {
          --background: #09111e;
          --foreground: #f6f3eb;
          --surface: rgba(9, 17, 30, 0.72);
          --surface-strong: rgba(11, 21, 38, 0.9);
          --muted: rgba(231, 226, 215, 0.72);
          --line: rgba(255, 255, 255, 0.12);
          --accent: #8df2d3;
          --accent-strong: #2fc3a7;
          --accent-warm: #ffc977;
          --shadow: 0 28px 70px rgba(3, 8, 20, 0.38);
          --ds-font-sans: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
          --ds-font-mono: "IBM Plex Mono", "SFMono-Regular", "SF Mono", "Cascadia Code", monospace;
        }

        @theme inline {
          --color-background: var(--background);
          --color-foreground: var(--foreground);
          --font-sans: var(--ds-font-sans);
          --font-mono: var(--ds-font-mono);
        }

        * {
          box-sizing: border-box;
        }

        html {
          scroll-behavior: smooth;
        }

        body {
          min-height: 100vh;
          background:
            radial-gradient(circle at top left, rgba(47, 195, 167, 0.18), transparent 34%),
            radial-gradient(circle at 85% 15%, rgba(255, 201, 119, 0.18), transparent 28%),
            linear-gradient(180deg, #09111e 0%, #0d1526 55%, #09111e 100%);
          color: var(--foreground);
          font-family: var(--ds-font-sans);
          text-rendering: optimizeLegibility;
        }

        a {
          color: inherit;
          text-decoration: none;
        }

        ::selection {
          background: rgba(141, 242, 211, 0.32);
        }

        .ds-shell {
          margin: 0 auto;
          max-width: 1160px;
          padding: 1.5rem;
        }

        .ds-panel {
          border: 1px solid var(--line);
          background: linear-gradient(180deg, rgba(11, 21, 38, 0.92), rgba(11, 21, 38, 0.72));
          box-shadow: var(--shadow);
          backdrop-filter: blur(20px);
        }

        .ds-kicker {
          color: var(--accent);
          font-family: var(--ds-font-mono);
          font-size: 0.72rem;
          letter-spacing: 0.22em;
          text-transform: uppercase;
        }

        .ds-display {
          font-size: clamp(3.2rem, 9vw, 6.4rem);
          line-height: 0.94;
          letter-spacing: -0.06em;
        }

        .ds-muted {
          color: var(--muted);
        }

        .ds-accent-bar {
          height: 1px;
          background: linear-gradient(90deg, rgba(141, 242, 211, 0.88), transparent);
        }

        .ds-grid {
          display: grid;
          gap: 1rem;
        }

        @media (max-width: 768px) {
          .ds-shell {
            padding: 1rem;
          }
        }
        """
    )


def render_site_config(project_name: str, mode: str, addons: list[str]) -> str:
    description = site_description(mode)
    return textwrap.dedent(
        f"""
        export type StarterMode = "marketing-only" | "app-shell";

        type SiteConfig = {{
          name: string;
          mode: StarterMode;
          addons: readonly string[];
          description: string;
        }};

        export const siteConfig: SiteConfig = {{
          name: {json.dumps(project_name)},
          mode: {json.dumps(mode)} as StarterMode,
          addons: {json.dumps(addons)},
          description: {json.dumps(description)},
        }} as const;
        """
    )


def render_surface_card() -> str:
    return textwrap.dedent(
        """
        import * as React from "react";
        import { Card } from "@/components/ui/card";
        import { cn } from "@/lib/utils";

        export function SurfaceCard({
          className,
          ...props
        }: React.ComponentProps<typeof Card>) {
          return <Card className={cn("ds-panel rounded-[28px]", className)} {...props} />;
        }
        """
    )


def render_tsx(template: str, **replacements: str) -> str:
    rendered = textwrap.dedent(template).replace("{{", "{").replace("}}", "}")
    for key, value in replacements.items():
        rendered = rendered.replace(f"__{key}__", value)
    return rendered


def render_site_header() -> str:
    return textwrap.dedent(
        """
        import { Badge } from "@/components/ui/badge";
        import { Button } from "@/components/ui/button";
        import { siteConfig } from "@/lib/site-config";

        const navItems =
          siteConfig.mode === "marketing-only"
            ? ["System", "Proof", "Contact"]
            : ["Overview", "Queue", "Library"];

        export function SiteHeader() {
          return (
            <header className="ds-panel sticky top-4 z-20 mt-4 flex items-center justify-between rounded-full px-4 py-3 md:px-6">
              <div className="flex items-center gap-3">
                <span className="inline-flex size-10 items-center justify-center rounded-full border border-white/10 bg-white/8 font-mono text-xs uppercase tracking-[0.26em] text-[var(--accent)]">
                  DS
                </span>
                <div className="space-y-0.5">
                  <div className="text-sm font-medium tracking-[-0.03em] text-white">
                    {siteConfig.name}
                  </div>
                  <div className="text-xs text-[var(--muted)]">
                    {siteConfig.mode === "marketing-only" ? "Marketing starter" : "App shell starter"}
                  </div>
                </div>
              </div>
              <nav className="hidden items-center gap-2 md:flex">
                {navItems.map((item) => (
                  <Button key={item} type="button" variant="ghost" className="rounded-full text-xs text-[var(--muted)] hover:text-white">
                    {item}
                  </Button>
                ))}
              </nav>
              <Badge variant="outline" className="rounded-full border-[var(--line)] bg-white/5 px-3 py-1 text-[var(--accent)]">
                design-system-first
              </Badge>
            </header>
          );
        }
        """
    )


def render_marketing_page(project_name: str) -> str:
    return (
        textwrap.dedent(
            """
        import {{ Badge }} from "@/components/ui/badge";
        import {{ Button }} from "@/components/ui/button";
        import {{ SiteHeader }} from "@/components/site-header";
        import {{ SurfaceCard }} from "@/components/surface-card";

        const pillars = [
          {{
            title: "Tokenized from day one",
            body: "Shared color, type, spacing, and surface decisions live in one place so the starter feels like a system, not a pile of components.",
          }},
          {{
            title: "Visual thesis, not filler UI",
            body: "The first screen is designed to carry a point of view with expressive type, deliberate whitespace, and a real visual anchor.",
          }},
          {{
            title: "Ready for refinement",
            body: "The starter gives you a strong shell, then leaves room for `$design-system-refine`, `$shadcn`, and deeper product-specific art direction.",
          }},
        ];

        export default function Home() {{
          return (
            <main className="pb-16">
              <div className="ds-shell">
                <SiteHeader />
                <section className="grid gap-10 pb-14 pt-16 md:grid-cols-[1.2fr_0.8fr] md:items-end">
                  <div className="space-y-7">
                    <Badge variant="outline" className="rounded-full border-[var(--line)] bg-white/6 px-4 py-1 text-[var(--accent)]">
                      marketing-only starter
                    </Badge>
                    <div className="space-y-5">
                      <p className="ds-kicker">Design System First</p>
                      <h1 className="ds-display max-w-4xl font-medium text-white">
                        __PROJECT_NAME__ starts with atmosphere, hierarchy, and a real foundation.
                      </h1>
                      <p className="max-w-2xl text-lg leading-8 ds-muted">
                        This starter ships with shared tokens, shadcn foundations, and a polished landing-page shell so the first commit already feels intentional.
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-3">
                      <Button type="button" className="rounded-full bg-[var(--accent)] px-6 text-black hover:bg-[var(--accent)]/90">
                        Launch the first story
                      </Button>
                      <Button type="button" variant="outline" className="rounded-full border-[var(--line)] bg-white/4 px-6 text-white">
                        Review the system
                      </Button>
                    </div>
                  </div>
                  <SurfaceCard className="overflow-hidden p-6">
                    <div className="ds-kicker mb-6">Starter Surface</div>
                    <div className="space-y-6">
                      <div>
                        <div className="text-sm uppercase tracking-[0.26em] text-[var(--muted)]">Signature move</div>
                        <div className="mt-3 text-3xl font-medium tracking-[-0.05em] text-white">
                          Poster-led first viewport
                        </div>
                      </div>
                      <div className="ds-grid md:grid-cols-2">
                        <div className="rounded-[24px] border border-white/10 bg-[linear-gradient(140deg,rgba(141,242,211,0.18),rgba(255,255,255,0.04))] p-5">
                          <div className="text-xs uppercase tracking-[0.26em] text-[var(--muted)]">Typography</div>
                          <div className="mt-3 text-2xl font-medium tracking-[-0.05em] text-white">
                            Space Grotesk
                          </div>
                        </div>
                        <div className="rounded-[24px] border border-white/10 bg-[linear-gradient(140deg,rgba(255,201,119,0.18),rgba(255,255,255,0.04))] p-5">
                          <div className="text-xs uppercase tracking-[0.26em] text-[var(--muted)]">Accent</div>
                          <div className="mt-3 text-2xl font-medium tracking-[-0.05em] text-white">
                            Seafoam + Warm Sand
                          </div>
                        </div>
                      </div>
                      <div className="rounded-[28px] border border-white/10 bg-black/20 p-6">
                        <div className="text-sm text-[var(--muted)]">
                          Use this surface as the canonical example of how the system treats contrast, spacing, curvature, and content density.
                        </div>
                      </div>
                    </div>
                  </SurfaceCard>
                </section>

                <div className="ds-accent-bar mb-8" />

                <section className="grid gap-4 md:grid-cols-3">
                  {{pillars.map((pillar) => (
                    <SurfaceCard key={pillar.title} className="p-6">
                      <div className="space-y-3">
                        <div className="text-lg font-medium tracking-[-0.03em] text-white">{pillar.title}</div>
                        <p className="text-sm leading-7 ds-muted">{pillar.body}</p>
                      </div>
                    </SurfaceCard>
                  ))}}
                </section>
              </div>
            </main>
          );
        }}
        """
        )
        .replace("{{", "{")
        .replace("}}", "}")
        .replace("__PROJECT_NAME__", project_name)
    )


def render_app_page(project_name: str) -> str:
    return render_tsx(
        """
        import { AppShellFrame } from "@/components/app-shell-frame";
        import { SurfaceCard } from "@/components/surface-card";
        import { dashboardFocus, launchMetrics, signalFeed } from "@/lib/app-shell-data";

        export default function Home() {
          const spotlight = (
            <section className="grid gap-4 md:grid-cols-4">
              {launchMetrics.map((metric) => (
                <SurfaceCard key={metric.label} className="p-5">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">{metric.label}</div>
                  <div className="mt-4 text-4xl font-medium tracking-[-0.06em] text-white">{metric.value}</div>
                  <div className="mt-2 text-sm ds-muted">{metric.note}</div>
                </SurfaceCard>
              ))}
            </section>
          );

          return (
            <AppShellFrame
              eyebrow="Overview"
              title="__PROJECT_NAME__"
              description="A genuinely usable starter workspace with seeded routes, reusable shell primitives, and enough real structure to start product work instead of rebuilding the frame."
              spotlight={spotlight}
            >
              <section className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
                <SurfaceCard className="p-6">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Current focus tracks</div>
                      <div className="mt-2 text-2xl font-medium tracking-[-0.05em] text-white">Ship the frame before the feature flood arrives.</div>
                    </div>
                  </div>
                  <div className="mt-6 grid gap-4 md:grid-cols-3">
                    {dashboardFocus.map((item) => (
                      <div key={item.title} className="rounded-[24px] border border-white/10 bg-black/20 p-5">
                        <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">{item.label}</div>
                        <div className="mt-3 text-lg font-medium text-white">{item.title}</div>
                        <p className="mt-3 text-sm leading-7 ds-muted">{item.body}</p>
                      </div>
                    ))}
                  </div>
                </SurfaceCard>

                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Signal feed</div>
                  <div className="mt-4 space-y-4">
                    {signalFeed.map((item, index) => (
                      <div key={item.title} className="rounded-[22px] border border-white/10 bg-black/20 p-4">
                        <div className="font-mono text-xs uppercase tracking-[0.24em] text-[var(--accent)]">0{index + 1}</div>
                        <div className="mt-2 text-sm font-medium text-white">{item.title}</div>
                        <p className="mt-2 text-sm leading-7 ds-muted">{item.body}</p>
                      </div>
                    ))}
                  </div>
                </SurfaceCard>
              </section>

              <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Starter contract</div>
                  <div className="mt-3 text-2xl font-medium tracking-[-0.05em] text-white">What this shell gives you on day one</div>
                  <div className="mt-6 grid gap-4 md:grid-cols-2">
                    {[
                      "A routed overview, pipeline, library, and settings flow.",
                      "A reusable nav + topbar frame instead of one-off page chrome.",
                      "Shared panel treatments, spacing rhythm, and type hierarchy.",
                      "Seed data that shows how lists, metrics, and detail surfaces should feel.",
                    ].map((item) => (
                      <div key={item} className="rounded-[22px] border border-white/10 bg-black/20 p-4 text-sm leading-7 text-white">
                        {item}
                      </div>
                    ))}
                  </div>
                </SurfaceCard>

                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Next move</div>
                  <div className="mt-3 text-2xl font-medium tracking-[-0.05em] text-white">Replace the seed data, keep the patterns.</div>
                  <p className="mt-4 text-sm leading-7 ds-muted">
                    This is the moment to swap in your real routes, labels, and data contracts while keeping the frame, density, and canonical surface language intact.
                  </p>
                </SurfaceCard>
              </section>
            </AppShellFrame>
          );
        }
        """,
        PROJECT_NAME=project_name,
    )


def render_app_shell_data() -> str:
    return textwrap.dedent(
        """
        export const shellNavItems = [
          { href: "/", label: "Overview", note: "System pulse" },
          { href: "/pipeline", label: "Pipeline", note: "Work in motion" },
          { href: "/library", label: "Library", note: "Reusable blocks" },
          { href: "/settings", label: "Settings", note: "Defaults and governance" },
        ] as const;

        export const launchMetrics = [
          { label: "Routes seeded", value: "04", note: "overview, pipeline, library, settings" },
          { label: "Canonical surfaces", value: "09", note: "metrics, queues, settings, collections" },
          { label: "Starter debt", value: "03", note: "replace content, wire data, refine motion" },
          { label: "Docs status", value: "ON", note: "baseline docs root generated" },
        ] as const;

        export const dashboardFocus = [
          {
            label: "Primary workspace",
            title: "Overview becomes the command surface.",
            body: "Start with one page that shows health, work in motion, and the decisions that matter next.",
          },
          {
            label: "Operational rhythm",
            title: "Pipeline owns status and throughput.",
            body: "The shell already separates current work, blocked work, and ready-to-ship work into distinct surfaces.",
          },
          {
            label: "System memory",
            title: "Library and settings preserve the rules.",
            body: "Teams can add new product features without re-litigating the design system every sprint.",
          },
        ] as const;

        export const signalFeed = [
          {
            title: "Promote top-level sections into product routes immediately.",
            body: "This starter already assumes a routed workspace. Keep that momentum instead of collapsing back into a single dashboard page.",
          },
          {
            title: "Keep the nav labels operational.",
            body: "Use concrete route names and avoid turning the shell back into homepage language once real content lands.",
          },
          {
            title: "Treat the panel system as reusable infrastructure.",
            body: "Preserve the same curvature, line, density, and contrast language when you add tables, charts, and forms.",
          },
        ] as const;

        export const pipelineColumns = [
          {
            title: "Ready now",
            eyebrow: "03 streams",
            tasks: [
              "Wire overview metrics to live service data.",
              "Map library collections to actual product modules.",
              "Replace placeholder labels with domain language.",
            ],
          },
          {
            title: "In motion",
            eyebrow: "02 streams",
            tasks: [
              "Refine mobile nav density and overflow behavior.",
              "Add table and empty-state variants to the shell.",
              "Thread auth state into the topbar and settings route.",
            ],
          },
          {
            title: "Blocked / later",
            eyebrow: "03 streams",
            tasks: [
              "Finalize analytics and release instrumentation.",
              "Choose whether to add docs site on top of DOCS root.",
              "Decide where design token ownership lives long-term.",
            ],
          },
        ] as const;

        export const releaseChecklist = [
          "Overview route reads clearly with production data.",
          "Pipeline states map to the team’s actual workflow.",
          "Library blocks align with real component ownership.",
          "Settings route documents the defaults worth preserving.",
        ] as const;

        export const libraryCollections = [
          {
            title: "Navigation patterns",
            count: "06 blocks",
            body: "Sidebar, topbar, mobile overflow, route headers, and supporting status elements.",
          },
          {
            title: "Surface primitives",
            count: "09 blocks",
            body: "Metrics, panel stacks, signal feed cards, settings groups, and collection tiles.",
          },
          {
            title: "System voice",
            count: "04 rules",
            body: "Operational labels, muted support copy, high-contrast headings, and one accent hierarchy.",
          },
        ] as const;

        export const recentBlocks = [
          { name: "Route frame", kind: "Layout", status: "Stable" },
          { name: "Metric tile", kind: "Dashboard", status: "Ready to extend" },
          { name: "Pipeline column", kind: "Workflow", status: "Seeded" },
          { name: "Settings group", kind: "Forms", status: "Seeded" },
        ] as const;

        export const tokenFamilies = [
          { label: "Canvas", value: "Night ink / deep slate" },
          { label: "Accent", value: "Seafoam + warm sand" },
          { label: "Type", value: "Space Grotesk + IBM Plex Mono" },
          { label: "Surface", value: "Blurred panels with one line weight" },
        ] as const;
        """
    )


def render_app_shell_nav() -> str:
    return textwrap.dedent(
        """
        "use client";

        import Link from "next/link";
        import { usePathname } from "next/navigation";
        import { cn } from "@/lib/utils";
        import { shellNavItems } from "@/lib/app-shell-data";
        import { siteConfig } from "@/lib/site-config";

        export function AppShellNav() {
          const pathname = usePathname();

          return (
            <aside className="space-y-4">
              <div className="ds-panel rounded-[30px] p-5">
                <div className="flex items-center gap-3">
                  <span className="inline-flex size-11 items-center justify-center rounded-full border border-white/10 bg-white/6 font-mono text-xs uppercase tracking-[0.26em] text-[var(--accent)]">
                    DS
                  </span>
                  <div>
                    <div className="text-sm font-medium tracking-[-0.03em] text-white">{siteConfig.name}</div>
                    <div className="text-xs text-[var(--muted)]">Design-system-first starter</div>
                  </div>
                </div>

                <nav className="mt-6 space-y-2">
                  {shellNavItems.map((item) => {
                    const active = pathname === item.href;

                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={cn(
                          "block rounded-[22px] border px-4 py-3 transition",
                          active
                            ? "border-[var(--accent)]/40 bg-[linear-gradient(135deg,rgba(141,242,211,0.16),rgba(255,255,255,0.04))]"
                            : "border-white/8 bg-black/10 hover:border-white/15 hover:bg-white/5"
                        )}
                      >
                        <div className="text-sm font-medium text-white">{item.label}</div>
                        <div className="mt-1 text-xs text-[var(--muted)]">{item.note}</div>
                      </Link>
                    );
                  })}
                </nav>
              </div>

              <div className="ds-panel rounded-[28px] p-5">
                <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Rollout pulse</div>
                <div className="mt-3 text-lg font-medium text-white">Replace the content, not the frame.</div>
                <p className="mt-3 text-sm leading-7 ds-muted">
                  This shell is meant to survive the first product sprint. Preserve the route structure and surface language while real features land.
                </p>
              </div>
            </aside>
          );
        }
        """
    )


def render_app_shell_frame() -> str:
    return textwrap.dedent(
        """
        import type { ReactNode } from "react";
        import { Badge } from "@/components/ui/badge";
        import { Button } from "@/components/ui/button";
        import { Input } from "@/components/ui/input";
        import { AppShellNav } from "@/components/app-shell-nav";
        import { siteConfig } from "@/lib/site-config";

        type AppShellFrameProps = {
          eyebrow: string;
          title: string;
          description: string;
          children: ReactNode;
          spotlight?: ReactNode;
        };

        export function AppShellFrame({
          eyebrow,
          title,
          description,
          children,
          spotlight,
        }: AppShellFrameProps) {
          return (
            <main className="pb-16">
              <div className="ds-shell">
                <div className="grid gap-6 xl:grid-cols-[280px_minmax(0,1fr)]">
                  <AppShellNav />

                  <section className="space-y-6">
                    <div className="ds-panel rounded-[32px] p-6 md:p-7">
                      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
                        <div className="space-y-4">
                          <Badge variant="outline" className="rounded-full border-[var(--line)] bg-white/5 px-3 py-1 text-[var(--accent)]">
                            {eyebrow}
                          </Badge>
                          <div>
                            <h1 className="text-4xl font-medium tracking-[-0.06em] text-white md:text-5xl">
                              {title}
                            </h1>
                            <p className="mt-4 max-w-3xl text-sm leading-8 ds-muted">{description}</p>
                          </div>
                        </div>

                        <div className="flex w-full max-w-md flex-col gap-3">
                          <Input
                            readOnly
                            value={`Search ${siteConfig.mode === "app-shell" ? "routes, components, and queues" : "sections and proof points"}`}
                            className="rounded-full border-[var(--line)] bg-black/20 text-[var(--muted)]"
                          />
                          <div className="flex flex-wrap gap-2">
                            <Button type="button" className="rounded-full bg-[var(--accent)] px-5 text-black hover:bg-[var(--accent)]/90">
                              Refine starter
                            </Button>
                            <Button type="button" variant="outline" className="rounded-full border-[var(--line)] bg-white/5 px-5 text-white">
                              Review tokens
                            </Button>
                          </div>
                        </div>
                      </div>

                      {spotlight ? <div className="mt-6">{spotlight}</div> : null}
                    </div>

                    {children}
                  </section>
                </div>
              </div>
            </main>
          );
        }
        """
    )


def render_pipeline_page() -> str:
    return textwrap.dedent(
        """
        import { AppShellFrame } from "@/components/app-shell-frame";
        import { SurfaceCard } from "@/components/surface-card";
        import { pipelineColumns, releaseChecklist } from "@/lib/app-shell-data";

        export default function PipelinePage() {
          return (
            <AppShellFrame
              eyebrow="Pipeline"
              title="Work in motion"
              description="Use this route as the operational view for current initiatives, blocked work, and release readiness. It is meant to become the team’s working page, not a decorative dashboard."
            >
              <section className="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
                <div className="grid gap-4 lg:grid-cols-3">
                  {pipelineColumns.map((column) => (
                    <SurfaceCard key={column.title} className="p-5">
                      <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">{column.eyebrow}</div>
                      <div className="mt-3 text-xl font-medium tracking-[-0.04em] text-white">{column.title}</div>
                      <div className="mt-4 space-y-3">
                        {column.tasks.map((task) => (
                          <div key={task} className="rounded-[18px] border border-white/10 bg-black/20 p-4 text-sm leading-7 text-white">
                            {task}
                          </div>
                        ))}
                      </div>
                    </SurfaceCard>
                  ))}
                </div>

                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Release checklist</div>
                  <div className="mt-4 space-y-3">
                    {releaseChecklist.map((item) => (
                      <div key={item} className="rounded-[20px] border border-white/10 bg-black/20 p-4 text-sm leading-7 text-white">
                        {item}
                      </div>
                    ))}
                  </div>
                </SurfaceCard>
              </section>
            </AppShellFrame>
          );
        }
        """
    )


def render_library_page() -> str:
    return textwrap.dedent(
        """
        import { AppShellFrame } from "@/components/app-shell-frame";
        import { SurfaceCard } from "@/components/surface-card";
        import { libraryCollections, recentBlocks, tokenFamilies } from "@/lib/app-shell-data";

        export default function LibraryPage() {
          return (
            <AppShellFrame
              eyebrow="Library"
              title="Reusable building blocks"
              description="The library route is where teams can grow the system without losing the starter’s hierarchy. Keep collections, variants, and naming concrete here."
            >
              <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Collections</div>
                  <div className="mt-4 grid gap-4 md:grid-cols-3">
                    {libraryCollections.map((item) => (
                      <div key={item.title} className="rounded-[24px] border border-white/10 bg-black/20 p-5">
                        <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">{item.count}</div>
                        <div className="mt-3 text-lg font-medium text-white">{item.title}</div>
                        <p className="mt-3 text-sm leading-7 ds-muted">{item.body}</p>
                      </div>
                    ))}
                  </div>
                </SurfaceCard>

                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Recent blocks</div>
                  <div className="mt-4 space-y-3">
                    {recentBlocks.map((item) => (
                      <div key={item.name} className="grid grid-cols-[1.2fr_0.9fr_0.9fr] gap-3 rounded-[18px] border border-white/10 bg-black/20 px-4 py-3 text-sm text-white">
                        <div>{item.name}</div>
                        <div className="ds-muted">{item.kind}</div>
                        <div className="text-[var(--accent)]">{item.status}</div>
                      </div>
                    ))}
                  </div>
                </SurfaceCard>
              </section>

              <SurfaceCard className="p-6">
                <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Token families</div>
                <div className="mt-4 grid gap-4 md:grid-cols-4">
                  {tokenFamilies.map((item) => (
                    <div key={item.label} className="rounded-[22px] border border-white/10 bg-black/20 p-4">
                      <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">{item.label}</div>
                      <div className="mt-3 text-sm leading-7 text-white">{item.value}</div>
                    </div>
                  ))}
                </div>
              </SurfaceCard>
            </AppShellFrame>
          );
        }
        """
    )


def render_settings_page() -> str:
    return textwrap.dedent(
        """
        import { Button } from "@/components/ui/button";
        import { Input } from "@/components/ui/input";
        import { AppShellFrame } from "@/components/app-shell-frame";
        import { SurfaceCard } from "@/components/surface-card";

        export default function SettingsPage() {
          return (
            <AppShellFrame
              eyebrow="Settings"
              title="Defaults worth preserving"
              description="This route gives the starter a real governance surface. It is where teams should document shell decisions, design tokens, and operational defaults before entropy sets in."
            >
              <section className="grid gap-4 xl:grid-cols-[1fr_1fr]">
                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">Workspace defaults</div>
                  <div className="mt-4 space-y-4">
                    <div>
                      <div className="mb-2 text-sm text-[var(--muted)]">Workspace name</div>
                      <Input defaultValue="Design System First Playground" className="rounded-2xl border-[var(--line)] bg-black/20 text-white" />
                    </div>
                    <div>
                      <div className="mb-2 text-sm text-[var(--muted)]">Primary owner</div>
                      <Input defaultValue="Product design + frontend" className="rounded-2xl border-[var(--line)] bg-black/20 text-white" />
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <Button type="button" className="rounded-full bg-[var(--accent)] text-black hover:bg-[var(--accent)]/90">Save defaults</Button>
                      <Button type="button" variant="outline" className="rounded-full border-[var(--line)] bg-white/5 text-white">Review docs root</Button>
                    </div>
                  </div>
                </SurfaceCard>

                <SurfaceCard className="p-6">
                  <div className="text-xs uppercase tracking-[0.24em] text-[var(--muted)]">System rules</div>
                  <div className="mt-4 space-y-3">
                    {[
                      "Keep route names operational and product-facing.",
                      "Add new panels by reusing the same line weight, radius, and density.",
                      "Promote successful one-off surfaces back into the library route.",
                      "Treat docs root as the home for durable decisions, not temporary chat context.",
                    ].map((item) => (
                      <div key={item} className="rounded-[20px] border border-white/10 bg-black/20 p-4 text-sm leading-7 text-white">
                        {item}
                      </div>
                    ))}
                  </div>
                </SurfaceCard>
              </section>
            </AppShellFrame>
          );
        }
        """
    )


def update_package_json(project_dir: Path, mutator) -> None:
    package_json_path = project_dir / "package.json"
    package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
    mutator(package_json)
    write_text(package_json_path, json.dumps(package_json, indent=2))


def apply_design_system_overlay(
    project_dir: Path,
    project_name: str,
    mode: str,
    addons: list[str],
) -> None:
    description = site_description(mode)
    write_text(project_dir / "src/app/layout.tsx", render_layout(project_name, description))
    write_text(project_dir / "src/app/globals.css", render_globals_css())
    write_text(project_dir / "src/lib/site-config.ts", render_site_config(project_name, mode, addons))
    write_text(project_dir / "src/components/surface-card.tsx", render_surface_card())

    if mode == "marketing-only":
        write_text(project_dir / "src/components/site-header.tsx", render_site_header())
        write_text(project_dir / "src/app/page.tsx", render_marketing_page(project_name))
    else:
        write_text(project_dir / "src/lib/app-shell-data.ts", render_app_shell_data())
        write_text(project_dir / "src/components/app-shell-nav.tsx", render_app_shell_nav())
        write_text(project_dir / "src/components/app-shell-frame.tsx", render_app_shell_frame())
        write_text(project_dir / "src/app/page.tsx", render_app_page(project_name))
        write_text(project_dir / "src/app/pipeline/page.tsx", render_pipeline_page())
        write_text(project_dir / "src/app/library/page.tsx", render_library_page())
        write_text(project_dir / "src/app/settings/page.tsx", render_settings_page())


def apply_testing_scaffold(project_dir: Path, package_manager: PackageManager) -> None:
    smoke_port = 3310

    run(
        package_manager.dev_install
        + [
            "vitest",
            "@vitejs/plugin-react",
            "jsdom",
            "@testing-library/react",
            "@testing-library/jest-dom",
            "@testing-library/user-event",
            "@playwright/test",
        ],
        cwd=project_dir,
    )

    write_text(
        project_dir / "vitest.config.ts",
        textwrap.dedent(
            """
            import path from "node:path";
            import { defineConfig } from "vitest/config";
            import react from "@vitejs/plugin-react";

            export default defineConfig({
              plugins: [react()],
              test: {
                environment: "jsdom",
                globals: true,
                setupFiles: "./vitest.setup.ts",
                include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
                exclude: ["tests/**", "node_modules/**"],
              },
              resolve: {
                alias: {
                  "@": path.resolve(__dirname, "./src"),
                },
              },
            });
            """
        ),
    )

    write_text(
        project_dir / "vitest.setup.ts",
        textwrap.dedent(
            """
            import "@testing-library/jest-dom/vitest";
            """
        ),
    )

    write_text(
        project_dir / "src/components/surface-card.test.tsx",
        textwrap.dedent(
            """
            import { render, screen } from "@testing-library/react";
            import { SurfaceCard } from "@/components/surface-card";

            describe("SurfaceCard", () => {
              it("renders content inside the canonical starter surface", () => {
                render(<SurfaceCard>Starter surface</SurfaceCard>);

                expect(screen.getByText("Starter surface")).toBeInTheDocument();
              });
            });
            """
        ),
    )

    write_text(
        project_dir / "playwright.config.ts",
        textwrap.dedent(
            f"""
            import {{ defineConfig, devices }} from "@playwright/test";

            export default defineConfig({{
              testDir: "./tests",
              retries: process.env.CI ? 2 : 0,
              use: {{
                baseURL: "http://127.0.0.1:{smoke_port}",
                trace: "on-first-retry",
              }},
              webServer: {{
                command: {json.dumps(package_manager.run_script("dev:smoke"))},
                port: {smoke_port},
                reuseExistingServer: false,
                timeout: 120_000,
              }},
              projects: [
                {{
                  name: "chromium",
                  use: {{ ...devices["Desktop Chrome"] }},
                }},
              ],
            }});
            """
        ),
    )

    write_text(
        project_dir / "tests/home.spec.ts",
        textwrap.dedent(
            """
            import { expect, test } from "@playwright/test";

            test("home page renders the starter shell", async ({ page }) => {
              await page.goto("/");

              await expect(page.locator("main")).toBeVisible();
              await expect(page.getByRole("heading").first()).toBeVisible();
            });
            """
        ),
    )

    def add_test_scripts(package_json: dict) -> None:
        scripts = package_json.setdefault("scripts", {})
        scripts["dev:smoke"] = f"next dev --hostname 127.0.0.1 --port {smoke_port}"
        scripts["test"] = "vitest run"
        scripts["test:watch"] = "vitest"
        scripts["test:e2e"] = "playwright test"

    update_package_json(project_dir, add_test_scripts)


def locate_docs_skill() -> Path:
    codex_home = Path((Path.home() / ".codex").expanduser())
    candidates = [codex_home / "skills" / "docs-system-scaffold", *DOCS_SKILL_CANDIDATES]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise SystemExit("Could not locate docs-system-scaffold skill assets for the docs add-on.")


def docs_placeholders(project_dir: Path, docs_root: str = "DOCS") -> dict[str, str]:
    docs_skill = locate_docs_skill()
    timestamp_script = docs_skill / "assets/scripts/scripts/docs/timestamp-et.mjs"
    timestamp_payload = subprocess.run(
        ["node", str(timestamp_script), "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    timestamp_data = json.loads(timestamp_payload.stdout)
    return {
        "{{DOCS_ROOT}}": docs_root,
        "{{LAST_UPDATED_DATE_ET}}": timestamp_data["dateEt"],
        "{{LAST_UPDATED_TS_ET}}": timestamp_data["timestampEt"],
        "{{PROJECT_NAME}}": project_dir.name,
    }


def render_with_placeholders(content: str, replacements: dict[str, str]) -> str:
    rendered = content
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def copy_docs_tree(source_dir: Path, target_dir: Path, replacements: dict[str, str]) -> None:
    for path in source_dir.rglob("*"):
        relative_path = path.relative_to(source_dir)
        destination = target_dir / relative_path
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in {".md", ".yml", ".json"} or path.name.endswith(".mjs"):
            content = path.read_text(encoding="utf-8")
            if path.suffix in {".md", ".yml", ".json"}:
                content = render_with_placeholders(content, replacements)
            destination.write_text(content, encoding="utf-8")
        else:
            shutil.copy2(path, destination)


def apply_docs_scaffold(project_dir: Path) -> None:
    docs_skill = locate_docs_skill()
    replacements = docs_placeholders(project_dir)

    docs_root = project_dir / "DOCS"
    docs_root.mkdir(parents=True, exist_ok=True)

    copy_docs_tree(
        docs_skill / "assets/templates/docs-root",
        docs_root,
        replacements,
    )
    copy_docs_tree(
        docs_skill / "assets/templates/governance",
        project_dir,
        replacements,
    )
    copy_docs_tree(
        docs_skill / "assets/scripts/scripts/docs",
        project_dir / "scripts/docs",
        replacements,
    )

    def add_docs_scripts(package_json: dict) -> None:
        scripts = package_json.setdefault("scripts", {})
        scripts.setdefault("docs:manifest", "node scripts/docs/manifest.mjs DOCS")
        scripts.setdefault("docs:links", "node scripts/docs/check-links.mjs DOCS")
        scripts.setdefault("docs:frontmatter", "node scripts/docs/normalize-frontmatter.mjs DOCS")
        scripts.setdefault("docs:timestamp", "node scripts/docs/timestamp-et.mjs --json")

    update_package_json(project_dir, add_docs_scripts)

    manifest_script = project_dir / "scripts/docs/manifest.mjs"
    if manifest_script.exists():
        run(["node", str(manifest_script), "DOCS"], cwd=project_dir)


def print_summary(project_dir: Path, mode: str, addons: list[str]) -> None:
    print("\nScaffold complete.")
    print(f"Project: {project_dir}")
    print(f"Mode: {mode}")
    print(f"Add-ons: {', '.join(addons) if addons else 'none'}")
    print("\nRecommended follow-ons:")
    print("- Use $shadcn for additional components or registry items.")
    if mode == "marketing-only":
        print("- Use $frontend-skill for a stronger art-direction pass.")
    else:
        print("- Use $design-system-refine to tighten density, hierarchy, and shell details.")
    print("- Use $react-best-practices after larger React/Next edits.")
    if "docs" in addons:
        print("- Use $docs-system-scaffold later if you want a docs site or product-doc pack on top of the baseline docs root.")
    if "testing" in addons:
        print("- Run `npx playwright install chromium` before the first e2e run if the browser is not installed yet.")
    print("\nSuggested MCPs / plugins to consider:")
    print("- Vercel for deployment, preview URLs, and runtime logs.")
    print("- GitHub for PR workflow and CI inspection.")
    if "testing" in addons:
        print("- Playwright/browser verification tooling for UI checks.")


def main() -> int:
    args = parse_args()
    target_dir = Path(args.path).expanduser().resolve()
    project_name = args.name or target_dir.name.replace("-", " ").title()
    addons = parse_addons(args.addons)
    package_manager = PackageManager(args.package_manager)

    ensure_target_is_empty(target_dir)
    scaffold_next_app(target_dir, project_name, package_manager)
    initialize_shadcn(target_dir, args.mode, package_manager)
    apply_design_system_overlay(target_dir, project_name, args.mode, addons)

    if "testing" in addons:
        apply_testing_scaffold(target_dir, package_manager)
    if "docs" in addons:
        apply_docs_scaffold(target_dir)

    print_summary(target_dir, args.mode, addons)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
