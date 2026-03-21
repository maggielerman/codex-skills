#!/usr/bin/env python3
"""Build HTML/CSV/JSON artifacts for comparing 2-3 repository implementations."""

from __future__ import annotations

import argparse
import csv
import html
import json
import shutil
import subprocess
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from urllib.parse import quote

SCORE_FIELDS = [
    ("correctness", "Correctness"),
    ("architecture", "Architecture"),
    ("maintainability", "Maintainability"),
    ("testing", "Testing"),
    ("performance", "Performance"),
    ("security", "Security"),
    ("delivery_readiness", "Delivery Readiness"),
]

STATUS_CLASS = {
    "present": "status-present",
    "partial": "status-partial",
    "missing": "status-missing",
    "planned": "status-planned",
    "unknown": "status-unknown",
}

CHECK_STATUS_CLASS = {
    "pass": "check-pass",
    "fail": "check-fail",
    "skip": "check-skip",
    "discovered": "check-discovered",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build HTML/CSV/JSON report artifacts from review JSON input.")
    parser.add_argument("--input", required=True, help="Path to review JSON input file.")
    parser.add_argument("--output-dir", required=True, help="Directory where report artifacts are written.")
    parser.add_argument(
        "--pdf",
        choices=["auto", "always", "never"],
        default="auto",
        help="PDF generation mode via wkhtmltopdf.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def sanitize_text_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    cleaned = []
    for item in values:
        text = str(item).strip()
        if text:
            cleaned.append(text)
    return cleaned


def parse_score(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        numeric = float(value)
    elif isinstance(value, str):
        try:
            numeric = float(value.strip())
        except ValueError:
            return None
    else:
        return None

    if numeric < 1:
        numeric = 1.0
    if numeric > 5:
        numeric = 5.0
    return numeric


def normalize_status(value: object) -> str:
    if value is None:
        return "unknown"
    lowered = str(value).strip().lower()
    if lowered in STATUS_CLASS:
        return lowered
    if lowered in {"yes", "true", "done", "complete"}:
        return "present"
    if lowered in {"no", "false", "absent"}:
        return "missing"
    return "unknown"


def normalize_check_status(value: object) -> str:
    lowered = str(value or "").strip().lower()
    if lowered in CHECK_STATUS_CLASS:
        return lowered
    if lowered in {"ok", "success", "passed"}:
        return "pass"
    if lowered in {"error", "failed"}:
        return "fail"
    return "skip"


def parse_int_score(value: object) -> int | None:
    parsed = parse_score(value)
    if parsed is None:
        return None
    return int(round(parsed))


def parse_int(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except Exception:
        return default


def normalize_checks(raw_checks: object) -> list[dict]:
    if not isinstance(raw_checks, list):
        return []
    out = []
    for item in raw_checks:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "name": str(item.get("name", "Unnamed check")).strip() or "Unnamed check",
                "type": str(item.get("type", "check")).strip() or "check",
                "command": str(item.get("command", "")).strip(),
                "status": normalize_check_status(item.get("status")),
                "details": str(item.get("details", "")).strip(),
                "duration_seconds": item.get("duration_seconds"),
            }
        )
    return out


def normalize_endpoint_checks(raw_checks: object) -> list[dict]:
    if not isinstance(raw_checks, list):
        return []
    out = []
    for item in raw_checks:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "method": str(item.get("method", "GET")).strip().upper() or "GET",
                "endpoint": str(item.get("endpoint", "")).strip(),
                "source": str(item.get("source", "")).strip(),
                "status": normalize_check_status(item.get("status")),
                "details": str(item.get("details", "")).strip(),
            }
        )
    return out


def count_statuses(items: list[dict]) -> dict[str, int]:
    counts = {"pass": 0, "fail": 0, "skip": 0, "discovered": 0}
    for item in items:
        status = normalize_check_status(item.get("status"))
        counts[status] += 1
    return counts


def compute_overall_score(repo: dict) -> float | None:
    scores = repo.get("scores", {})
    if not isinstance(scores, dict):
        return None

    numeric_scores = []
    for field, _label in SCORE_FIELDS:
        numeric = parse_score(scores.get(field))
        if numeric is not None:
            numeric_scores.append(numeric)

    if not numeric_scores:
        return None

    return round(sum(numeric_scores) / len(numeric_scores), 2)


