#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
OVERLAYS_DIR = SKILL_ROOT / "assets" / "overlays"
SUPPORTED_FEATURES = {
  "merchant-comms",
  "review-prompts",
  "billing-stub",
  "app-proxy",
  "theme-extension",
}
SCAFFOLD_DEV_DEP_UPGRADES = {
  "@typescript-eslint/eslint-plugin": "^8.58.0",
  "@typescript-eslint/parser": "^8.58.0",
}
SCAFFOLD_PACKAGE_OVERRIDES = {
  "@prisma/config": {
    "effect": "3.20.0",
  },
  "@typescript-eslint/typescript-estree": {
    "minimatch": "9.0.9",
  },
}

CORE_POSTGRES_ENV_BLOCK = """
# Postgres / Prisma
DATABASE_URL=
DIRECT_URL=
""".strip()

MERCHANT_COMMS_ENV_BLOCK_TEMPLATE = """
# Merchant comms
SENDGRID_API_KEY=
EMAIL_FROM=
EMAIL_UNSUBSCRIBE_SECRET=
EMAIL_QUEUE_ENABLED=1
SHOPIFY_APP_STORE_URL={app_store_url}
""".strip()

BASE_ENV_TEMPLATE = """
# Shopify
SHOPIFY_API_KEY=
SHOPIFY_API_SECRET=
SCOPES={scopes}
SHOPIFY_APP_URL={app_url}

# App metadata
APP_NAME={app_name}
SUPPORT_EMAIL={support_email}
""".strip()

MERCHANT_COMMS_PRISMA_BLOCK = """
model ShopCommsPreferences {
  shop                String   @id
  contactEmail        String?
  emailOptIn          Boolean  @default(false)
  emailOptInAt        DateTime?
  emailOptInSource    String?
  emailUnsubscribedAt DateTime?
  uninstalledAt       DateTime?
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt
}

model EmailQueueItem {
  id          String   @id @default(cuid())
  shop        String
  toEmail     String
  template    String
  payload     Json?
  scheduledAt DateTime
  sentAt      DateTime?
  cancelledAt DateTime?
  lastError   String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([shop, scheduledAt])
  @@index([sentAt, scheduledAt])
}

model JobLock {
  id        String   @id
  owner     String
  lockedAt  DateTime @default(now())
  expiresAt DateTime @default(now())
}
""".strip()

REVIEW_PROMPTS_PRISMA_BLOCK = """
model ShopReviewState {
  shop             String   @id
  dismissed        Boolean  @default(false)
  lastRequestedAt  DateTime?
  lastResultCode   String?
  lastMilestoneId  String?
  createdAt        DateTime @default(now())
  updatedAt        DateTime @updatedAt
}
""".strip()


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
  return subprocess.run(
    cmd,
    cwd=str(cwd) if cwd else None,
    check=check,
    text=True,
    capture_output=capture,
  )


def log(message: str) -> None:
  print(f"[ML-shopify-app-scaffold] {message}")


def die(message: str) -> None:
  print(f"[ML-shopify-app-scaffold][error] {message}", file=sys.stderr)
  sys.exit(1)


def detect_shopify_version() -> tuple[str | None, str | None]:
  installed = None
  latest = None

  try:
    result = run(["shopify", "version"], capture=True, check=False)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if lines:
      installed = lines[-1]
  except Exception:
    installed = None

  try:
    result = run(["npm", "view", "@shopify/cli", "version"], capture=True, check=False)
    value = result.stdout.strip()
    if value:
      latest = value
  except Exception:
    latest = None

  return installed, latest


def ensure_target_ready(target: Path, skip_init: bool) -> None:
  if skip_init:
    if not target.exists():
      die(f"--skip-init was set but target does not exist: {target}")
    return

  if target.exists() and any(target.iterdir()):
    die(f"target already exists and is not empty: {target}")


def validate_existing_target(target: Path) -> None:
  required_paths = [
    target / "package.json",
    target / "prisma" / "schema.prisma",
  ]
  missing = [str(path.relative_to(target)) for path in required_paths if not path.exists()]
  if missing:
    die(
      "--skip-init expects an existing Shopify app target with "
      f"{', '.join(missing)} present: {target}"
    )


def slugify_app_name(value: str) -> str:
  slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
  return slug or "shopify-app"


