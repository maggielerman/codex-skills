#!/usr/bin/env python3
"""Validate the structured execution packet used by the tranche orchestrator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath


VALID_STATUSES = {"active", "in-review", "blocked", "completed", "backlog", "stale"}
VALID_DELEGATION_MODES = {"collaborative", "autonomous"}
REQUIRED_ORCHESTRATION_KEYS = {
    "delegation_mode",
    "user_approval_required",
    "source_refs",
    "must_read_files",
    "drift_triggers",
}
REQUIRED_PROJECT_KEYS = {"id", "title", "source_doc", "current_status"}
REQUIRED_TRANCHE_KEYS = {
    "id",
    "name",
    "objective",
    "in_scope",
    "non_goals",
    "dependencies",
    "blockers",
    "exit_criteria",
    "escalation_conditions",
    "lifecycle_target_after_review",
}
REQUIRED_ASSIGNMENT_KEYS = {
    "role",
    "objective",
    "scope",
    "non_goals",
    "write_paths",
    "source_refs",
    "must_read_files",
    "acceptance_criteria",
    "verification",
    "handoff_prompt",
}
REQUIRED_REVIEW_GATE_KEYS = {"doc_criteria", "code_review_checks", "required_evidence"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "packet",
        nargs="?",
        help="Path to a JSON packet file. If omitted, JSON is read from stdin.",
    )
    return parser.parse_args()


def load_payload(path: str | None) -> dict:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Packet root must be a JSON object.")
    return payload


def ensure_keys(name: str, payload: dict, required: set[str], errors: list[str]) -> None:
    missing = sorted(required - payload.keys())
    if missing:
        errors.append(f"{name} is missing keys: {', '.join(missing)}")


def ensure_string_list(name: str, value: object, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{name} must be a list of strings.")
        return
    if not allow_empty and not value:
        errors.append(f"{name} must not be empty.")


def normalize_path(path: str) -> PurePosixPath:
    return PurePosixPath(path.strip("/"))


def overlaps(left: str, right: str) -> bool:
    left_path = normalize_path(left)
    right_path = normalize_path(right)
    if left_path == right_path:
        return True
    return str(left_path).startswith(f"{right_path}/") or str(right_path).startswith(f"{left_path}/")


def validate_assignments(assignments: object, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(assignments, list) or not assignments:
        errors.append("assignments must be a non-empty list.")
        return

    normalized_paths: list[tuple[str, str]] = []

    for index, assignment in enumerate(assignments, start=1):
        if not isinstance(assignment, dict):
            errors.append(f"assignments[{index}] must be an object.")
            continue

        ensure_keys(f"assignments[{index}]", assignment, REQUIRED_ASSIGNMENT_KEYS, errors)
        for field in ("role", "objective", "handoff_prompt"):
            if field in assignment and not isinstance(assignment[field], str):
                errors.append(f"assignments[{index}].{field} must be a string.")
        if "quote_back_required" in assignment and not isinstance(assignment["quote_back_required"], bool):
            errors.append(f"assignments[{index}].quote_back_required must be a boolean.")
        for field in (
            "scope",
            "non_goals",
            "write_paths",
            "source_refs",
            "must_read_files",
            "acceptance_criteria",
            "verification",
        ):
            if field in assignment:
                ensure_string_list(f"assignments[{index}].{field}", assignment[field], errors)

        for path in assignment.get("write_paths", []):
            if not isinstance(path, str):
                continue
            normalized_paths.append((f"assignments[{index}]", path))

    for left_index, left in enumerate(normalized_paths):
        for right in normalized_paths[left_index + 1 :]:
            if overlaps(left[1], right[1]):
                warnings.append(
                    f"Potential write-path overlap between {left[0]}:{left[1]} and {right[0]}:{right[1]}"
                )


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args.packet)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"valid": False, "errors": [str(exc)], "warnings": []}, indent=2))
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    for key in ("orchestration", "project", "tranche", "assignments", "review_gate"):
        if key not in payload:
            errors.append(f"Missing top-level key: {key}")

    orchestration = payload.get("orchestration")
    if isinstance(orchestration, dict):
        ensure_keys("orchestration", orchestration, REQUIRED_ORCHESTRATION_KEYS, errors)
        if orchestration.get("delegation_mode") not in VALID_DELEGATION_MODES:
            errors.append("orchestration.delegation_mode must be 'collaborative' or 'autonomous'.")
        if "user_approval_required" in orchestration and not isinstance(
            orchestration["user_approval_required"], bool
        ):
            errors.append("orchestration.user_approval_required must be a boolean.")
        for field in ("source_refs", "must_read_files", "drift_triggers"):
            if field in orchestration:
                ensure_string_list(f"orchestration.{field}", orchestration[field], errors)
        if (
            orchestration.get("delegation_mode") == "collaborative"
            and orchestration.get("user_approval_required") is False
        ):
            warnings.append(
                "orchestration.delegation_mode is collaborative but user_approval_required is false."
            )
    else:
        errors.append("orchestration must be an object.")

    project = payload.get("project")
    if isinstance(project, dict):
        ensure_keys("project", project, REQUIRED_PROJECT_KEYS, errors)
        if "current_status" in project and project["current_status"] not in VALID_STATUSES:
            errors.append("project.current_status must be a known lifecycle status.")
    else:
        errors.append("project must be an object.")

    tranche = payload.get("tranche")
    if isinstance(tranche, dict):
        ensure_keys("tranche", tranche, REQUIRED_TRANCHE_KEYS, errors)
        for field in ("objective", "id", "name"):
            if field in tranche and not isinstance(tranche[field], str):
                errors.append(f"tranche.{field} must be a string.")
        for field in (
            "in_scope",
            "non_goals",
            "dependencies",
            "blockers",
            "exit_criteria",
            "escalation_conditions",
        ):
            if field in tranche:
                ensure_string_list(f"tranche.{field}", tranche[field], errors, allow_empty=(field in {"dependencies", "blockers"}))
        if tranche.get("lifecycle_target_after_review") not in VALID_STATUSES:
            errors.append("tranche.lifecycle_target_after_review must be a known lifecycle status.")
    else:
        errors.append("tranche must be an object.")

    validate_assignments(payload.get("assignments"), errors, warnings)

    review_gate = payload.get("review_gate")
    if isinstance(review_gate, dict):
        ensure_keys("review_gate", review_gate, REQUIRED_REVIEW_GATE_KEYS, errors)
        for field in REQUIRED_REVIEW_GATE_KEYS:
            if field in review_gate:
                ensure_string_list(f"review_gate.{field}", review_gate[field], errors)
    else:
        errors.append("review_gate must be an object.")

    result = {"valid": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
