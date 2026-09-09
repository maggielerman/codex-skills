import Link from "next/link";
import { PageShell } from "@/components/site/shell";
export const metadata = { title: "Getting started | Codex Skills" };
export default function GettingStarted() {
  return (
    <PageShell>
      <main id="main" className="guide-page">
        <section className="intro compact">
          <h1>
            Start with one
            <br />
            useful workflow.
          </h1>
          <p>
            A skill is a set of instructions with the references and tools
            needed to repeat a task. A plugin packages related skills together.
          </p>
        </section>
        <div className="article-body">
          <section>
            <h2>1. Find your starting point</h2>
            <p>
              Use <Link href="/plugins/context-layer">Context Layer</Link> to
              organize ongoing project work. Explore{" "}
              <Link href="/skills/rps-print-order">RPS Print Order</Link> for a
              concrete business workflow, or{" "}
              <Link href="/docs">browse the full library</Link> for your stack.
            </p>
          </section>
          <section>
            <h2>2. Read the source</h2>
            <p>
              Each guide links to its complete source folder. Read SKILL.md and
              its references before running a workflow. RPS skills describe my
              business setup and need its services and repositories; they are
              useful examples, not turnkey integrations for another business.
            </p>
            <p>
              This collection includes custom work and upstream material. The
              repository is publicly viewable, but no general open-source
              license has been selected. Check the{" "}
              <a href="https://github.com/maggielerman/codex-skills#license">
                license notes
              </a>{" "}
              and any bundled notices for the files you want to use.
            </p>
          </section>
          <section>
            <h2>3. Keep the package together</h2>
            <p>
              When permitted, copy the complete skill folder into your Codex
              skills directory. Keep scripts, references, assets, and SKILL.md
              together. For a plugin, retain its whole package, including
              .codex-plugin/plugin.json and its bundled skills.
            </p>
            <p>
              Refresh your Codex session, then invoke the skill by name in the
              target project. Follow its documented setup and working directory.
            </p>
          </section>
          <section>
            <h2>4. Give it a concrete task</h2>
            <pre>{`Use $context-layer-scaffold to organize this repository.\nRead its existing instructions first.\nPreserve current documentation and propose a clear structure.`}</pre>
            <p>
              State your outcome, constraints, and what the agent can change.
              Review the result and verify it in your own environment.
            </p>
          </section>
          <section>
            <h2>Questions or improvements?</h2>
            <p>
              <a href="https://github.com/maggielerman/codex-skills/issues">
                Open a GitHub issue
              </a>{" "}
              with the workflow name, what you expected, and what happened.
              Leave credentials and private project data out of the example.
            </p>
          </section>
        </div>
      </main>
    </PageShell>
  );
}
