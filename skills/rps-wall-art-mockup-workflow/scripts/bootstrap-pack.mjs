#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const [, , packRoot, packSlug] = process.argv;

if (!packRoot || !packSlug) {
  console.error("Usage: node scripts/bootstrap-pack.mjs <pack-root> <pack-slug>");
  process.exit(1);
}

const destination = path.resolve(packRoot, packSlug);
if (fs.existsSync(destination)) {
  console.error(`Pack already exists: ${destination}`);
  process.exit(1);
}

fs.mkdirSync(path.join(destination, "raw-bases"), { recursive: true });
fs.mkdirSync(path.join(destination, "composited-examples"), { recursive: true });

const manifest = {
  packId: packSlug,
  title: packSlug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" "),
  createdAt: "",
  lastUpdated: "",
  status: "draft",
  preferredOption: null,
  surfaces: ["shopify-listing"],
  useCase: "",
  guardrail:
    "Generated bases use blank placeholders only; real RPS artwork is composited locally.",
  files: {
    reviewBoard: "review-board.jpg",
    rawBases: [],
    compositedExamples: [],
    sourceAssets: [],
  },
  outputs: [],
  promptPattern: "",
  reuseNotes: [],
};

fs.writeFileSync(
  path.join(destination, "manifest.json"),
  `${JSON.stringify(manifest, null, 2)}\n`,
);

console.log(`Created ${destination}`);
