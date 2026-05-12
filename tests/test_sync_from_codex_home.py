import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "sync_from_codex_home.sh"


class SyncFromCodexHomeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.codex_home = self.root / "codex-home"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "skills").mkdir(parents=True)
        (self.codex_home / "skills").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.repo / "scripts" / "sync_from_codex_home.sh")
        os.chmod(self.repo / "scripts" / "sync_from_codex_home.sh", 0o755)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_skill(self, root: Path, name: str, files: dict[str, str] | None = None) -> None:
        files = files or {"SKILL.md": f"---\nname: {name}\ndescription: Test skill.\n---\n"}
        skill_dir = root / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        for relative_path, content in files.items():
            path = skill_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def run_sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["CODEX_HOME"] = str(self.codex_home)
        return subprocess.run(
            [str(self.repo / "scripts" / "sync_from_codex_home.sh"), *args],
            cwd=self.repo,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_check_reports_all_missing_sources_without_writing(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text(
            "alpha\nbeta\n", encoding="utf-8"
        )
        self.write_skill(self.codex_home / "skills", "local-only")

        result = self.run_sync("--check")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing allowlisted source skills:", output)
        self.assertIn("alpha", output)
        self.assertIn("beta", output)
        self.assertIn("Local source skills not listed in suite:", output)
        self.assertIn("local-only", output)
        self.assertFalse((self.repo / "skills" / "local-only").exists())

    def test_sync_requires_prune_when_repo_has_stale_skill_files(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text("alpha\n", encoding="utf-8")
        self.write_skill(self.codex_home / "skills", "alpha", {"SKILL.md": "fresh\n"})
        self.write_skill(
            self.repo / "skills",
            "alpha",
            {"SKILL.md": "old\n", "references/old.md": "stale\n"},
        )

        result = self.run_sync()

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Stale repo-only files detected:", output)
        self.assertIn("alpha/references/old.md", output)
        self.assertEqual((self.repo / "skills" / "alpha" / "SKILL.md").read_text(), "old\n")

    def test_check_reports_changed_skill_files_without_writing(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text("alpha\n", encoding="utf-8")
        self.write_skill(self.codex_home / "skills", "alpha", {"SKILL.md": "fresh\n"})
        self.write_skill(self.repo / "skills", "alpha", {"SKILL.md": "old\n"})

        result = self.run_sync("--check")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Changed skill files detected:", output)
        self.assertIn("alpha/SKILL.md", output)
        self.assertEqual((self.repo / "skills" / "alpha" / "SKILL.md").read_text(), "old\n")

    def test_check_reports_source_only_skill_files_without_writing(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text("alpha\n", encoding="utf-8")
        self.write_skill(
            self.codex_home / "skills",
            "alpha",
            {"SKILL.md": "fresh\n", "references/new.md": "new\n"},
        )
        self.write_skill(self.repo / "skills", "alpha", {"SKILL.md": "fresh\n"})

        result = self.run_sync("--check")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Source-only skill files detected:", output)
        self.assertIn("alpha/references/new.md", output)
        self.assertFalse((self.repo / "skills" / "alpha" / "references" / "new.md").exists())

    def test_check_and_prune_stale_are_incompatible(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text("alpha\n", encoding="utf-8")
        self.write_skill(self.codex_home / "skills", "alpha", {"SKILL.md": "fresh\n"})
        self.write_skill(
            self.repo / "skills",
            "alpha",
            {"SKILL.md": "fresh\n", "references/old.md": "stale\n"},
        )

        result = self.run_sync("--check", "--prune-stale")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--check cannot be combined with --prune-stale", output)
        self.assertTrue((self.repo / "skills" / "alpha" / "references" / "old.md").exists())

    def test_include_system_check_is_rejected(self) -> None:
        result = self.run_sync("--include-system", "--check")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--include-system cannot be combined with --check", output)

    def test_include_system_prune_stale_is_rejected(self) -> None:
        result = self.run_sync("--include-system", "--prune-stale")

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--include-system cannot be combined with --prune-stale", output)

    def test_prune_stale_sync_deletes_repo_only_files(self) -> None:
        (self.repo / "skills" / "SUITE_SKILLS.txt").write_text("alpha\n", encoding="utf-8")
        self.write_skill(self.codex_home / "skills", "alpha", {"SKILL.md": "fresh\n"})
        self.write_skill(
            self.repo / "skills",
            "alpha",
            {"SKILL.md": "old\n", "references/old.md": "stale\n"},
        )

        result = self.run_sync("--prune-stale")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.repo / "skills" / "alpha" / "SKILL.md").read_text(), "fresh\n")
        self.assertFalse((self.repo / "skills" / "alpha" / "references" / "old.md").exists())


if __name__ == "__main__":
    unittest.main()
