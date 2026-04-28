#!/usr/bin/env python3
"""Scaffold a lightweight UX/UI bug intake lifecycle folder for a repository."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


README_TEMPLATE = """---
title: UX/UI Bug Intake
description: Lightweight lifecycle rules for capturing, triaging, routing, and archiving UX/UI bugs
status: evolving
docRole: current-state
lastUpdated: "{timestamp}"
owner: Product/Engineering
---

# UX/UI Bug Intake

Use this folder as the canonical intake and lifecycle system for UX/UI bugs in this repository.

## Summary

- capture fast in `INBOX.md`
- normalize and route in `TRIAGED.md`
- move closed items into `ARCHIVE.md`
- keep project docs focused on execution rather than ad hoc bug memory

## Operating Model

- user detects bugs
- main agent detects bugs
- subagents detect bugs
- main agent remains the canonical logger and router

## Folder Roles

- `INBOX.md`
  - fast capture
  - append-first, low-friction
- `TRIAGED.md`
  - normalized working queue
  - one item per tracked bug
- `ARCHIVE.md`
  - fixed, superseded, or rejected items

## Entry Schema

- `ID`
- `Reported`
- `Detected by`
- `Actor`
- `Surface`
- `Summary`
- `Severity`
- `Status`
- `Likely owner`
- `Superseded by migration?`
- `Notes`

## Allowed Values

### Severity

- `blocker`
- `high`
- `medium`
- `low`

### Status

- `new`
- `triaged`
- `scheduled`
- `in active slice`
- `fixed`
- `wont-fix`
- `superseded`

## Triage Rules

### Fix Immediately

Pull a bug into the active branch only if it:

- breaks a real workflow
- blocks verification or CI
- creates misleading workflow truth
- is tiny and local to files already being edited
- is unlikely to be replaced by the next migration tranche

### Capture And Defer

Log the bug and defer it if it is:

- spacing, alignment, or visual polish
- hierarchy or copy awkwardness
- non-blocking responsive roughness
- grouped cleanup that is better handled as a planned tranche

## Subagent Contract

Subagents should report bugs they find, but they should not be the canonical logging system.

Have them return:

- short bug summary
- actor and surface
- likely owner stream
- blocker vs defer recommendation
- whether it looks likely to be superseded by ongoing migration

## Operating Rhythm

1. capture new UX/UI bugs in `INBOX.md`
2. normalize serious or clear items into `TRIAGED.md`
3. fix blocker-class or active-slice-local bugs immediately when warranted
4. at tranche boundaries, cluster the best triaged items into the next planned slice
5. move fixed, superseded, or rejected items into `ARCHIVE.md`
"""


INBOX_TEMPLATE = """---
title: UX/UI Bug Inbox
description: Append-first capture queue for newly reported or newly discovered UX/UI issues
status: evolving
docRole: current-state
lastUpdated: "{timestamp}"
owner: Product/Engineering
---

# UX/UI Bug Inbox

Use this file for fast capture before dedupe and routing.

## Rules

- append new items to the top
- keep entries short
- do not over-triage here
- move normalized items into `TRIAGED.md`
- move obsolete items into `ARCHIVE.md`

## Current Inbox

No active inbox items recorded yet.

## Capture Template

```md
## UIBUG-0001

- Reported: {timestamp}
- Detected by: user
- Actor: shared
- Surface: /dashboard/...
- Summary:
- Severity: blocker | high | medium | low
- Status: new
- Likely owner:
- Superseded by migration?: yes | no | likely | unknown
- Notes:
```
"""


TRIAGED_TEMPLATE = """---
title: Triaged UX/UI Bugs
description: Normalized working queue of routed UX/UI bugs after review and deduplication
status: evolving
docRole: current-state
lastUpdated: "{timestamp}"
owner: Product/Engineering
---

# Triaged UX/UI Bugs

Use this file for the curated working queue.

## Rules

- one entry per tracked bug
- update status here when a bug is scheduled, in-flight, fixed, or superseded
- keep owner stream explicit
- use this file during tranche planning and branch selection

## Current Triaged Queue

No triaged UX/UI bugs recorded yet.

## Entry Template

```md
## UIBUG-0001 - Short Title

- Reported: {timestamp}
- Detected by: user
- Actor: shared
- Surface: /dashboard/...
- Severity: medium
- Status: scheduled
- Likely owner:
- Superseded by migration?: no
- Decision: defer into the next planned slice
- Notes:
```
"""


ARCHIVE_TEMPLATE = """---
title: Archived UX/UI Bugs
description: Closed history for fixed, superseded, or rejected UX/UI bugs
status: evolving
docRole: historical
lastUpdated: "{timestamp}"
owner: Product/Engineering
---

# Archived UX/UI Bugs

Move entries here when they are:

- `fixed`
- `wont-fix`
- `superseded`

Keep the original bug ID and final disposition so old discussions still have a stable reference.

## Archive

No archived UX/UI bugs yet.
"""


def detect_docs_root(repo_root: Path) -> Path:
    for candidate in ("DOCS", "docs"):
        path = repo_root / candidate
        if path.is_dir():
            return path
    raise SystemExit("Could not find DOCS/ or docs/ in the target repository.")


def now_stamp() -> str:
    dt = datetime.now().astimezone()
    tz_name = dt.tzname() or "Local"
    return dt.strftime(f"%Y-%m-%d %H:%M {tz_name}")


def write_if_missing(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        print(f"skip  {path} (already exists)")
        return
    path.write_text(content, encoding="utf-8")
    print(f"write {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a lightweight UX/UI bug intake system."
    )
    parser.add_argument("--root", required=True, help="Repository root path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing lifecycle docs if they already exist",
    )
    args = parser.parse_args()

    repo_root = Path(args.root).expanduser().resolve()
    docs_root = detect_docs_root(repo_root)
    bug_root = docs_root / "UX_UI_BUGS"
    bug_root.mkdir(parents=True, exist_ok=True)

    timestamp = now_stamp()

    files = {
        bug_root / "README.md": README_TEMPLATE.format(timestamp=timestamp),
        bug_root / "INBOX.md": INBOX_TEMPLATE.format(timestamp=timestamp),
        bug_root / "TRIAGED.md": TRIAGED_TEMPLATE.format(timestamp=timestamp),
        bug_root / "ARCHIVE.md": ARCHIVE_TEMPLATE.format(timestamp=timestamp),
    }

    for path, content in files.items():
        write_if_missing(path, content, force=args.force)

    print("\nNext steps:")
    print("- wire the lifecycle folder into the repo's governance docs")
    print("- adapt timestamps/frontmatter to repo conventions")
    print("- add owner-routing defaults that match the repo's project system")


if __name__ == "__main__":
    main()
