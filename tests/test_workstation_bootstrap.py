import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "workstation_bootstrap.py"


class WorkstationBootstrapTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.codex_home = self.root / "codex-home"
        (self.repo / "templates").mkdir(parents=True)
        (self.repo / "skills" / "alpha").mkdir(parents=True)
        (self.codex_home / "skills" / "alpha").mkdir(parents=True)
        (self.repo / "templates" / "global-AGENTS.md").write_text(
            "# Canonical policy\n", encoding="utf-8"
        )
        (self.repo / "skills" / "alpha" / "SKILL.md").write_text(
            "canonical skill\n", encoding="utf-8"
        )
        (self.codex_home / "AGENTS.md").write_text("old policy\n", encoding="utf-8")
        (self.codex_home / "skills" / "alpha" / "SKILL.md").write_text(
            "old skill\n", encoding="utf-8"
        )
        self.manifest = self.repo / "workstation-baseline.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "globalPolicy": "templates/global-AGENTS.md",
                    "standaloneSkills": [{"name": "alpha", "source": "skills/alpha"}],
                    "plugins": [],
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_bootstrap(self, apply: bool) -> subprocess.CompletedProcess:
        command = [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(self.repo),
            "--codex-home",
            str(self.codex_home),
            "--manifest",
            str(self.manifest),
            "--skip-plugins",
        ]
        if apply:
            command.append("--apply")
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_preview_does_not_change_installed_files(self) -> None:
        result = self.run_bootstrap(apply=False)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.codex_home / "AGENTS.md").read_text(), "old policy\n")
        self.assertEqual(
            (self.codex_home / "skills" / "alpha" / "SKILL.md").read_text(),
            "old skill\n",
        )

    def test_apply_installs_exact_files_and_preserves_backup(self) -> None:
        result = self.run_bootstrap(apply=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.codex_home / "AGENTS.md").read_text(), "# Canonical policy\n")
        self.assertEqual(
            (self.codex_home / "skills" / "alpha" / "SKILL.md").read_text(),
            "canonical skill\n",
        )
        backups = list((self.codex_home / "backups" / "workstation-bootstrap").glob("*/AGENTS.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "old policy\n")
        skill_backups = list(
            (self.codex_home / "backups" / "workstation-bootstrap").glob("*/skills/alpha/SKILL.md")
        )
        self.assertEqual(len(skill_backups), 1)
        self.assertEqual(skill_backups[0].read_text(), "old skill\n")
        self.assertEqual((self.codex_home / "AGENTS.md").stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
