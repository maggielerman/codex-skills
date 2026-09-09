import runpy
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "build_catalog.py"


class BuildCatalogTest(unittest.TestCase):
    def test_multiline_descriptions_preserve_content_and_colons(self) -> None:
        parse = runpy.run_path(str(SCRIPT))["parse_frontmatter"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            for indicator, expected in [("|", "First line\nUse when: setting up a store."), (">", "First line Use when: setting up a store.")]:
                with self.subTest(indicator=indicator):
                    path.write_text("---\nname: example\ndescription: " + indicator + "\n  First line\n  Use when: setting up a store.\n---\n", encoding="utf-8")
                    result = parse(path)
                    self.assertEqual(result["description"], expected)
                    self.assertEqual(set(result), {"name", "description"})

    def test_check_mode_runs_on_supported_workstation_python(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("No catalog drift detected.", result.stdout)


if __name__ == "__main__":
    unittest.main()