def resolve_project_root(target: Path, app_name: str) -> Path:
  if (target / "package.json").exists():
    return target

  slugged = target / slugify_app_name(app_name)
  if (slugged / "package.json").exists():
    return slugged

  if target.exists():
    candidates = [
      child for child in target.iterdir()
      if child.is_dir() and (child / "package.json").exists() and (child / "shopify.app.toml").exists()
    ]
    if len(candidates) == 1:
      return candidates[0]

  die(
    "Shopify CLI finished, but the scaffolded app root could not be located under "
    f"{target}. Check whether the CLI created a nested slugged directory."
  )


def collapse_nested_project_root(requested_target: Path, actual_target: Path) -> Path:
  if actual_target == requested_target:
    return requested_target

  if actual_target.parent != requested_target:
    return actual_target

  extra_entries = [
    child for child in requested_target.iterdir()
    if child != actual_target and child.name != ".DS_Store"
  ]
  if extra_entries:
    log(
      "Leaving nested Shopify app directory in place because the requested path contains "
      f"other files: {', '.join(sorted(child.name for child in extra_entries))}"
    )
    return actual_target

  for child in actual_target.iterdir():
    shutil.move(str(child), str(requested_target / child.name))
  actual_target.rmdir()
  log(f"Collapsed nested Shopify app directory into requested path: {requested_target}")
  return requested_target


def scaffold_base_app(args: argparse.Namespace, target: Path) -> None:
  if args.skip_init:
    log("Skipping Shopify CLI app init because --skip-init was provided")
    return

  cmd = [
    "shopify",
    "app",
    "init",
    "--template",
    args.template,
    "--flavor",
    args.language,
    "--name",
    args.app_name,
    "--path",
    str(target),
    "--package-manager",
    args.package_manager,
  ]
  if args.client_id:
    cmd.extend(["--client-id", args.client_id])

  log("Running Shopify CLI scaffold")
  run(cmd)


def copy_tree(src: Path, dest: Path) -> None:
  for item in src.rglob("*"):
    if item.is_dir():
      continue
    relative = item.relative_to(src)
    out = dest / relative
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(item, out)


def upsert_env_block(env_path: Path, header: str, block: str) -> None:
  env_path.parent.mkdir(parents=True, exist_ok=True)
  existing = env_path.read_text() if env_path.exists() else ""
  marker = f"# --- {header} ---"
  if marker in existing:
    return

  text = existing.rstrip()
  if text:
    text += "\n\n"
  text += f"{marker}\n{block}\n"
  env_path.write_text(text)


def ensure_env_example_tracked(target: Path) -> bool:
  gitignore_path = target / ".gitignore"
  if not gitignore_path.exists():
    return False

  lines = gitignore_path.read_text().splitlines()
  if "!.env.example" in lines:
    return False

  lines.append("!.env.example")
  gitignore_path.write_text("\n".join(lines) + "\n")
  return True


def append_prisma_block(schema_path: Path, model_name: str, block: str) -> bool:
  if not schema_path.exists():
    die(f"Expected Prisma schema at {schema_path}")

  existing = schema_path.read_text()
  if f"model {model_name} " in existing:
    return False

  schema_path.write_text(existing.rstrip() + "\n\n" + block + "\n")
  return True


def configure_postgres_prisma_schema(schema_path: Path) -> bool:
  if not schema_path.exists():
    die(f"Expected Prisma schema at {schema_path}")

  existing = schema_path.read_text()
  replacement = """datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}"""
  updated = re.sub(
    r'datasource db \{[^}]*\}',
    replacement,
    existing,
    count=1,
    flags=re.DOTALL,
  )
  if updated == existing:
    return False

  schema_path.write_text(updated)
  return True


def load_package_json(path: Path) -> dict:
  if not path.exists():
    die(f"Expected package.json at {path}")
  return json.loads(path.read_text())


def write_package_json(path: Path, data: dict) -> None:
  path.write_text(json.dumps(data, indent=2) + "\n")


def harden_package_manifest(target: Path) -> bool:
  package_json_path = target / "package.json"
  package_json = load_package_json(package_json_path)
  changed = False

  dev_dependencies = package_json.setdefault("devDependencies", {})
  for name, version in SCAFFOLD_DEV_DEP_UPGRADES.items():
    if name in dev_dependencies and dev_dependencies[name] != version:
      dev_dependencies[name] = version
      changed = True

  overrides = package_json.setdefault("overrides", {})
  for name, override_value in SCAFFOLD_PACKAGE_OVERRIDES.items():
    if overrides.get(name) != override_value:
      overrides[name] = override_value
      changed = True

  if changed:
    write_package_json(package_json_path, package_json)

  return changed


