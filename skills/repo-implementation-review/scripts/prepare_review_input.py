#!/usr/bin/env python3
"""Prepare structured input for a multi-repo implementation review."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import time
from contextlib import suppress
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".next",
    ".turbo",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".hpp": "C/C++",
    ".scala": "Scala",
    ".sh": "Shell",
    ".sql": "SQL",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "CSS",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".clj": "Clojure",
    ".tf": "Terraform",
    ".yaml": "YAML",
    ".yml": "YAML",
}

MANIFEST_FILES = [
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "Pipfile",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "Gemfile",
    "composer.json",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
]

SCORE_FIELDS = [
    "correctness",
    "architecture",
    "maintainability",
    "testing",
    "performance",
    "security",
    "delivery_readiness",
]

TEST_DIR_PATTERN = re.compile(r"^(test|tests|spec|specs|__tests__|e2e)$", re.IGNORECASE)
PLACEHOLDER_DOC_PATTERNS = [
    re.compile(r"add feature overviews here", re.IGNORECASE),
    re.compile(r"todo", re.IGNORECASE),
    re.compile(r"tbd", re.IGNORECASE),
]

EXPRESS_ROUTE_PATTERN = re.compile(
    r"""(?:app|router)\s*\.\s*(get|post|put|patch|delete)\s*\(\s*["'](/[^"']*)["']""",
    re.IGNORECASE,
)
FASTAPI_ROUTE_PATTERN = re.compile(
    r"""@\w+\.(get|post|put|patch|delete)\s*\(\s*["'](/[^"']*)["']""",
    re.IGNORECASE,
)


def parse_repo_arg(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise ValueError(
            f"Invalid --repo value '{raw}'. Use format 'Label=/absolute/or/relative/path'."
        )

    label, path_text = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError(f"Invalid --repo value '{raw}'. Label cannot be empty.")

    path = Path(path_text.strip()).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Repository path does not exist or is not a directory: {path}")

    return label, path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "repo"


def detect_test_directories(repo_path: Path) -> list[str]:
    test_dirs: set[str] = set()
    for root, dirs, _files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel_root = Path(root).relative_to(repo_path)
        for directory in dirs:
            if TEST_DIR_PATTERN.match(directory):
                rel = (rel_root / directory).as_posix()
                test_dirs.add(rel)
    return sorted(test_dirs)


def collect_language_counts(repo_path: Path) -> tuple[int, int, list[dict[str, object]]]:
    total_files = 0
    source_files = 0
    counts: Counter[str] = Counter()

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file_name in files:
            total_files += 1
            suffix = Path(file_name).suffix.lower()
            language = LANGUAGE_BY_EXTENSION.get(suffix)
            if language:
                source_files += 1
                counts[language] += 1

    top_languages = [
        {"language": language, "files": file_count}
        for language, file_count in counts.most_common(6)
    ]

    return total_files, source_files, top_languages


def detect_manifests(repo_path: Path) -> list[str]:
    found = []
    for manifest in MANIFEST_FILES:
        if (repo_path / manifest).exists():
            found.append(manifest)
    return found


def detect_key_files(repo_path: Path, test_dirs: list[str]) -> dict[str, bool]:
    return {
        "README.md": (repo_path / "README.md").exists(),
        "LICENSE": (repo_path / "LICENSE").exists() or (repo_path / "LICENSE.md").exists(),
        "Dockerfile": (repo_path / "Dockerfile").exists(),
        ".github/workflows": (repo_path / ".github" / "workflows").exists(),
        "tests": bool(test_dirs),
    }


def read_text_safely(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        with suppress(Exception):
            return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    return ""


def infer_stated_goal(repo_path: Path) -> str:
    readme = repo_path / "README.md"
    if not readme.exists():
        return ""

    text = read_text_safely(readme)
    if not text.strip():
        return ""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    non_title = [line for line in lines if not line.startswith("#")]
    if not non_title:
        return ""
    for line in non_title:
        normalized = line.strip()
        lowered = normalized.lower()
        if normalized.startswith(("-", "*")):
            continue
        if lowered.startswith("docs index") or lowered.startswith("documentation"):
            continue
        if lowered.startswith("vitepress") or lowered.startswith("commands"):
            continue
        if "`" in normalized and ":" in normalized:
            continue
        if len(normalized.split()) < 4:
            continue
        return normalized[:240]
    return non_title[0][:240]


def load_package_scripts(repo_path: Path) -> dict[str, str]:
    package_json = repo_path / "package.json"
    if not package_json.exists():
        return {}

    try:
        data = json.loads(read_text_safely(package_json))
    except json.JSONDecodeError:
        return {}

    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}

    normalized = {}
    for key, value in scripts.items():
        if isinstance(value, str):
            normalized[str(key)] = value
    return normalized


def run_command(command: list[str], cwd: Path, timeout_seconds: int) -> tuple[int | None, float, str]:
    started = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration = round(time.time() - started, 2)
        output = "\n".join(
            part.strip()
            for part in [result.stdout, result.stderr]
            if isinstance(part, str) and part.strip()
        ).strip()
        if not output:
            output = "No command output."
        return result.returncode, duration, output[:3000]
    except subprocess.TimeoutExpired:
        duration = round(time.time() - started, 2)
        return None, duration, f"Timed out after {timeout_seconds}s."
    except Exception as exc:
        duration = round(time.time() - started, 2)
        return None, duration, f"Failed to execute command: {exc}"


def build_check_record(
    name: str,
    check_type: str,
    command: list[str],
    cwd: Path,
    timeout_seconds: int,
    skip_reason: str | None = None,
) -> dict[str, object]:
    rendered_command = " ".join(command)
    if skip_reason:
        return {
            "name": name,
            "type": check_type,
            "command": rendered_command,
            "status": "skip",
            "duration_seconds": 0,
            "details": skip_reason,
        }

    code, duration, output = run_command(command, cwd=cwd, timeout_seconds=timeout_seconds)
    status = "pass" if code == 0 else "fail"
    details = output if code is not None else output
    return {
        "name": name,
        "type": check_type,
        "command": rendered_command,
        "status": status,
        "exit_code": code,
        "duration_seconds": duration,
        "details": details,
    }


def collect_docs_review(repo_path: Path) -> dict[str, object]:
    readme = repo_path / "README.md"
    docs_dirs = [repo_path / "DOCS", repo_path / "docs"]
    docs_dir = next((path for path in docs_dirs if path.exists() and path.is_dir()), None)
    docs_index_candidates = [
        repo_path / "DOCS" / "index.md",
        repo_path / "DOCS" / "README.md",
        repo_path / "docs" / "index.md",
        repo_path / "docs" / "README.md",
    ]
    docs_site = repo_path / "docs-site"

    key_docs: list[str] = []
    if readme.exists():
        key_docs.append("README.md")
    if docs_dir:
        key_docs.append(docs_dir.relative_to(repo_path).as_posix())
    for path in docs_index_candidates:
        if path.exists():
            key_docs.append(path.relative_to(repo_path).as_posix())
            break
    if docs_site.exists() and docs_site.is_dir():
        key_docs.append("docs-site/")

    placeholder_hits: list[str] = []
    if docs_dir:
        for root, _dirs, files in os.walk(docs_dir):
            for file_name in files:
                if not file_name.endswith(".md"):
                    continue
                path = Path(root) / file_name
                text = read_text_safely(path)
                for pattern in PLACEHOLDER_DOC_PATTERNS:
                    if pattern.search(text):
                        placeholder_hits.append(path.relative_to(repo_path).as_posix())
                        break

    score = 1
    if readme.exists():
        score += 1
    if docs_dir:
        score += 1
    if any(path.exists() for path in docs_index_candidates):
        score += 1
    if docs_site.exists() and docs_site.is_dir():
        score += 1
    if placeholder_hits:
        score -= 1
    score = max(1, min(score, 5))

    if score >= 4:
        coverage = "high"
    elif score == 3:
        coverage = "medium"
    else:
        coverage = "low"

    gaps: list[str] = []
    if not readme.exists():
        gaps.append("Missing README.md for onboarding context.")
    if not docs_dir:
        gaps.append("Missing dedicated docs directory (`DOCS/` or `docs/`).")
    if not any(path.exists() for path in docs_index_candidates):
        gaps.append("Missing docs index page (`DOCS/index.md` or equivalent).")
    if placeholder_hits:
        sample = ", ".join(placeholder_hits[:4])
        gaps.append(f"Placeholder docs content detected: {sample}")

    return {
        "coverage": coverage,
        "quality_score": score,
        "key_docs": key_docs,
        "gaps": gaps,
    }


def discover_endpoints(repo_path: Path) -> list[dict[str, str]]:
    endpoints: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    source_exts = {".ts", ".tsx", ".js", ".jsx", ".py"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file_name in files:
            path = Path(root) / file_name
            if path.suffix.lower() not in source_exts:
                continue
            text = read_text_safely(path)
            if not text:
                continue

            rel = path.relative_to(repo_path).as_posix()
            for pattern in (EXPRESS_ROUTE_PATTERN, FASTAPI_ROUTE_PATTERN):
                for method, endpoint in pattern.findall(text):
                    if not endpoint.startswith("/"):
                        continue
                    key = (method.upper(), endpoint, rel)
                    if key in seen:
                        continue
                    seen.add(key)
                    endpoints.append(
                        {
                            "method": method.upper(),
                            "endpoint": endpoint,
                            "source": rel,
                            "status": "discovered",
                            "details": "Discovered from source code.",
                        }
                    )

    endpoints.sort(key=lambda item: (item["endpoint"], item["method"], item["source"]))
    return endpoints[:40]


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def probe_http(url: str) -> tuple[str, str]:
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=4) as resp:
            code = getattr(resp, "status", 200)
            return ("pass", f"HTTP {code}")
    except error.HTTPError as exc:
        if 400 <= exc.code < 500:
            return ("pass", f"HTTP {exc.code}")
        return ("fail", f"HTTP {exc.code}")
    except Exception as exc:
        return ("fail", str(exc))


def runtime_endpoint_probe(
    repo_path: Path,
    package_scripts: dict[str, str],
    discovered_endpoints: list[dict[str, str]],
    timeout_seconds: int,
    runtime_port: int,
) -> list[dict[str, str]]:
    if shutil.which("npm") is None:
        return [
            {
                "method": "GET",
                "endpoint": "/",
                "source": "runtime-probe",
                "status": "skip",
                "details": "npm not found; cannot run Node endpoint probes.",
            }
        ]

    if not (repo_path / "node_modules").exists():
        return [
            {
                "method": "GET",
                "endpoint": "/",
                "source": "runtime-probe",
                "status": "skip",
                "details": "node_modules missing; run install before runtime endpoint probing.",
            }
        ]

    start_script = None
    for candidate in ["start", "dev"]:
        if candidate in package_scripts:
            start_script = candidate
            break

    if not start_script:
        return [
            {
                "method": "GET",
                "endpoint": "/",
                "source": "runtime-probe",
                "status": "skip",
                "details": "No npm start/dev script detected for runtime endpoint probing.",
            }
        ]

    command = ["npm", "run", start_script]
    env = os.environ.copy()
    env["PORT"] = str(runtime_port)
    env.setdefault("NODE_ENV", "test")

    process = subprocess.Popen(
        command,
        cwd=str(repo_path),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    started = time.time()
    ready = False
    while time.time() - started < min(timeout_seconds, 30):
        if process.poll() is not None:
            break
        if is_port_open(runtime_port):
            ready = True
            break
        time.sleep(0.5)

    defaults = ["/health", "/api/health", "/"]
    dynamic = []
    for endpoint in discovered_endpoints:
        if endpoint.get("method") != "GET":
            continue
        path = endpoint.get("endpoint", "")
        if ":" in path or "{" in path:
            continue
        dynamic.append(path)

    probe_paths: list[str] = []
    for path in defaults + dynamic:
        if path not in probe_paths:
            probe_paths.append(path)
        if len(probe_paths) >= 10:
            break

    results: list[dict[str, str]] = []
    if not ready:
        details = "Service failed to start for runtime probe."
        try:
            out, err = process.communicate(timeout=5)
            combined = "\n".join(part for part in [out, err] if part).strip()
            if combined:
                details = (combined[:1800]).strip()
        except Exception:
            pass
        finally:
            if process.poll() is None:
                with suppress(Exception):
                    process.terminate()
                with suppress(Exception):
                    process.wait(timeout=3)
                if process.poll() is None:
                    with suppress(Exception):
                        process.kill()

        return [
            {
                "method": "GET",
                "endpoint": "/",
                "source": "runtime-probe",
                "status": "fail",
                "details": details,
            }
        ]

    base_url = f"http://127.0.0.1:{runtime_port}"
    for path in probe_paths:
        status, details = probe_http(base_url + path)
        results.append(
            {
                "method": "GET",
                "endpoint": path,
                "source": "runtime-probe",
                "status": status,
                "details": details,
            }
        )

    if process.poll() is None:
        with suppress(Exception):
            process.terminate()
        with suppress(Exception):
            process.wait(timeout=5)
        if process.poll() is None:
            with suppress(Exception):
                process.kill()

    return results


def collect_checks(
    repo_path: Path,
    package_scripts: dict[str, str],
    timeout_seconds: int,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    has_npm = shutil.which("npm") is not None
    has_python = shutil.which("python3") is not None
    has_node_modules = (repo_path / "node_modules").exists()
    tests_dir = (repo_path / "tests").exists()

    if package_scripts:
        if "check" in package_scripts:
            checks.append(
                build_check_record(
                    "Node typecheck/check",
                    "quality",
                    ["npm", "run", "check"],
                    cwd=repo_path,
                    timeout_seconds=timeout_seconds,
                    skip_reason=None if (has_npm and has_node_modules) else "npm or node_modules missing.",
                )
            )
        if "test" in package_scripts:
            checks.append(
                build_check_record(
                    "Node test suite",
                    "test",
                    ["npm", "run", "test"],
                    cwd=repo_path,
                    timeout_seconds=timeout_seconds,
                    skip_reason=None if (has_npm and has_node_modules) else "npm or node_modules missing.",
                )
            )
        if "build" in package_scripts:
            checks.append(
                build_check_record(
                    "Node build",
                    "build",
                    ["npm", "run", "build"],
                    cwd=repo_path,
                    timeout_seconds=timeout_seconds,
                    skip_reason=None if (has_npm and has_node_modules) else "npm or node_modules missing.",
                )
            )

    if tests_dir:
        checks.append(
            build_check_record(
                "Python unittest discover",
                "test",
                ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                cwd=repo_path,
                timeout_seconds=timeout_seconds,
                skip_reason=None if has_python else "python3 not found.",
            )
        )

    if not checks:
        checks.append(
            {
                "name": "Automated checks",
                "type": "test",
                "command": "",
                "status": "skip",
                "duration_seconds": 0,
                "details": "No obvious automated check commands discovered.",
            }
        )

    return checks


def count_check_statuses(checks: list[dict[str, object]]) -> dict[str, int]:
    counts = {"pass": 0, "fail": 0, "skip": 0}
    for check in checks:
        status = str(check.get("status", "skip")).lower()
        if status not in counts:
            status = "skip"
        counts[status] += 1
    return counts


def build_repo_entry(
    repo_id: str,
    label: str,
    path: Path,
    repo_index: int,
    run_checks: bool,
    probe_runtime: bool,
    timeout_seconds: int,
    runtime_port: int,
) -> dict[str, object]:
    total_files, source_files, top_languages = collect_language_counts(path)
    test_dirs = detect_test_directories(path)
    manifests = detect_manifests(path)
    package_scripts = load_package_scripts(path)
    docs_review = collect_docs_review(path)
    discovered_endpoints = discover_endpoints(path)
    checks: list[dict[str, object]] = []
    endpoint_checks: list[dict[str, str]] = discovered_endpoints

    if run_checks:
        checks = collect_checks(path, package_scripts, timeout_seconds)
        if probe_runtime:
            runtime_port_for_repo = runtime_port + ((repo_index - 1) * 10)
            runtime_results = runtime_endpoint_probe(
                repo_path=path,
                package_scripts=package_scripts,
                discovered_endpoints=discovered_endpoints,
                timeout_seconds=timeout_seconds,
                runtime_port=runtime_port_for_repo,
            )
            endpoint_checks = discovered_endpoints + runtime_results
    else:
        checks = [
            {
                "name": "Automated checks",
                "type": "test",
                "command": "",
                "status": "skip",
                "duration_seconds": 0,
                "details": "Checks disabled via CLI flag.",
            }
        ]

    return {
        "id": repo_id,
        "name": label,
        "path": str(path),
        "auto_signals": {
            "total_files": total_files,
            "source_files": source_files,
            "top_languages": top_languages,
            "manifests": manifests,
            "key_files": detect_key_files(path, test_dirs),
            "test_directories": test_dirs,
        },
        "summary": "",
        "scores": {field: None for field in SCORE_FIELDS},
        "pros": [],
        "cons": [],
        "notable_features": [],
        "missing_features": [],
        "risks": [],
        "recommended_use_cases": [],
        "feature_status": {},
        "goal_alignment": {
            "stated_goal": infer_stated_goal(path),
            "success_assessment": "",
            "completion_score": None,
        },
        "verification": {
            "checks": checks,
            "endpoint_checks": endpoint_checks,
            "check_summary": count_check_statuses(checks),
            "docs_review": docs_review,
        },
    }


def build_document(
    project_name: str,
    repo_specs: list[tuple[str, Path]],
    run_checks: bool,
    probe_runtime: bool,
    timeout_seconds: int,
    runtime_port: int,
) -> dict[str, object]:
    used_ids: set[str] = set()
    repos = []

    for repo_index, (label, path) in enumerate(repo_specs, start=1):
        base_id = slugify(label)
        repo_id = base_id
        suffix = 2
        while repo_id in used_ids:
            repo_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(repo_id)

        repos.append(
            build_repo_entry(
                repo_id=repo_id,
                label=label,
                path=path,
                repo_index=repo_index,
                run_checks=run_checks,
                probe_runtime=probe_runtime,
                timeout_seconds=timeout_seconds,
                runtime_port=runtime_port,
            )
        )

    return {
        "project_name": project_name,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_count": len(repos),
        "repos": repos,
        "cross_repo_findings": [],
        "feature_matrix": [],
        "recommended_path": {
            "recommended_repo": "",
            "rationale": [],
            "hybrid_strategy": "",
            "next_steps": [],
        },
        "analysis_notes": "",
        "starting_goal": "",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a JSON scaffold for repo implementation review.")
    parser.add_argument("--project-name", required=True, help="Shared project idea name.")
    parser.add_argument(
        "--repo",
        action="append",
        required=True,
        help="Repo in format Label=/path/to/repo. Repeat 2 or 3 times.",
    )
    parser.add_argument(
        "--run-checks",
        dest="run_checks",
        action="store_true",
        default=True,
        help="Run discovered tests/build/quality checks when possible (default: enabled).",
    )
    parser.add_argument(
        "--skip-checks",
        dest="run_checks",
        action="store_false",
        help="Skip executing automated checks and only collect static signals.",
    )
    parser.add_argument(
        "--probe-runtime",
        dest="probe_runtime",
        action="store_true",
        default=True,
        help="Attempt runtime endpoint probes for Node repos when possible (default: enabled).",
    )
    parser.add_argument(
        "--skip-runtime-probe",
        dest="probe_runtime",
        action="store_false",
        help="Skip runtime endpoint probes.",
    )
    parser.add_argument(
        "--check-timeout-seconds",
        type=int,
        default=180,
        help="Per-command timeout for automated checks.",
    )
    parser.add_argument(
        "--runtime-port",
        type=int,
        default=5055,
        help="Base localhost port used for runtime endpoint probes.",
    )
    parser.add_argument("--output", required=True, help="Output JSON path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if len(args.repo) < 2 or len(args.repo) > 3:
        raise SystemExit("You must pass exactly 2 or 3 --repo values.")

    repo_specs = []
    for raw in args.repo:
        repo_specs.append(parse_repo_arg(raw))

    document = build_document(
        project_name=args.project_name,
        repo_specs=repo_specs,
        run_checks=bool(args.run_checks),
        probe_runtime=bool(args.probe_runtime),
        timeout_seconds=max(20, int(args.check_timeout_seconds)),
        runtime_port=max(1024, int(args.runtime_port)),
    )

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2) + "\n")

    print(f"[OK] Wrote scaffold: {output_path}")
    print("[OK] Next step: fill success_assessment/completion_score plus final findings/recommendation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
