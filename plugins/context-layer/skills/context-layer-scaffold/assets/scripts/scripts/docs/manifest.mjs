import fs from 'node:fs'
import path from 'node:path'

const cwd = process.cwd()
const argRoot = process.argv[2]
const argOut = process.argv[3]

function detectDocsRoot() {
  const canonical = 'DOCS'
  const entries = fs.readdirSync(cwd, { withFileTypes: true })
  return entries.some((entry) => entry.name === canonical && entry.isDirectory()) ? canonical : null
}

function readFrontmatter(content) {
  if (!content.startsWith('---')) return null
  const end = content.indexOf('\n---', 3)
  if (end === -1) return null
  const block = content.slice(3, end).trim()
  const out = {}
  for (const line of block.split('\n')) {
    const idx = line.indexOf(':')
    if (idx === -1) continue
    const key = line.slice(0, idx).trim()
    const val = line.slice(idx + 1).trim()
    out[key] = val
  }
  return out
}

function findTitle(content, fm) {
  if (fm && fm.title) return fm.title
  const match = content.match(/^#\s+(.+)$/m)
  return match ? match[1].trim() : null
}

function walk(dir, out = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
  for (const e of entries) {
    if (e.name.startsWith('.')) continue
    if (e.name === 'node_modules') continue
    if (e.name === '.vitepress') continue
    const full = path.join(dir, e.name)
    if (e.isDirectory()) {
      walk(full, out)
    } else if (e.isFile() && e.name.endsWith('.md')) {
      out.push(full)
    }
  }
  return out
}

const docsRoot = argRoot || detectDocsRoot()
if (docsRoot !== 'DOCS' || !detectDocsRoot()) {
  console.error('No canonical docs root found. Create DOCS/ or pass DOCS as the first argument.')
  process.exit(1)
}

const rootPath = path.join(cwd, docsRoot)
const files = walk(rootPath)
const items = files.map(fp => {
  const content = fs.readFileSync(fp, 'utf8')
  const fm = readFrontmatter(content)
  return {
    path: path.relative(cwd, fp).replace(/\\/g, '/'),
    title: findTitle(content, fm),
    description: fm?.description || null,
    status: fm?.status || null,
    lastUpdated: fm?.lastUpdated || null,
    owner: fm?.owner || null,
  }
})

const outPath = argOut || path.join(rootPath, 'manifest.json')
fs.writeFileSync(outPath, JSON.stringify({ generatedAt: new Date().toISOString(), items }, null, 2))
console.log(`Wrote manifest to ${outPath}`)
