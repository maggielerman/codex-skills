import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "workstation_doctor.py"


class WorkstationDoctorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.codex_home = self.root / "codex-home"
        self.external_repo = self.root / "external-repo"
        self.installed_plugin = self.root / "installed-plugin"

        (self.repo / "templates").mkdir(parents=True)
        (self.repo / "skills" / "alpha").mkdir(parents=True)
        (self.external_repo / "plugins" / "sample" / ".codex-plugin").mkdir(parents=True)
        (self.codex_home / "skills" / "alpha").mkdir(parents=True)
        (self.installed_plugin / ".codex-plugin").mkdir(parents=True)

        policy = "# Test policy\n"
        skill = "---\nname: alpha\ndescription: Test.\n---\n"
        plugin = '{"name":"sample","version":"1.0.0"}\n'
        (self.repo / "templates" / "global-AGENTS.md").write_text(policy, encoding="utf-8")
        (self.codex_home / "AGENTS.md").write_text(policy, encoding="utf-8")
        (self.codex_home / "AGENTS.md").chmod(0o600)
        (self.repo / "skills" / "alpha" / "SKILL.md").write_text(skill, encoding="utf-8")
        (self.codex_home / "skills" / "alpha" / "SKILL.md").write_text(skill, encoding="utf-8")
        (self.external_repo / "plugins" / "sample" / ".codex-plugin" / "plugin.json").write_text(
            plugin, encoding="utf-8"
        )
        (self.installed_plugin / ".codex-plugin" / "plugin.json").write_text(
            plugin, encoding="utf-8"
        )

        self.manifest = self.repo / "workstation-baseline.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "globalPolicy": "templates/global-AGENTS.md",
                    "standaloneSkills": [{"name": "alpha", "source": "skills/alpha"}],
                    "plugins": [
                        {
                            "name": "sample",
                            "version": "1.0.0",
                            "sourceRoot": "external",
                            "source": "plugins/sample",
                            "enabled": True,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.host_overlay = self.root / "host-overlay.json"
        self.host_overlay.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "repositoryRoots": {"external": str(self.external_repo)},
                }
            ),
            encoding="utf-8",
        )
        self.plugin_state = self.root / "plugin-state.json"
        self.plugin_state.write_text(
            json.dumps(
                {
                    "installed": [
                        {
                            "name": "sample",
                            "version": "1.0.0",
                            "enabled": True,
                            "source": {"path": str(self.installed_plugin)},
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_doctor(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo-root",
                str(self.repo),
                "--codex-home",
                str(self.codex_home),
                "--manifest",
                str(self.manifest),
                "--plugin-state-json",
                str(self.plugin_state),
                "--host-overlay",
                str(self.host_overlay),
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_passes_when_policy_skill_and_plugin_match(self) -> None:
        result = self.run_doctor()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertTrue(all(check["status"] == "pass" for check in report["checks"]))

    def test_reports_drift_without_exposing_file_contents(self) -> None:
        secret_marker = "DO-NOT-PRINT-THIS-CONTENT"
        (self.codex_home / "skills" / "alpha" / "SKILL.md").write_text(
            secret_marker, encoding="utf-8"
        )

        result = self.run_doctor()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "drift")
        self.assertNotIn(secret_marker, result.stdout + result.stderr)
        self.assertTrue(
            any(check["name"] == "alpha" and check["status"] == "drift" for check in report["checks"])
        )

    def test_reports_global_policy_file_drift(self) -> None:
        (self.codex_home / "AGENTS.md").write_text("different policy\n", encoding="utf-8")

        result = self.run_doctor()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(
            any(
                check["kind"] == "global-policy" and check["status"] == "drift"
                for check in report["checks"]
            )
        )

    def test_reports_insecure_global_policy_permissions(self) -> None:
        (self.codex_home / "AGENTS.md").chmod(0o644)

        result = self.run_doctor()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(
            any(
                check["kind"] == "global-policy"
                and check["status"] == "drift"
                and check["actualMode"] == "644"
                for check in report["checks"]
            )
        )

    def test_reports_required_source_with_workstation_specific_home_path(self) -> None:
        absolute_path = "/Users/example-person/Documents/project"
        skill_path = self.repo / "skills" / "alpha" / "SKILL.md"
        installed_skill_path = self.codex_home / "skills" / "alpha" / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8") + f"\nRun from `{absolute_path}`.\n"
        skill_path.write_text(skill_text, encoding="utf-8")
        installed_skill_path.write_text(skill_text, encoding="utf-8")

        result = self.run_doctor()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertNotIn(absolute_path, result.stdout + result.stderr)
        self.assertTrue(
            any(
                check["kind"] == "portable-source"
                and check["name"] == "standalone-skill:alpha"
                and check["status"] == "drift"
                for check in report["checks"]
            )
        )

    def test_reports_missing_host_overlay_repository_root(self) -> None:
        missing = self.root / "missing-external-repo"
        self.host_overlay.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "repositoryRoots": {"external": str(missing)},
                }
            ),
            encoding="utf-8",
        )

        result = self.run_doctor()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(
            any(
                check["kind"] == "repository-root"
                and check["name"] == "external"
                and check["status"] == "drift"
                for check in report["checks"]
            )
        )


if __name__ == "__main__":
    unittest.main()
