#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

log() {
  printf '[setup] %s\n' "$*" >&2
}

fail() {
  printf '[setup][error] %s\n' "$*" >&2
  exit 1
}

MIGRATE_URL="${DIRECT_URL:-${DATABASE_URL:-}}"
if [ -z "${MIGRATE_URL}" ]; then
  fail "DIRECT_URL (or DATABASE_URL) must be set for Prisma migrations"
fi

log "Running prisma generate"
npx prisma generate

log "Applying Prisma migrations"
DATABASE_URL="${MIGRATE_URL}" npx prisma migrate deploy

log "Prisma setup completed"
