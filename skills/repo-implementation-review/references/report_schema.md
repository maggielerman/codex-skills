# Report Input Schema

`build_report.py` consumes a JSON document with this shape.

## Top-Level

```json
{
  "project_name": "Shared project idea",
  "starting_goal": "What both implementations are supposed to achieve",
  "generated_at_utc": "2026-02-11T17:00:00Z",
  "repo_count": 2,
  "repos": [],
  "cross_repo_findings": [],
  "feature_matrix": [],
  "recommended_path": {
    "recommended_repo": "repo-a",
    "rationale": [],
    "hybrid_strategy": "",
    "next_steps": []
  },
  "analysis_notes": ""
}
```

## Repo Entry

```json
{
  "id": "repo-a",
  "name": "Implementation A",
  "path": "/absolute/path/to/repo-a",
  "auto_signals": {
    "total_files": 0,
    "source_files": 0,
    "top_languages": [
      {"language": "TypeScript", "files": 120}
    ],
    "manifests": ["package.json"],
    "key_files": {
      "README.md": true,
      "Dockerfile": false,
      ".github/workflows": true,
      "tests": true
    },
    "test_directories": ["tests"]
  },
  "summary": "",
  "scores": {
    "correctness": null,
    "architecture": null,
    "maintainability": null,
    "testing": null,
    "performance": null,
    "security": null,
    "delivery_readiness": null
  },
  "pros": [],
  "cons": [],
  "notable_features": [],
  "missing_features": [],
  "risks": [],
  "recommended_use_cases": [],
  "goal_alignment": {
    "stated_goal": "Goal statement inferred from repo/docs (editable)",
    "success_assessment": "How well this repo achieved the goal",
    "completion_score": null
  },
  "verification": {
    "checks": [
      {
        "name": "Python unittest discover",
        "type": "test",
        "command": "python3 -m unittest discover -s tests -p test_*.py",
        "status": "pass",
        "details": "17 tests passed."
      }
    ],
    "endpoint_checks": [
      {
        "method": "GET",
        "endpoint": "/api/health",
        "source": "runtime-probe",
        "status": "pass",
        "details": "HTTP 200"
      }
    ],
    "check_summary": {
      "pass": 2,
      "fail": 0,
      "skip": 1
    },
    "docs_review": {
      "coverage": "high",
      "quality_score": 4,
      "key_docs": ["README.md", "DOCS/index.md"],
      "gaps": []
    }
  },
  "feature_status": {
    "Core workflow complete": "present",
    "Automated tests": "present"
  }
}
```

## Feature Matrix (Optional)

If `feature_matrix` is omitted or empty, `build_report.py` derives one from `feature_status` and feature lists.

Manual matrix row format:

```json
{
  "feature": "Authentication",
  "repo-a": "present",
  "repo-b": "partial"
}
```

## Status Values

Use these values for feature status for best rendering:
- `present`
- `partial`
- `missing`
- `planned`
- `unknown`

For verification checks and endpoint checks, status values are:
- `pass`
- `fail`
- `skip`
- `discovered`

## Outcome-Oriented Features

Keep feature names capability-focused instead of tool-focused.

Preferred examples:
- `Core workflow complete`
- `Automated tests`
- `Endpoint health checks`
- `Scheduled execution`
- `Failure recovery`

Avoid tool/vendor-specific labels as primary comparison dimensions (for example `Cloudflare trigger`, `Notion pipeline`) unless they directly represent required product outcomes.
