from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.model_adapter import SecurityModel, load_model

REQUIRED_KEYS = ("Issue Type", "Description", "Recommended Fix")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run structured tests against a security analysis model",
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("tests/test_cases.json"),
        help="Path to the JSON file containing evaluation inputs.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where JSON reports will be written.",
    )
    return parser.parse_args()


def load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_output(raw_output: Any) -> tuple[list[dict[str, Any]], list[str]]:
    """Convert model output into a list of issue dictionaries."""

    errors: list[str] = []
    issues: Any = raw_output

    if isinstance(issues, str):
        try:
            issues = json.loads(issues)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            errors.append(f"Model returned non-JSON string: {exc}")
            return [], errors

    if isinstance(issues, dict):
        if "issues" in issues and isinstance(issues["issues"], list):
            issues = issues["issues"]
        else:
            issues = [issues]

    if not isinstance(issues, list):
        errors.append("Model response must be a list or JSON object containing 'issues'.")
        return [], errors

    valid_issues: list[dict[str, Any]] = []
    for idx, item in enumerate(issues):
        if not isinstance(item, dict):
            errors.append(f"Issue #{idx} is not an object: {item!r}")
            continue
        missing = [key for key in REQUIRED_KEYS if key not in item]
        if missing:
            errors.append(
                f"Issue #{idx} missing required fields: {', '.join(missing)}"
            )
            continue
        valid_issues.append(item)
    return valid_issues, errors


def evaluate_expectations(
    issues: Iterable[dict[str, Any]], expected: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    expected_issues = expected.get("issues", [])
    allow_extra = expected.get("allow_additional_issues", True)

    issues = list(issues)
    issue_map = {
        issue["Issue Type"].lower(): issue for issue in issues
        if isinstance(issue.get("Issue Type"), str)
    }

    missing_issue_types: list[str] = []
    keyword_mismatches: list[str] = []

    for expected_issue in expected_issues:
        issue_type = expected_issue["issue_type"].lower()
        match = issue_map.get(issue_type)
        if not match:
            missing_issue_types.append(expected_issue["issue_type"])
            continue
        desc_keywords = expected_issue.get("description_keywords", [])
        fix_keywords = expected_issue.get("recommended_fix_keywords", [])
        description = match["Description"].lower()
        fix = match["Recommended Fix"].lower()
        if any(keyword.lower() not in description for keyword in desc_keywords):
            keyword_mismatches.append(
                f"{expected_issue['issue_type']}: missing description keyword"
            )
        if any(keyword.lower() not in fix for keyword in fix_keywords):
            keyword_mismatches.append(
                f"{expected_issue['issue_type']}: missing fix keyword"
            )

    unexpected_issue_types: list[str] = []
    if not allow_extra:
        expected_types = {entry["issue_type"].lower() for entry in expected_issues}
        unexpected_issue_types = [
            issue["Issue Type"]
            for issue in issues
            if issue["Issue Type"].lower() not in expected_types
        ]

    case_passed = not (
        missing_issue_types or keyword_mismatches or unexpected_issue_types
    )

    details = {
        "missing_issue_types": missing_issue_types,
        "keyword_mismatches": keyword_mismatches,
        "unexpected_issue_types": unexpected_issue_types,
    }
    return case_passed, details


def evaluate_case(model: SecurityModel, case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id", "unknown")
    expected = case.get("expected", {})
    input_payload = case.get("input", {})

    result: dict[str, Any] = {
        "case_id": case_id,
        "description": case.get("description", ""),
        "status": "failed",
        "errors": [],
        "details": {},
        "issues": [],
        "raw_output": None,
    }

    try:
        raw_output = model.analyze(input_payload)
    except Exception as exc:  # pragma: no cover - surface runtime errors
        result["errors"].append(f"Model raised an exception: {exc}")
        return result

    result["raw_output"] = raw_output
    issues, format_errors = normalize_output(raw_output)
    result["issues"] = issues
    result["errors"].extend(format_errors)

    if format_errors:
        return result

    passed, details = evaluate_expectations(issues, expected)
    result["details"] = details
    result["status"] = "passed" if passed else "failed"
    return result


def run() -> dict[str, Any]:
    args = parse_args()
    cases = load_cases(args.cases)
    model = load_model()

    case_results = [evaluate_case(model, case) for case in cases]
    passed = sum(1 for result in case_results if result["status"] == "passed")
    failed = len(case_results) - passed

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "case_count": len(case_results),
        "passed": passed,
        "failed": failed,
        "cases": case_results,
    }

    args.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.report_dir / "security_evaluation_report.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(
        json.dumps(
            {
                "summary": {
                    "total": len(case_results),
                    "passed": passed,
                    "failed": failed,
                    "report": str(report_path),
                }
            },
            indent=2,
        )
    )
    return report


if __name__ == "__main__":
    run()