def normalize_npmrc(target: Path, package_manager: str) -> bool:
  if package_manager != "npm":
    return False

  npmrc_path = target / ".npmrc"
  if not npmrc_path.exists():
    return False

  lines = npmrc_path.read_text().splitlines()
  filtered = [line for line in lines if line.strip() != "shamefully-hoist=true"]
  if filtered == lines:
    return False

  content = "\n".join(filtered)
  if content:
    content += "\n"
  npmrc_path.write_text(content)
  return True


def install_project_dependencies(target: Path, package_manager: str) -> None:
  install_commands = {
    "npm": ["npm", "install"],
    "yarn": ["yarn", "install"],
    "pnpm": ["pnpm", "install"],
    "bun": ["bun", "install"],
  }
  run(install_commands[package_manager], cwd=target)


def install_missing_dependencies(target: Path, package_manager: str, desired: list[str]) -> None:
  if not desired:
    return

  package_json = load_package_json(target / "package.json")
  existing = set(package_json.get("dependencies", {}).keys()) | set(package_json.get("devDependencies", {}).keys())
  missing = [pkg for pkg in desired if pkg not in existing]
  if not missing:
    return

  log(f"Installing missing dependencies: {', '.join(missing)}")
  install_commands = {
    "npm": ["npm", "install", *missing],
    "yarn": ["yarn", "add", *missing],
    "pnpm": ["pnpm", "add", *missing],
    "bun": ["bun", "add", *missing],
  }
  run(install_commands[package_manager], cwd=target)


def add_package_script(target: Path, name: str, value: str) -> None:
  package_json_path = target / "package.json"
  package_json = load_package_json(package_json_path)
  scripts = package_json.setdefault("scripts", {})
  if name not in scripts:
    scripts[name] = value
    write_package_json(package_json_path, package_json)


def regenerate_prisma_client(target: Path) -> None:
  schema_path = target / "prisma" / "schema.prisma"
  if not schema_path.exists():
    return

  log("Regenerating Prisma client")
  run(["npx", "prisma", "generate"], cwd=target)


def write_env_example(target: Path, args: argparse.Namespace, features: set[str]) -> None:
  env_path = target / ".env.example"
  base_block = BASE_ENV_TEMPLATE.format(
    scopes=args.scopes,
    app_url=args.app_url or "https://example.ngrok-free.app",
    app_name=args.app_name,
    support_email=args.support_email,
  )
  upsert_env_block(env_path, "base", base_block)

  if args.database_mode == "postgres_prisma":
    upsert_env_block(env_path, "postgres_prisma", CORE_POSTGRES_ENV_BLOCK)

  if "merchant-comms" in features:
    upsert_env_block(
      env_path,
      "merchant_comms",
      MERCHANT_COMMS_ENV_BLOCK_TEMPLATE.format(app_store_url=args.app_store_url or ""),
    )


def write_scaffold_manifest(target: Path, args: argparse.Namespace, features: set[str], installed: str | None, latest: str | None) -> None:
  manifest_path = target / ".codex-shopify-scaffold.json"
  manifest = {
    "appName": args.app_name,
    "supportEmail": args.support_email,
    "databaseMode": args.database_mode,
    "features": sorted(features),
    "template": args.template,
    "language": args.language,
    "packageManager": args.package_manager,
    "clientIdLinked": bool(args.client_id),
    "shopifyCliInstalled": installed,
    "shopifyCliLatest": latest,
  }
  manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def apply_core_postgres_overlay(target: Path) -> None:
  src = OVERLAYS_DIR / "core"
  copy_tree(src, target)
  script_path = target / "scripts" / "prisma-setup.sh"
  if script_path.exists():
    script_path.chmod(script_path.stat().st_mode | stat.S_IXUSR)
  add_package_script(target, "prisma:setup", "./scripts/prisma-setup.sh")


def apply_overlay(target: Path, name: str) -> None:
  src = OVERLAYS_DIR / name
  if not src.exists():
    die(f"Missing overlay directory: {src}")
  if not any(path.is_file() for path in src.rglob("*")):
    die(
      f"Feature '{name}' is reserved in the skill, but its bundled overlay is not implemented yet: {src}"
    )
  copy_tree(src, target)


