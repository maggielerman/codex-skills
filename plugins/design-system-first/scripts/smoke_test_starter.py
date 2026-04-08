#!/usr/bin/env python3
"""Run local smoke tests for the design-system-first starter."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_SCRIPT = (
    PLUGIN_ROOT
    / "skills"
    / "design-system-starter"
    / "scripts"
    / "scaffold_design_system_first.py"
)

SCENARIOS = {
    "marketing-only": ("marketing-only", []),
    "app-shell": ("app-shell", []),
    "marketing-only+docs": ("marketing-only", ["docs"]),
    "app-shell+testing": ("app-shell", ["testing"]),
    "app-shell+docs+testing": ("app-shell", ["docs", "testing"]),
}


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        action="append",
        dest="scenarios",
        choices=sorted(SCENARIOS.keys()),
        help="Scenario(s) to run. Defaults to all.",
    )
    parser.add_argument(
        "--package-manager",
        default="npm",
        choices=["npm", "pnpm", "yarn", "bun"],
        help="Package manager to use for scaffolding.",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep the temporary projects instead of deleting them.",
    )
    args = parser.parse_args()

    scenarios = args.scenarios or list(SCENARIOS.keys())
    parent_dir = (
        Path(tempfile.mkdtemp(prefix="design-system-first-smoke-"))
        if args.keep_temp
        else Path(tempfile.mkdtemp(prefix="design-system-first-smoke-"))
    )
    print(f"Using temp root: {parent_dir}")

    try:
        for scenario_name in scenarios:
            mode, addons = SCENARIOS[scenario_name]
            target_dir = parent_dir / scenario_name.replace("+", "-")
            run(
                [
                    "python3",
                    str(SCAFFOLD_SCRIPT),
                    "--path",
                    str(target_dir),
                    "--mode",
                    mode,
                    "--package-manager",
                    args.package_manager,
                    *(
                        ["--addons", ",".join(addons)]
                        if addons
                        else []
                    ),
                ]
            )

            run(["npm", "run", "build"], cwd=target_dir)

            if "testing" in addons:
                run(["npm", "run", "test"], cwd=target_dir)
                run(["npx", "playwright", "install", "chromium"], cwd=target_dir)
                run(["npm", "run", "test:e2e"], cwd=target_dir)

        print("All smoke tests passed.")
        if args.keep_temp:
            print(f"Projects kept at: {parent_dir}")
        return 0
    finally:
        if not args.keep_temp:
            shutil.rmtree(parent_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
