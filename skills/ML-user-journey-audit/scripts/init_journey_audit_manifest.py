#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


DEFAULT_COLORS = [
    "#b74f2e",
    "#0b7a70",
    "#2b5fc7",
    "#8a3ffc",
    "#6e4c1e",
]


def parse_role(role_arg: str, index: int):
    parts = role_arg.split(":")
    if len(parts) < 2:
        raise ValueError(
            f"Invalid --role '{role_arg}'. Use id:Label or id:Label:#hexcolor."
        )

    role_id = parts[0].strip()
    label = parts[1].strip()
    color = parts[2].strip() if len(parts) > 2 and parts[2].strip() else DEFAULT_COLORS[index % len(DEFAULT_COLORS)]

    if not role_id or not label:
        raise ValueError(f"Invalid --role '{role_arg}'. Role id and label are required.")

    return {"id": role_id, "label": label, "color": color}


def build_inventory_headers():
    return [
        "Screen ID",
        "URL / State",
        "How You Get There",
        "Next Available Clicks",
        "Screenshot",
        "Confusion Notes",
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a JSON manifest for the user journey audit PDF renderer."
    )
    parser.add_argument("--title", required=True, help="Report title")
    parser.add_argument("--audit-root", required=True, help="Audit root directory")
    parser.add_argument("--output", required=True, help="Output manifest path")
    parser.add_argument(
        "--role",
        action="append",
        required=True,
        help="Role definition in the form id:Label or id:Label:#hexcolor. Repeat for multiple roles.",
    )
    args = parser.parse_args()

    roles = [parse_role(role_arg, index) for index, role_arg in enumerate(args.role)]
    audit_root = str(Path(args.audit_root).resolve())
    output_path = Path(args.output).resolve()

    manifest = {
        "title": args.title,
        "intro": "Fill in the current-state audit summary for this project.",
        "scopeLock": "Current-state only. Do not add future-state synthesis until the user asks for it.",
        "generatedAt": "",
        "auditRoot": audit_root,
        "roles": roles,
        "crossRoleComparison": {
            "headers": ["Surface"] + [role["label"] for role in roles] + ["Highest-signal confusion"],
            "rows": [],
        },
        "routeReuse": [],
        "redundancyMatrix": {
            "headers": ["User Type", "Observed User Task", "Current Surfaces", "Why It Feels Redundant"],
            "rows": [],
        },
        "terminologyMatrix": {
            "headers": ["User Type", "Concept", "Labels Found On Live Product", "Problem"],
            "rows": [],
        },
        "brokenRoutes": {
            "headers": ["Role", "Route", "Captured Outcome", "Evidence"],
            "rows": [],
        },
        "findings": [],
        "priorities": [],
        "coverage": {
            "updatedAt": "",
            "verdict": [],
            "covered": {
                "headers": ["Route Family", "Coverage Status", "Notes"],
                "rows": [],
            },
            "missingDashboard": {
                "headers": ["Route / Variant", "Evidence In Code Or Tests", "Current Report Status", "Why It Matters"],
                "rows": [],
            },
            "missingPublic": {
                "headers": ["Route Family", "Evidence In Code Or Tests", "Current Report Status", "Notes"],
                "rows": [],
            },
            "implications": [],
        },
        "roleReports": [
            {
                "id": role["id"],
                "label": role["label"],
                "title": f"{role['label']} User Journey",
                "accountUsed": "",
                "lastUpdated": "",
                "diagrams": [
                    {
                        "title": "Overview",
                        "mermaid": "flowchart TD\n  A[Entry] --> B[Primary Surface]",
                    }
                ],
                "findings": [],
                "inventory": {
                    "headers": build_inventory_headers(),
                    "rows": [],
                },
            }
            for role in roles
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")

    print(json.dumps({"output": str(output_path), "roles": roles}, indent=2))


if __name__ == "__main__":
    main()