def parse_features(raw: str) -> set[str]:
  features = {item.strip() for item in raw.split(",") if item.strip()}
  unknown = sorted(features - SUPPORTED_FEATURES)
  if unknown:
    die(f"Unknown feature(s): {', '.join(unknown)}")
  return features


def main() -> None:
  parser = argparse.ArgumentParser(description="Scaffold a new Shopify app and apply reusable overlays.")
  parser.add_argument("--app-name", required=True)
  parser.add_argument("--path", required=True)
  parser.add_argument("--support-email", required=True)
  parser.add_argument("--scopes", default="write_products")
  parser.add_argument("--database-mode", choices=["sqlite_local", "postgres_prisma"], default="postgres_prisma")
  parser.add_argument("--features", default="merchant-comms,review-prompts")
  parser.add_argument("--package-manager", default="npm", choices=["npm", "yarn", "pnpm", "bun"])
  parser.add_argument("--template", default="reactRouter")
  parser.add_argument("--language", default="typescript", choices=["typescript", "javascript"])
  parser.add_argument("--client-id")
  parser.add_argument("--app-url")
  parser.add_argument("--app-store-url")
  parser.add_argument("--skip-init", action="store_true")
  parser.add_argument("--no-install", action="store_true")
  args = parser.parse_args()

  requested_target = Path(args.path).expanduser().resolve()
  features = parse_features(args.features)
  installed, latest = detect_shopify_version()

  if installed:
    log(f"Installed Shopify CLI: {installed}")
  if latest and installed and latest != installed:
    log(f"Latest published Shopify CLI: {latest} (not auto-upgrading)")

  ensure_target_ready(requested_target, args.skip_init)
  if args.skip_init:
    validate_existing_target(requested_target)
  scaffold_base_app(args, requested_target)

  target = requested_target if args.skip_init else resolve_project_root(requested_target, args.app_name)
  if target != requested_target:
    log(f"Shopify CLI scaffolded into nested app directory: {target}")
    target = collapse_nested_project_root(requested_target, target)

  if args.database_mode == "postgres_prisma":
    apply_core_postgres_overlay(target)
    configure_postgres_prisma_schema(target / "prisma" / "schema.prisma")

  write_env_example(target, args, features)
  env_example_tracked = ensure_env_example_tracked(target)
  manifest_changed = harden_package_manifest(target)
  npmrc_changed = normalize_npmrc(target, args.package_manager)
  if env_example_tracked:
    log("Updated .gitignore so .env.example stays commitable")
  if manifest_changed:
    log("Applied scaffold package hardening for audit-safe defaults")
  if npmrc_changed:
    log("Removed pnpm-only npmrc flags that trigger npm warnings")

  prisma_schema = target / "prisma" / "schema.prisma"
  dependency_list: list[str] = []
  if "merchant-comms" in features:
    apply_overlay(target, "merchant-comms")
    append_prisma_block(prisma_schema, "ShopCommsPreferences", MERCHANT_COMMS_PRISMA_BLOCK)
    dependency_list.append("@sendgrid/mail")

  if "review-prompts" in features:
    apply_overlay(target, "review-prompts")
    append_prisma_block(prisma_schema, "ShopReviewState", REVIEW_PROMPTS_PRISMA_BLOCK)
    dependency_list.extend(["@shopify/app-bridge-react", "@shopify/polaris"])

  if "billing-stub" in features:
    apply_overlay(target, "billing-stub")

  if "app-proxy" in features:
    apply_overlay(target, "app-proxy")

  if "theme-extension" in features:
    apply_overlay(target, "theme-extension")

  if args.no_install:
    log("Skipping dependency installation because --no-install was provided")
  else:
    install_missing_dependencies(target, args.package_manager, dependency_list)
    if manifest_changed:
      log("Refreshing dependencies after package hardening")
      install_project_dependencies(target, args.package_manager)
    if prisma_schema.exists():
      regenerate_prisma_client(target)
  write_scaffold_manifest(target, args, features, installed, latest)

  log("Scaffold complete")
  log(f"Next: cd {target}")
  log("Recommended follow-up: inspect .codex-shopify-scaffold.json and integrate milestones/settings routes")


if __name__ == "__main__":
  main()
