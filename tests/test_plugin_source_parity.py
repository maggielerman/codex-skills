import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class PluginSourceParityTest(unittest.TestCase):
    def test_rps_visual_guardrails_match_marketplace_package(self) -> None:
        standalone = (
            REPO_ROOT
            / "skills"
            / "rps-wall-art-mockup-workflow"
            / "references"
            / "visual-guardrails.md"
        )
        packaged = (
            REPO_ROOT
            / "plugins"
            / "rps-etsy-ops"
            / "skills"
            / "rps-wall-art-mockup-workflow"
            / "references"
            / "visual-guardrails.md"
        )

        self.assertEqual(
            packaged.read_bytes(),
            standalone.read_bytes(),
            "The installed RPS marketplace package must carry the canonical visual guardrails.",
        )


if __name__ == "__main__":
    unittest.main()
