import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "scaffold_shopify_app.py"
SPEC = importlib.util.spec_from_file_location("shopify_scaffold", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
  raise RuntimeError(f"Unable to load scaffold script from {SCRIPT_PATH}")

skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(skill)


def make_existing_app(target: Path) -> None:
  (target / "prisma").mkdir(parents=True, exist_ok=True)
  (target / "package.json").write_text(
    json.dumps(
      {
        "name": "fixture-app",
        "scripts": {},
        "dependencies": {},
        "devDependencies": {
          "@typescript-eslint/eslint-plugin": "^6.21.0",
          "@typescript-eslint/parser": "^6.21.0",
        },
        "overrides": {
          "p-map": "^4.0.0",
        },
      },
      indent=2,
    )
    + "\n"
  )
  (target / ".npmrc").write_text("engine-strict=true\nshamefully-hoist=true\n")
  (target / ".gitignore").write_text(".env\n.env.*\n")
  (target / "prisma" / "schema.prisma").write_text(
    """
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
""".lstrip()
  )


def make_sqlite_app(target: Path) -> None:
  (target / "prisma").mkdir(parents=True, exist_ok=True)
  (target / "package.json").write_text(
    json.dumps(
      {
        "name": "fixture-app",
        "scripts": {},
        "dependencies": {},
        "devDependencies": {
          "@typescript-eslint/eslint-plugin": "^6.21.0",
          "@typescript-eslint/parser": "^6.21.0",
        },
        "overrides": {
          "p-map": "^4.0.0",
        },
      },
      indent=2,
    )
    + "\n"
  )
  (target / ".npmrc").write_text("engine-strict=true\nshamefully-hoist=true\n")
  (target / ".gitignore").write_text(".env\n.env.*\n")
  (target / "prisma" / "schema.prisma").write_text(
    """
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = "file:dev.sqlite"
}
""".lstrip()
  )


class ShopifyAppScaffoldTests(unittest.TestCase):
  def test_resolve_project_root_handles_nested_slugged_directory(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      actual_root = target / "xyppy-scaffold-test"
      actual_root.mkdir(parents=True)
      make_existing_app(actual_root)
      (actual_root / "shopify.app.toml").write_text('name = "Xyppy Scaffold Test"\n')

      resolved = skill.resolve_project_root(target, "Xyppy Scaffold Test")

      self.assertEqual(resolved, actual_root)

  def test_collapse_nested_project_root_moves_app_to_requested_path(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      requested = Path(tmpdir)
      actual_root = requested / "xyppy-scaffold-test"
      actual_root.mkdir(parents=True)
      make_existing_app(actual_root)
      (actual_root / ".git").mkdir()
      (actual_root / "shopify.app.toml").write_text('name = "Xyppy Scaffold Test"\n')

      collapsed = skill.collapse_nested_project_root(requested, actual_root)

      self.assertEqual(collapsed, requested)
      self.assertTrue((requested / "package.json").exists())
      self.assertTrue((requested / ".git").exists())
      self.assertFalse(actual_root.exists())

  def test_parse_features_rejects_unknown_features(self) -> None:
    with self.assertRaises(SystemExit):
      skill.parse_features("merchant-comms,totally-made-up")

  def test_install_missing_dependencies_uses_selected_package_manager(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      with mock.patch.object(skill, "run") as run_mock:
        skill.install_missing_dependencies(target, "pnpm", ["@sendgrid/mail"])

      run_mock.assert_called_once_with(["pnpm", "add", "@sendgrid/mail"], cwd=target)

  def test_regenerate_prisma_client_runs_generate_in_target(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      with mock.patch.object(skill, "run") as run_mock:
        skill.regenerate_prisma_client(target)

      run_mock.assert_called_once_with(["npx", "prisma", "generate"], cwd=target)

  def test_harden_package_manifest_updates_versions_and_overrides(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      changed = skill.harden_package_manifest(target)

      self.assertTrue(changed)
      package_json = json.loads((target / "package.json").read_text())
      self.assertEqual(package_json["devDependencies"]["@typescript-eslint/eslint-plugin"], "^8.58.0")
      self.assertEqual(package_json["devDependencies"]["@typescript-eslint/parser"], "^8.58.0")
      self.assertEqual(package_json["overrides"]["@prisma/config"]["effect"], "3.20.0")
      self.assertEqual(
        package_json["overrides"]["@typescript-eslint/typescript-estree"]["minimatch"],
        "9.0.9",
      )

  def test_configure_postgres_prisma_schema_rewrites_sqlite_datasource(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_sqlite_app(target)

      changed = skill.configure_postgres_prisma_schema(target / "prisma" / "schema.prisma")

      self.assertTrue(changed)
      schema_text = (target / "prisma" / "schema.prisma").read_text()
      self.assertIn('provider  = "postgresql"', schema_text)
      self.assertIn('url       = env("DATABASE_URL")', schema_text)
      self.assertIn('directUrl = env("DIRECT_URL")', schema_text)

  def test_normalize_npmrc_removes_pnpm_only_flag_for_npm(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      changed = skill.normalize_npmrc(target, "npm")

      self.assertTrue(changed)
      self.assertEqual((target / ".npmrc").read_text(), "engine-strict=true\n")

  def test_ensure_env_example_tracked_adds_gitignore_exception(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)
      (target / ".gitignore").write_text(".env\n.env.*\n")

      changed = skill.ensure_env_example_tracked(target)

      self.assertTrue(changed)
      self.assertEqual((target / ".gitignore").read_text(), ".env\n.env.*\n!.env.example\n")

  def test_skip_init_scaffold_writes_expected_files_without_installing(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      argv = [
        str(SCRIPT_PATH),
        "--app-name",
        "Fixture App",
        "--path",
        str(target),
        "--support-email",
        "support@example.com",
        "--skip-init",
        "--no-install",
        "--features",
        "merchant-comms,review-prompts",
        "--database-mode",
        "postgres_prisma",
      ]

      with mock.patch.object(sys, "argv", argv):
        with mock.patch.object(skill, "detect_shopify_version", return_value=("3.86.1", "3.92.1")):
          skill.main()

      env_text = (target / ".env.example").read_text()
      self.assertIn("# --- base ---", env_text)
      self.assertIn("# --- postgres_prisma ---", env_text)
      self.assertIn("# --- merchant_comms ---", env_text)

      schema_text = (target / "prisma" / "schema.prisma").read_text()
      self.assertIn("model ShopCommsPreferences", schema_text)
      self.assertIn("model ShopReviewState", schema_text)

      package_json = json.loads((target / "package.json").read_text())
      self.assertEqual(package_json["scripts"]["prisma:setup"], "./scripts/prisma-setup.sh")
      self.assertEqual(package_json["devDependencies"]["@typescript-eslint/eslint-plugin"], "^8.58.0")
      self.assertEqual(package_json["devDependencies"]["@typescript-eslint/parser"], "^8.58.0")
      self.assertEqual(package_json["overrides"]["@prisma/config"]["effect"], "3.20.0")
      self.assertEqual(
        package_json["overrides"]["@typescript-eslint/typescript-estree"]["minimatch"],
        "9.0.9",
      )

      manifest = json.loads((target / ".codex-shopify-scaffold.json").read_text())
      self.assertEqual(manifest["features"], ["merchant-comms", "review-prompts"])
      self.assertEqual(manifest["shopifyCliInstalled"], "3.86.1")
      self.assertEqual(manifest["shopifyCliLatest"], "3.92.1")

      self.assertTrue((target / "app" / "routes" / "unsubscribe.tsx").exists())
      self.assertTrue((target / "app" / "routes" / "app.review-banner.tsx").exists())
      self.assertTrue((target / "scripts" / "prisma-setup.sh").exists())
      self.assertEqual((target / ".npmrc").read_text(), "engine-strict=true\n")
      self.assertIn("!.env.example", (target / ".gitignore").read_text())

  def test_reserved_feature_fails_fast_until_overlay_exists(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      target = Path(tmpdir)
      make_existing_app(target)

      argv = [
        str(SCRIPT_PATH),
        "--app-name",
        "Fixture App",
        "--path",
        str(target),
        "--support-email",
        "support@example.com",
        "--skip-init",
        "--no-install",
        "--features",
        "billing-stub",
      ]

      with mock.patch.object(sys, "argv", argv):
        with mock.patch.object(skill, "detect_shopify_version", return_value=("3.86.1", "3.92.1")):
          with self.assertRaises(SystemExit):
            skill.main()


if __name__ == "__main__":
  unittest.main()
