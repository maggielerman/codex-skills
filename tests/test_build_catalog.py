import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "build_catalog.py"


class BuildCatalogTest(unittest.TestCase):
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