def normalize_repos(raw_repos: object) -> list[dict]:
    if not isinstance(raw_repos, list):
        raise SystemExit("Input must include a 'repos' array.")
    if len(raw_repos) < 2 or len(raw_repos) > 3:
        raise SystemExit("Input must include exactly 2 or 3 repositories in 'repos'.")

    repos: list[dict] = []
    seen_ids = set()

    for index, raw_repo in enumerate(raw_repos, start=1):
        if not isinstance(raw_repo, dict):
            raise SystemExit(f"Repo entry #{index} is not an object.")

        repo_id = str(raw_repo.get("id", "")).strip() or f"repo-{index}"
        if repo_id in seen_ids:
            raise SystemExit(f"Duplicate repo id detected: '{repo_id}'.")
        seen_ids.add(repo_id)

        name = str(raw_repo.get("name", repo_id)).strip() or repo_id
        path = str(raw_repo.get("path", "")).strip()
        implementation_label = f"Implementation {index}"

        auto_signals = raw_repo.get("auto_signals", {})
        if not isinstance(auto_signals, dict):
            auto_signals = {}

        scores_obj = raw_repo.get("scores", {})
        if not isinstance(scores_obj, dict):
            scores_obj = {}

        normalized_scores = {}
        for field, _label in SCORE_FIELDS:
            normalized_scores[field] = parse_score(scores_obj.get(field))

        feature_status = raw_repo.get("feature_status", {})
        if not isinstance(feature_status, dict):
            feature_status = {}

        goal_alignment = raw_repo.get("goal_alignment", {})
        if not isinstance(goal_alignment, dict):
            goal_alignment = {}

        verification = raw_repo.get("verification", {})
        if not isinstance(verification, dict):
            verification = {}

        docs_review = verification.get("docs_review", {})
        if not isinstance(docs_review, dict):
            docs_review = {}

        checks = normalize_checks(verification.get("checks", []))
        endpoint_checks = normalize_endpoint_checks(verification.get("endpoint_checks", []))
        check_summary = verification.get("check_summary", {})
        if not isinstance(check_summary, dict):
            check_summary = {}
        computed_check_summary = count_statuses(checks)
        normalized_check_summary = {
            "pass": parse_int(check_summary.get("pass", computed_check_summary["pass"]), default=0),
            "fail": parse_int(check_summary.get("fail", computed_check_summary["fail"]), default=0),
            "skip": parse_int(check_summary.get("skip", computed_check_summary["skip"]), default=0),
        }
        endpoint_summary = count_statuses(endpoint_checks)

        repos.append(
            {
                "implementation_index": index,
                "implementation_label": implementation_label,
                "id": repo_id,
                "name": name,
                "path": path,
                "auto_signals": auto_signals,
                "summary": str(raw_repo.get("summary", "")).strip(),
                "scores": normalized_scores,
                "overall_score": compute_overall_score({"scores": normalized_scores}),
                "pros": sanitize_text_list(raw_repo.get("pros", [])),
                "cons": sanitize_text_list(raw_repo.get("cons", [])),
                "notable_features": sanitize_text_list(raw_repo.get("notable_features", [])),
                "missing_features": sanitize_text_list(raw_repo.get("missing_features", [])),
                "risks": sanitize_text_list(raw_repo.get("risks", [])),
                "recommended_use_cases": sanitize_text_list(raw_repo.get("recommended_use_cases", [])),
                "feature_status": {
                    str(k).strip(): normalize_status(v)
                    for k, v in feature_status.items()
                    if str(k).strip()
                },
                "goal_alignment": {
                    "stated_goal": str(goal_alignment.get("stated_goal", "")).strip(),
                    "success_assessment": str(goal_alignment.get("success_assessment", "")).strip(),
                    "completion_score": parse_int_score(goal_alignment.get("completion_score")),
                },
                "verification": {
                    "checks": checks,
                    "endpoint_checks": endpoint_checks,
                    "check_summary": normalized_check_summary,
                    "endpoint_summary": endpoint_summary,
                    "docs_review": {
                        "coverage": str(docs_review.get("coverage", "unknown")).strip() or "unknown",
                        "quality_score": parse_int_score(docs_review.get("quality_score")),
                        "key_docs": sanitize_text_list(docs_review.get("key_docs", [])),
                        "gaps": sanitize_text_list(docs_review.get("gaps", [])),
                    },
                },
            }
        )

    return repos


def collect_feature_matrix(input_data: dict, repos: list[dict]) -> list[dict]:
    repo_ids = [repo["id"] for repo in repos]
    manual_matrix = input_data.get("feature_matrix", [])

    normalized_rows = []
    if isinstance(manual_matrix, list) and manual_matrix:
        for raw_row in manual_matrix:
            if not isinstance(raw_row, dict):
                continue
            feature = str(raw_row.get("feature", "")).strip()
            if not feature:
                continue

            statuses = {}
            for repo in repos:
                raw_status = raw_row.get(repo["id"])
                if raw_status is None:
                    raw_status = raw_row.get(repo["name"])
                if raw_status is None:
                    raw_status = raw_row.get(repo["implementation_label"])
                if raw_status is None:
                    raw_status = raw_row.get(f"{repo['implementation_label']}: {repo['name']}")
                statuses[repo["id"]] = normalize_status(raw_status)

            normalized_rows.append({"feature": feature, "statuses": statuses})

        if normalized_rows:
            return normalized_rows

    feature_key_to_name: dict[str, str] = {}

    for repo in repos:
        for feature in repo["feature_status"].keys():
            lowered = feature.lower()
            feature_key_to_name.setdefault(lowered, feature)
        for feature in repo["notable_features"]:
            lowered = feature.lower()
            feature_key_to_name.setdefault(lowered, feature)
        for feature in repo["missing_features"]:
            lowered = feature.lower()
            feature_key_to_name.setdefault(lowered, feature)

    for lowered, feature in sorted(feature_key_to_name.items(), key=lambda item: item[1].lower()):
        statuses = {}
        for repo in repos:
            explicit = None
            for key, status in repo["feature_status"].items():
                if key.lower() == lowered:
                    explicit = status
                    break

            if explicit:
                statuses[repo["id"]] = explicit
                continue

            notable_lower = {item.lower() for item in repo["notable_features"]}
            missing_lower = {item.lower() for item in repo["missing_features"]}

            if lowered in notable_lower:
                statuses[repo["id"]] = "present"
            elif lowered in missing_lower:
                statuses[repo["id"]] = "missing"
            else:
                statuses[repo["id"]] = "unknown"

        normalized_rows.append({"feature": feature, "statuses": statuses})

    return normalized_rows


