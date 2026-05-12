import fs from 'node:fs'
import path from 'node:path'

const cwd = process.cwd()
const argRoot = process.argv[2]

function detectDocsRoot() {
  const candidates = ['DOCS', 'docs', 'documentation']
  for (const c of candidates) {
    const full = path.join(cwd, c)
    if (fs.existsSync(full) && fs.statSync(full).isDirectory()) {
      return c
    }
  }
  return null
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

function titleFromFile(fp, content) {
  const match = content.match(/^#\s+(.+)$/m)
  if (match) return match[1].trim()
  const base = path.basename(fp, '.md')
  return base.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function today() {
  const d = new Date()
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

function parseFrontmatter(content) {
  if (!content.startsWith('---')) return null
  const end = content.indexOf('\n---', 3)
  if (end === -1) return null
  const block = content.slice(3, end).trim()
  const data = {}
  for (const line of block.split('\n')) {
    const idx = line.indexOf(':')
    if (idx === -1) continue
    const key = line.slice(0, idx).trim()
    const val = line.slice(idx + 1).trim()
    data[key] = val
  }
  return { data, endIndex: end + 4 }
}

function buildFrontmatter(data) {
  const lines = ['---']
  for (const [k, v] of Object.entries(data)) {
    lines.push(`${k}: ${v}`)
  }
  lines.push('---')
  return lines.join('\n') + '\n\n'
}

const docsRoot = argRoot || detectDocsRoot()
if (!docsRoot) {
  console.error('No docs root found. Pass DOCS or docs as the first argument.')
  process.exit(1)
}

const rootPath = path.join(cwd, docsRoot)
const files = walk(rootPath)
let updated = 0

for (const fp of files) {
  const content = fs.readFileSync(fp, 'utf8')
  const fm = parseFrontmatter(content)
  const required = {
    title: titleFromFile(fp, content),
    description: 'TODO: Add description',
    status: 'draft',
    lastUpdated: today(),
    owner: 'Documentation',
  }

  if (!fm) {
    const newContent = buildFrontmatter(required) + content
    fs.writeFileSync(fp, newContent)
    updated += 1
    continue
  }

  let changed = false
  const data = { ...fm.data }
  for (const [k, v] of Object.entries(required)) {
    if (!data[k]) {
      data[k] = v
      changed = true
    }
  }

  if (changed) {
    const rest = content.slice(fm.endIndex)
    const newContent = buildFrontmatter(data) + rest.replace(/^\n+/, '')
    fs.writeFileSync(fp, newContent)
    updated += 1
  }
}

console.log(`Frontmatter normalized in ${updated} files`)
