#!/usr/bin/env node

const TZ = 'America/New_York'

function partValue(parts, type) {
  const part = parts.find((p) => p.type === type)
  if (!part) {
    throw new Error(`Missing date part: ${type}`)
  }
  return part.value
}

function buildTimestamp(date = new Date()) {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZoneName: 'short',
  })

  const parts = formatter.formatToParts(date)
  const year = partValue(parts, 'year')
  const month = partValue(parts, 'month')
  const day = partValue(parts, 'day')
  const hour = partValue(parts, 'hour')
  const minute = partValue(parts, 'minute')
  const zoneAbbrev = partValue(parts, 'timeZoneName')

  const dateEt = `${year}-${month}-${day}`
  const timestampEt = `${dateEt} ${hour}:${minute} ET (${TZ})`

  return {
    dateEt,
    timeEt: `${hour}:${minute}`,
    timestampEt,
    zoneAbbrev,
    timezone: TZ,
  }
}

function printUsage() {
  console.log('Usage: node timestamp-et.mjs [--json|--shell]')
  process.exit(0)
}

const args = new Set(process.argv.slice(2))
if (args.has('-h') || args.has('--help')) {
  printUsage()
}

const out = buildTimestamp()

if (args.has('--shell')) {
  console.log(`LAST_UPDATED_DATE_ET='${out.dateEt}'`)
  console.log(`LAST_UPDATED_TS_ET='${out.timestampEt}'`)
  console.log(`LAST_UPDATED_ZONE='${out.zoneAbbrev}'`)
  console.log(`LAST_UPDATED_TIMEZONE='${out.timezone}'`)
  process.exit(0)
}

console.log(JSON.stringify(out, null, 2))