def format_score(score: float | None) -> str:
    if score is None:
        return "n/a"
    return f"{score:.2f}"


def summarize_recommendation(input_data: dict, repos: list[dict]) -> dict:
    rec = input_data.get("recommended_path", {})
    if not isinstance(rec, dict):
        rec = {}

    recommended_repo = str(rec.get("recommended_repo", "")).strip()
    repo_lookup = {repo["id"]: repo for repo in repos}
    if recommended_repo and recommended_repo in repo_lookup:
        repo = repo_lookup[recommended_repo]
        recommended_label = f"{repo['implementation_label']}: {repo['name']} ({recommended_repo})"
    elif recommended_repo:
        recommended_label = recommended_repo
    else:
        recommended_label = "Not specified"

    return {
        "recommended_repo": recommended_label,
        "rationale": sanitize_text_list(rec.get("rationale", [])),
        "hybrid_strategy": str(rec.get("hybrid_strategy", "")).strip(),
        "next_steps": sanitize_text_list(rec.get("next_steps", [])),
    }


def build_csv_text(
    project_name: str,
    generated_at: str,
    starting_goal: str,
    repos: list[dict],
    feature_matrix: list[dict],
    recommendation: dict,
    cross_repo_findings: list[str],
) -> str:
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["section", "repo", "metric", "value"])

    writer.writerow(["meta", "all", "project_name", project_name])
    writer.writerow(["meta", "all", "generated_at_utc", generated_at])
    writer.writerow(["meta", "all", "starting_goal", starting_goal])

    for repo in repos:
        writer.writerow(["meta", repo["id"], "implementation_label", repo["implementation_label"]])
        writer.writerow(["meta", repo["id"], "repo_name", repo["name"]])
        writer.writerow(["meta", repo["id"], "repo_path", repo["path"]])
        writer.writerow(["meta", repo["id"], "goal_stated", repo["goal_alignment"]["stated_goal"]])
        writer.writerow(["meta", repo["id"], "goal_success_assessment", repo["goal_alignment"]["success_assessment"]])
        writer.writerow(
            ["meta", repo["id"], "goal_completion_score", repo["goal_alignment"]["completion_score"] or "n/a"]
        )
        docs_review = repo["verification"]["docs_review"]
        writer.writerow(["meta", repo["id"], "docs_coverage", docs_review["coverage"]])
        writer.writerow(["meta", repo["id"], "docs_quality_score", docs_review["quality_score"] or "n/a"])
        writer.writerow(["meta", repo["id"], "docs_key_docs", " | ".join(docs_review["key_docs"])])
        writer.writerow(["meta", repo["id"], "docs_gaps", " | ".join(docs_review["gaps"])])
        check_summary = repo["verification"]["check_summary"]
        endpoint_summary = repo["verification"]["endpoint_summary"]
        writer.writerow(["meta", repo["id"], "checks_pass", check_summary["pass"]])
        writer.writerow(["meta", repo["id"], "checks_fail", check_summary["fail"]])
        writer.writerow(["meta", repo["id"], "checks_skip", check_summary["skip"]])
        writer.writerow(["meta", repo["id"], "endpoint_pass", endpoint_summary["pass"]])
        writer.writerow(["meta", repo["id"], "endpoint_fail", endpoint_summary["fail"]])
        writer.writerow(["meta", repo["id"], "endpoint_skip", endpoint_summary["skip"]])
        writer.writerow(["meta", repo["id"], "endpoint_discovered", endpoint_summary["discovered"]])
        writer.writerow(["score", repo["id"], "overall", format_score(repo["overall_score"])])
        for field, label in SCORE_FIELDS:
            writer.writerow(["score", repo["id"], label, format_score(repo["scores"].get(field))])

        writer.writerow(["summary", repo["id"], "summary", repo["summary"]])
        writer.writerow(["list", repo["id"], "pros", " | ".join(repo["pros"])])
        writer.writerow(["list", repo["id"], "cons", " | ".join(repo["cons"])])
        writer.writerow(["list", repo["id"], "notable_features", " | ".join(repo["notable_features"])])
        writer.writerow(["list", repo["id"], "missing_features", " | ".join(repo["missing_features"])])
        writer.writerow(["list", repo["id"], "risks", " | ".join(repo["risks"])])
        for check in repo["verification"]["checks"]:
            writer.writerow(
                [
                    "check",
                    repo["id"],
                    check["name"],
                    f"{check['status']} | {check['type']} | {check['command']} | {check['details']}",
                ]
            )
        for endpoint in repo["verification"]["endpoint_checks"]:
            writer.writerow(
                [
                    "endpoint",
                    repo["id"],
                    f"{endpoint['method']} {endpoint['endpoint']}",
                    f"{endpoint['status']} | {endpoint['source']} | {endpoint['details']}",
                ]
            )

    for row in feature_matrix:
        feature = row["feature"]
        for repo in repos:
            status = row["statuses"].get(repo["id"], "unknown")
            writer.writerow(["feature", repo["id"], feature, status])

    for finding in cross_repo_findings:
        writer.writerow(["cross_repo", "all", "finding", finding])

    writer.writerow(["recommendation", "all", "recommended_repo", recommendation["recommended_repo"]])
    writer.writerow(["recommendation", "all", "hybrid_strategy", recommendation["hybrid_strategy"]])
    writer.writerow(["recommendation", "all", "rationale", " | ".join(recommendation["rationale"])])
    writer.writerow(["recommendation", "all", "next_steps", " | ".join(recommendation["next_steps"])])

    return buf.getvalue()


