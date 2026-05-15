import fs from 'node:fs'
import path from 'node:path'

const cwd = process.cwd()
const argRoot = process.argv[2]

function detectDocsRoot() {
  const canonical = 'DOCS'
  const entries = fs.readdirSync(cwd, { withFileTypes: true })
  return entries.some((entry) => entry.name === canonical && entry.isDirectory()) ? canonical : null
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

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[`*_~]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
}

function extractHeadings(content) {
  const headings = []
  const re = /^(#{1,6})\s+(.+)$/gm
  let match
  while ((match = re.exec(content))) {
    headings.push(match[2].trim())
  }
  const seen = new Map()
  const slugs = new Set()
  for (const h of headings) {
    let slug = slugify(h)
    const count = seen.get(slug) || 0
    if (count > 0) {
      slug = `${slug}-${count}`
    }
    seen.set(slugify(h), count + 1)
    slugs.add(slug)
  }
  return slugs
}

const docsRoot = argRoot || detectDocsRoot()
if (docsRoot !== 'DOCS' || !detectDocsRoot()) {
  console.error('No canonical docs root found. Create DOCS/ or pass DOCS as the first argument.')
  process.exit(1)
}

const rootPath = path.join(cwd, docsRoot)
const files = walk(rootPath)
const errors = []

for (const fp of files) {
  const content = fs.readFileSync(fp, 'utf8')
  const dir = path.dirname(fp)
  const links = [...content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map(m => m[1])
  for (const raw of links) {
    if (!raw) continue
    if (raw.startsWith('http://') || raw.startsWith('https://')) continue
    if (raw.startsWith('mailto:') || raw.startsWith('tel:')) continue
    if (raw.startsWith('#')) {
      const anchors = extractHeadings(content)
      const target = raw.slice(1)
      if (target && !anchors.has(target)) {
        errors.push(`${path.relative(cwd, fp)}: missing anchor #${target}`)
      }
      continue
    }

    const [targetPathRaw, anchor] = raw.split('#')
    let targetPath = targetPathRaw

    if (!targetPath || targetPath === '.') {
      targetPath = fp
    } else {
      const resolved = path.resolve(dir, targetPath)
      const candidates = [
        resolved,
        `${resolved}.md`,
        path.join(resolved, 'index.md'),
      ]
      const existing = candidates.find(c => fs.existsSync(c))
      if (!existing) {
        errors.push(`${path.relative(cwd, fp)}: missing file ${targetPathRaw}`)
        continue
      }
      targetPath = existing
    }

    if (anchor) {
      const targetContent = fs.readFileSync(targetPath, 'utf8')
      const anchors = extractHeadings(targetContent)
      if (!anchors.has(anchor)) {
        errors.push(`${path.relative(cwd, fp)}: missing anchor #${anchor} in ${path.relative(cwd, targetPath)}`)
      }
    }
  }
}

if (errors.length) {
  console.error('Broken links found:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Link check passed')
