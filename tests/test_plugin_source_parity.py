import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class PluginSourceParityTest(unittest.TestCase):
    def test_portable_skills_do_not_embed_a_workstation_home(self) -> None:
        required_skills = [
            "hyphenomenon-chat-intake",
            "hyphenomenon-project-intake",
            "rps-print-order",
            "rps-etsy-shop-uploader-listing-workflow",
            "shopify-app-scaffold",
            "user-journey-audit",
            "ux-ui-bug-intake",
            "visual-design-critique",
            "rps-wall-art-mockup-workflow",
        ]

        violations = []
        for skill_name in required_skills:
            for path in (REPO_ROOT / "skills" / skill_name).rglob("*"):
                if not path.is_file():
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if "/Users/" in text:
                    violations.append(str(path.relative_to(REPO_ROOT)))

        self.assertEqual(
            violations,
            [],
            "Portable skills must resolve host paths at runtime.",
        )

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