def render_list(items: list[str], empty_text: str = "None noted.") -> str:
    if not items:
        return f"<p class=\"empty\">{html.escape(empty_text)}</p>"
    parts = ["<ul>"]
    for item in items:
        parts.append(f"<li>{html.escape(item)}</li>")
    parts.append("</ul>")
    return "".join(parts)


def status_chip(status: str) -> str:
    css_class = STATUS_CLASS.get(status, "status-unknown")
    return f"<span class=\"chip {css_class}\">{html.escape(status.title())}</span>"


def check_chip(status: str) -> str:
    normalized = normalize_check_status(status)
    css_class = CHECK_STATUS_CLASS.get(normalized, "check-skip")
    return f"<span class=\"check-chip {css_class}\">{html.escape(normalized.title())}</span>"


def render_check_rows(checks: list[dict], empty_text: str, limit: int = 10) -> str:
    if not checks:
        return f"<p class=\"empty\">{html.escape(empty_text)}</p>"

    rows = []
    for check in checks[:limit]:
        command_text = check.get("command", "")
        if command_text:
            command_html = f"<code>{html.escape(str(command_text))}</code>"
        else:
            command_html = "<span class=\"empty\">n/a</span>"
        rows.append(
            "".join(
                [
                    "<tr>",
                    f"<td>{html.escape(str(check.get('name', 'Check')))}</td>",
                    f"<td>{check_chip(str(check.get('status', 'skip')))}</td>",
                    f"<td>{command_html}</td>",
                    f"<td>{html.escape(str(check.get('details', '')))}</td>",
                    "</tr>",
                ]
            )
        )

    return (
        "<table>"
        "<thead><tr><th>Check</th><th>Status</th><th>Command</th><th>Details</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )


def render_endpoint_rows(endpoints: list[dict], empty_text: str, limit: int = 12) -> str:
    if not endpoints:
        return f"<p class=\"empty\">{html.escape(empty_text)}</p>"

    rows = []
    for endpoint in endpoints[:limit]:
        rows.append(
            "".join(
                [
                    "<tr>",
                    f"<td><code>{html.escape(str(endpoint.get('method', 'GET')))} {html.escape(str(endpoint.get('endpoint', '/')))}</code></td>",
                    f"<td>{check_chip(str(endpoint.get('status', 'skip')))}</td>",
                    f"<td>{html.escape(str(endpoint.get('source', '')))}</td>",
                    f"<td>{html.escape(str(endpoint.get('details', '')))}</td>",
                    "</tr>",
                ]
            )
        )

    return (
        "<table>"
        "<thead><tr><th>Endpoint</th><th>Status</th><th>Source</th><th>Details</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )


def repo_file_link(path: str) -> str:
    cleaned = str(path).strip()
    if not cleaned:
        return "<span class=\"empty\">n/a</span>"
    href = "file://" + quote(cleaned, safe="/:")
    return f'<a href="{href}"><code>{html.escape(cleaned)}</code></a>'


def repo_header_html(repo: dict) -> str:
    return (
        f"<div><strong>{html.escape(repo['implementation_label'])}</strong></div>"
        f"<div>{html.escape(repo['name'])}</div>"
        f"<div class=\"mono\">{html.escape(repo['id'])}</div>"
    )


def render_auto_signals(repo: dict) -> str:
    signals = repo.get("auto_signals", {})
    if not isinstance(signals, dict):
        return "<p class=\"empty\">No auto signals.</p>"

    top_languages = signals.get("top_languages", [])
    if isinstance(top_languages, list):
        language_parts = []
        for entry in top_languages:
            if isinstance(entry, dict):
                language = str(entry.get("language", "")).strip()
                files = entry.get("files")
                if language:
                    language_parts.append(f"{language} ({files})")
        language_text = ", ".join(language_parts) if language_parts else "n/a"
    else:
        language_text = "n/a"

    manifests = signals.get("manifests", [])
    manifests_text = ", ".join(str(item) for item in manifests) if isinstance(manifests, list) else "n/a"

    key_files = signals.get("key_files", {})
    key_file_parts = []
    if isinstance(key_files, dict):
        for key, value in key_files.items():
            mark = "yes" if bool(value) else "no"
            key_file_parts.append(f"{key}: {mark}")
    key_files_text = ", ".join(key_file_parts) if key_file_parts else "n/a"

    test_dirs = signals.get("test_directories", [])
    test_dirs_text = ", ".join(str(item) for item in test_dirs) if isinstance(test_dirs, list) and test_dirs else "n/a"

    total_files = signals.get("total_files", "n/a")
    source_files = signals.get("source_files", "n/a")

    return (
        "<div class=\"signals\">"
        f"<div><strong>Total files:</strong> {html.escape(str(total_files))}</div>"
        f"<div><strong>Source files:</strong> {html.escape(str(source_files))}</div>"
        f"<div><strong>Top languages:</strong> {html.escape(language_text)}</div>"
        f"<div><strong>Manifests:</strong> {html.escape(manifests_text)}</div>"
        f"<div><strong>Key files:</strong> {html.escape(key_files_text)}</div>"
        f"<div><strong>Test directories:</strong> {html.escape(test_dirs_text)}</div>"
        "</div>"
    )


def build_html(
    project_name: str,
    generated_at: str,
    starting_goal: str,
    repos: list[dict],
    feature_matrix: list[dict],
    cross_repo_findings: list[str],
    recommendation: dict,
    csv_text: str,
    pdf_available: bool,
) -> str:
    repo_headers = "".join(f"<th>{repo_header_html(repo)}</th>" for repo in repos)
    empty_colspan = len(repos) + 1

    score_rows = []
    score_rows.append("<tr><th>Overall</th>" + "".join(f"<td>{format_score(repo['overall_score'])}</td>" for repo in repos) + "</tr>")
    for field, label in SCORE_FIELDS:
        row_cells = "".join(f"<td>{format_score(repo['scores'].get(field))}</td>" for repo in repos)
        score_rows.append(f"<tr><th>{html.escape(label)}</th>{row_cells}</tr>")

    verification_rows = [
        "<tr><th>Goal Completion (1-5)</th>"
        + "".join(f"<td>{format_score(repo['goal_alignment']['completion_score'])}</td>" for repo in repos)
        + "</tr>",
        "<tr><th>Docs Quality (1-5)</th>"
        + "".join(
            f"<td>{format_score(repo['verification']['docs_review']['quality_score'])}</td>" for repo in repos
        )
        + "</tr>",
        "<tr><th>Checks Passed</th>"
        + "".join(f"<td>{repo['verification']['check_summary']['pass']}</td>" for repo in repos)
        + "</tr>",
        "<tr><th>Checks Failed</th>"
        + "".join(f"<td>{repo['verification']['check_summary']['fail']}</td>" for repo in repos)
        + "</tr>",
        "<tr><th>Endpoint Probes Passed</th>"
        + "".join(f"<td>{repo['verification']['endpoint_summary']['pass']}</td>" for repo in repos)
        + "</tr>",
        "<tr><th>Endpoint Probes Failed</th>"
        + "".join(f"<td>{repo['verification']['endpoint_summary']['fail']}</td>" for repo in repos)
        + "</tr>",
    ]

    matrix_rows = []
    for row in feature_matrix:
        cells = []
        for repo in repos:
            status = row["statuses"].get(repo["id"], "unknown")
            cells.append(f"<td>{status_chip(status)}</td>")
        matrix_rows.append(f"<tr><th>{html.escape(row['feature'])}</th>{''.join(cells)}</tr>")

    side_by_side_cards = []
    for repo in repos:
        present = []
        partial = []
        planned = []
        missing = []
        unknown = []
        for row in feature_matrix:
            status = row["statuses"].get(repo["id"], "unknown")
            feature_name = row["feature"]
            if status == "present":
                present.append(feature_name)
            elif status == "partial":
                partial.append(feature_name)
            elif status == "planned":
                planned.append(feature_name)
            elif status == "missing":
                missing.append(feature_name)
            else:
                unknown.append(feature_name)

        side_by_side_cards.append(
            "".join(
                [
                    "<section class=\"feature-column\">",
                    f"<h3>{html.escape(repo['implementation_label'])}</h3>",
                    f"<p><strong>Repo:</strong> {html.escape(repo['name'])}</p>",
                    f"<p class=\"mono\">{html.escape(repo['id'])}</p>",
                    "<h4>Present</h4>",
                    render_list(present, "None identified."),
                    "<h4>Partial</h4>",
                    render_list(partial, "None identified."),
                    "<h4>Planned</h4>",
                    render_list(planned, "None identified."),
                    "<h4>Missing</h4>",
                    render_list(missing, "None identified."),
                    "<h4>Unknown</h4>",
                    render_list(unknown, "None identified."),
                    "</section>",
                ]
            )
        )

    mapping_rows = []
    for repo in repos:
        mapping_rows.append(
            "".join(
                [
                    "<tr>",
                    f"<td><strong>{html.escape(repo['implementation_label'])}</strong></td>",
                    f"<td>{html.escape(repo['name'])}</td>",
                    f"<td class=\"mono\">{html.escape(repo['id'])}</td>",
                    f"<td>{repo_file_link(repo['path'])}</td>",
                    "</tr>",
                ]
            )
        )

    repo_cards = []
    for repo in repos:
        repo_cards.append(
            "".join(
                [
                    "<section class=\"repo-card\">",
                    f"<h3>{html.escape(repo['implementation_label'])}</h3>",
                    f"<p><strong>Repo:</strong> {html.escape(repo['name'])}</p>",
                    f"<p class=\"mono\">{html.escape(repo['id'])}</p>",
                    f"<p><strong>Path:</strong> {repo_file_link(repo['path'])}</p>",
                    f"<p>{html.escape(repo['summary'] or 'No summary provided.')}</p>",
                    "<h4>Goal Fit</h4>",
                    f"<p><strong>Stated Goal:</strong> {html.escape(repo['goal_alignment']['stated_goal'] or 'Not captured')}</p>",
                    f"<p><strong>Success Assessment:</strong> {html.escape(repo['goal_alignment']['success_assessment'] or 'Not provided')}</p>",
                    f"<p><strong>Completion Score:</strong> {format_score(repo['goal_alignment']['completion_score'])}</p>",
                    "<h4>Auto Signals</h4>",
                    render_auto_signals(repo),
                    "<h4>Docs Review</h4>",
                    f"<p><strong>Coverage:</strong> {html.escape(repo['verification']['docs_review']['coverage'])}</p>",
                    f"<p><strong>Quality Score:</strong> {format_score(repo['verification']['docs_review']['quality_score'])}</p>",
                    "<p><strong>Key Docs:</strong></p>",
                    render_list(repo["verification"]["docs_review"]["key_docs"], "No key docs detected."),
                    "<p><strong>Doc Gaps:</strong></p>",
                    render_list(repo["verification"]["docs_review"]["gaps"], "No major doc gaps detected."),
                    "<h4>Verification Summary</h4>",
                    "<div class=\"signals\">",
                    f"<div><strong>Checks:</strong> pass {repo['verification']['check_summary']['pass']} | fail {repo['verification']['check_summary']['fail']} | skip {repo['verification']['check_summary']['skip']}</div>",
                    f"<div><strong>Endpoints:</strong> pass {repo['verification']['endpoint_summary']['pass']} | fail {repo['verification']['endpoint_summary']['fail']} | skip {repo['verification']['endpoint_summary']['skip']} | discovered {repo['verification']['endpoint_summary']['discovered']}</div>",
                    "</div>",
                    "<h4>Automated Checks</h4>",
                    render_check_rows(repo["verification"]["checks"], "No checks were recorded."),
                    "<h4>Endpoint Checks</h4>",
                    render_endpoint_rows(repo["verification"]["endpoint_checks"], "No endpoint checks were recorded."),
                    "<h4>Pros</h4>",
                    render_list(repo["pros"]),
                    "<h4>Cons</h4>",
                    render_list(repo["cons"]),
                    "<h4>Notable Features</h4>",
                    render_list(repo["notable_features"]),
                    "<h4>Missing Features</h4>",
                    render_list(repo["missing_features"]),
                    "<h4>Risks</h4>",
                    render_list(repo["risks"]),
                    "<h4>Recommended Use Cases</h4>",
                    render_list(repo["recommended_use_cases"]),
                    "</section>",
                ]
            )
        )

    csv_js = json.dumps(csv_text)
    findings_html = render_list(cross_repo_findings, "No cross-repo findings provided.")

    rationale_html = render_list(recommendation["rationale"], "No rationale provided.")
    next_steps_html = render_list(recommendation["next_steps"], "No next steps provided.")

    pdf_link = ""
    if pdf_available:
        pdf_link = '<a class="button" href="report.pdf" download>Download Generated PDF</a>'

    html_output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(project_name)} - Implementation Review</title>
  <style>
    :root {{
      --bg: #f5f7f2;
      --surface: #ffffff;
      --ink: #1f2933;
      --muted: #52606d;
      --line: #d9e2ec;
      --accent: #0f766e;
      --accent-2: #b45309;
      --ok: #166534;
      --warn: #92400e;
      --bad: #991b1b;
      --planned: #1d4ed8;
      --unknown: #475569;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: "Avenir Next", "Segoe UI", sans-serif; background: linear-gradient(160deg, #f5f7f2 0%, #eef2ff 100%); color: var(--ink); }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 28px 20px 64px; }}
    header {{ background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 20px; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); }}
    h1 {{ margin: 0 0 8px; font-size: clamp(1.5rem, 2.6vw, 2.2rem); }}
    .meta {{ color: var(--muted); margin: 0; }}
    .toolbar {{ margin-top: 16px; display: flex; flex-wrap: wrap; gap: 10px; }}
    .button {{ display: inline-block; border: none; text-decoration: none; background: var(--accent); color: #fff; padding: 10px 14px; border-radius: 8px; cursor: pointer; font-weight: 600; }}
    .button.secondary {{ background: #334155; }}
    .button.warn {{ background: var(--accent-2); }}
    main {{ display: grid; gap: 16px; margin-top: 16px; }}
    section.panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 16px; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04); }}
    h2 {{ margin-top: 0; font-size: 1.2rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.95rem; }}
    th, td {{ text-align: left; border-bottom: 1px solid var(--line); padding: 10px 8px; vertical-align: top; }}
    th {{ color: #0f172a; }}
    .repo-grid {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
    .repo-card {{ border: 1px solid var(--line); border-radius: 12px; padding: 14px; background: #fcfdff; }}
    .repo-card h3 {{ margin-top: 0; margin-bottom: 2px; }}
    .repo-card h4 {{ margin-bottom: 6px; margin-top: 14px; font-size: 0.95rem; }}
    .feature-columns {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
    .feature-column {{ border: 1px solid var(--line); border-radius: 12px; padding: 14px; background: #fcfdff; }}
    .feature-column h3 {{ margin-top: 0; margin-bottom: 2px; }}
    .feature-column h4 {{ margin-bottom: 6px; margin-top: 14px; font-size: 0.95rem; }}
    .mono {{ font-family: "SFMono-Regular", Consolas, monospace; color: var(--muted); margin-top: 0; }}
    .signals {{ display: grid; gap: 6px; font-size: 0.92rem; color: #334155; }}
    .chip {{ display: inline-block; padding: 3px 8px; border-radius: 999px; color: #fff; font-size: 0.82rem; font-weight: 600; }}
    .status-present {{ background: var(--ok); }}
    .status-partial {{ background: var(--warn); }}
    .status-missing {{ background: var(--bad); }}
    .status-planned {{ background: var(--planned); }}
    .status-unknown {{ background: var(--unknown); }}
    .check-chip {{ display: inline-block; padding: 3px 8px; border-radius: 999px; color: #fff; font-size: 0.82rem; font-weight: 600; }}
    .check-pass {{ background: var(--ok); }}
    .check-fail {{ background: var(--bad); }}
    .check-skip {{ background: #6b7280; }}
    .check-discovered {{ background: var(--planned); }}
    .empty {{ color: var(--muted); font-style: italic; }}
    ul {{ margin: 0.2rem 0 0.4rem 1.2rem; padding: 0; }}
    .rec-grid {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
    @media print {{
      .toolbar {{ display: none; }}
      body {{ background: #fff; }}
      section.panel, header {{ box-shadow: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{html.escape(project_name)} - Multi-Repo Review</h1>
      <p class="meta">Generated at {html.escape(generated_at)} UTC</p>
      <div class="toolbar">
        <button class="button" onclick="downloadCsv()">Export Spreadsheet (CSV)</button>
        <button class="button warn" onclick="window.print()">Export PDF</button>
        <a class="button secondary" href="review-data.json" download>Download JSON</a>
        {pdf_link}
      </div>
    </header>

    <main>
      <section class="panel">
        <h2>Project Goal</h2>
        <p>{html.escape(starting_goal or 'No explicit starting goal provided. Add `starting_goal` in input JSON.')}</p>
      </section>

      <section class="panel">
        <h2>Implementation Mapping</h2>
        <table>
          <thead>
            <tr>
              <th>Implementation</th>
              <th>Repository</th>
              <th>Repo ID</th>
              <th>Path</th>
            </tr>
          </thead>
          <tbody>
            {''.join(mapping_rows)}
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h2>Score Comparison</h2>
        <table>
          <thead>
            <tr>
              <th>Dimension</th>
              {repo_headers}
            </tr>
          </thead>
          <tbody>
            {''.join(score_rows)}
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h2>Goal & Verification Snapshot</h2>
        <table>
          <thead>
            <tr>
              <th>Metric</th>
              {repo_headers}
            </tr>
          </thead>
          <tbody>
            {''.join(verification_rows)}
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h2>Repository Findings</h2>
        <div class="repo-grid">
          {''.join(repo_cards)}
        </div>
      </section>

      <section class="panel">
        <h2>Side-by-Side Feature Comparison</h2>
        <div class="feature-columns">
          {''.join(side_by_side_cards)}
        </div>
      </section>

      <section class="panel">
        <h2>Feature Matrix</h2>
        <table>
          <thead>
            <tr>
              <th>Feature</th>
              {repo_headers}
            </tr>
          </thead>
          <tbody>
            {''.join(matrix_rows) if matrix_rows else f'<tr><td colspan="{empty_colspan}" class="empty">No feature data provided.</td></tr>'}
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h2>Cross-Repo Findings</h2>
        {findings_html}
      </section>

      <section class="panel">
        <h2>Recommendation</h2>
        <div class="rec-grid">
          <div>
            <h3>Recommended Path</h3>
            <p><strong>{html.escape(recommendation['recommended_repo'])}</strong></p>
            <p>{html.escape(recommendation['hybrid_strategy'] or 'No hybrid strategy provided.')}</p>
          </div>
          <div>
            <h3>Rationale</h3>
            {rationale_html}
          </div>
          <div>
            <h3>Next Steps</h3>
            {next_steps_html}
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const csvContent = {csv_js};

    function downloadCsv() {{
      const blob = new Blob([csvContent], {{ type: "text/csv;charset=utf-8;" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "comparison.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>
"""

    return html_output


def maybe_generate_pdf(html_path: Path, pdf_path: Path, mode: str) -> tuple[bool, str]:
    if mode == "never":
        return False, "PDF generation disabled (--pdf never)."

    wkhtmltopdf = shutil.which("wkhtmltopdf")
    if not wkhtmltopdf:
        if mode == "always":
            raise SystemExit("wkhtmltopdf not found in PATH but --pdf always was requested.")
        return False, "wkhtmltopdf not found; skipped PDF file generation."

    result = subprocess.run(
        [wkhtmltopdf, str(html_path), str(pdf_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "wkhtmltopdf failed").strip()
        if mode == "always":
            raise SystemExit(f"Failed to generate PDF: {message}")
        return False, f"wkhtmltopdf failed; skipped PDF file generation: {message}"

    return True, f"Generated PDF: {pdf_path}"


def main() -> int:
    args = parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    input_data = load_json(input_path)

    project_name = str(input_data.get("project_name", "Implementation Review")).strip() or "Implementation Review"
    starting_goal = str(input_data.get("starting_goal", "")).strip()
    generated_at = str(input_data.get("generated_at_utc", "")).strip()
    if not generated_at:
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    repos = normalize_repos(input_data.get("repos", []))
    feature_matrix = collect_feature_matrix(input_data, repos)
    cross_repo_findings = sanitize_text_list(input_data.get("cross_repo_findings", []))
    recommendation = summarize_recommendation(input_data, repos)

    csv_text = build_csv_text(
        project_name=project_name,
        generated_at=generated_at,
        starting_goal=starting_goal,
        repos=repos,
        feature_matrix=feature_matrix,
        recommendation=recommendation,
        cross_repo_findings=cross_repo_findings,
    )

    review_data = {
        "project_name": project_name,
        "starting_goal": starting_goal,
        "generated_at_utc": generated_at,
        "repo_count": len(repos),
        "repos": repos,
        "feature_matrix": [
            {
                "feature": row["feature"],
                **row["statuses"],
            }
            for row in feature_matrix
        ],
        "cross_repo_findings": cross_repo_findings,
        "recommended_path": recommendation,
        "analysis_notes": str(input_data.get("analysis_notes", "")).strip(),
    }

    review_json_path = output_dir / "review-data.json"
    review_json_path.write_text(json.dumps(review_data, indent=2) + "\n")

    csv_path = output_dir / "comparison.csv"
    csv_path.write_text(csv_text)

    html_path = output_dir / "report.html"
    pdf_path = output_dir / "report.pdf"

    html_text = build_html(
        project_name=project_name,
        generated_at=generated_at,
        starting_goal=starting_goal,
        repos=repos,
        feature_matrix=feature_matrix,
        cross_repo_findings=cross_repo_findings,
        recommendation=recommendation,
        csv_text=csv_text,
        pdf_available=False,
    )
    html_path.write_text(html_text)

    pdf_available = False
    pdf_message = "PDF generation disabled (--pdf never)."
    if args.pdf != "never":
        pdf_available, pdf_message = maybe_generate_pdf(html_path, pdf_path, args.pdf)
        if pdf_available:
            html_with_pdf_link = build_html(
                project_name=project_name,
                generated_at=generated_at,
                starting_goal=starting_goal,
                repos=repos,
                feature_matrix=feature_matrix,
                cross_repo_findings=cross_repo_findings,
                recommendation=recommendation,
                csv_text=csv_text,
                pdf_available=True,
            )
            html_path.write_text(html_with_pdf_link)

    print(f"[OK] Wrote HTML report: {html_path}")
    print(f"[OK] Wrote CSV export: {csv_path}")
    print(f"[OK] Wrote JSON data: {review_json_path}")
    print(f"[INFO] {pdf_message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
