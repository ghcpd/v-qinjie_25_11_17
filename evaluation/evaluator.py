"""Run the security vulnerability evaluation suite against a target model."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .mock_model import MockModelClient
from .model_client import SubprocessModelClient
from .test_cases import TEST_CASES, TestCase


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the vulnerability and secrets detection evaluation suite."
    )
    parser.add_argument(
        "--model-cmd",
        help="Command to execute the model. Expects JSON input on stdin and JSON list on stdout.",
    )
    parser.add_argument(
        "--report-dir",
        default="reports",
        help="Directory to persist JSON reports (default: reports).",
    )
    return parser.parse_args()


def _choose_model_client(args: argparse.Namespace):
    command = args.model_cmd or os.getenv("MODEL_COMMAND")
    if command:
        return SubprocessModelClient(command)
    return MockModelClient()


def _normalize_issue(issue: Dict[str, Any]) -> Dict[str, str]:
    return {
        "Issue Type": issue.get("Issue Type", ""),
        "Description": issue.get("Description", ""),
        "Recommended Fix": issue.get("Recommended Fix", ""),
    }


def _evaluate(test_case: TestCase, actual_issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected = {issue["Issue Type"]: issue for issue in test_case.expectations_as_dicts()}
    normalized_actual = {
        issue["Issue Type"]: _normalize_issue(issue) for issue in actual_issues
    }
    details = []
    passed = True

    for issue_type, expectation in expected.items():
        if issue_type not in normalized_actual:
            details.append(f"Missing expected issue: {issue_type}")
            passed = False
            continue
        actual = normalized_actual[issue_type]
        if actual["Description"] != expectation["Description"]:
            details.append(
                f"Description mismatch on {issue_type}: expected '{expectation['Description']}' vs '{actual['Description']}'"
            )
            passed = False
        if actual["Recommended Fix"] != expectation["Recommended Fix"]:
            details.append(
                f"Fix mismatch on {issue_type}: expected '{expectation['Recommended Fix']}' vs '{actual['Recommended Fix']}'"
            )
            passed = False

    for issue_type in normalized_actual:
        if issue_type not in expected:
            details.append(f"Reported unexpected issue: {issue_type}")
            passed = False

    return {
        "test_name": test_case.name,
        "status": "pass" if passed else "fail",
        "expected_issues": len(expected),
        "actual_issues": len(normalized_actual),
        "details": details,
        "edge_case_flags": test_case.edge_case_flags,
    }


def _write_report(report_dir: Path, entries: List[Dict[str, Any]]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = report_dir / f"evaluation_report_{timestamp}.json"
    summary = {
        "generated_at": timestamp,
        "total_tests": len(entries),
        "passed": sum(1 for e in entries if e["status"] == "pass"),
        "failed": sum(1 for e in entries if e["status"] == "fail"),
        "results": entries,
    }
    report_path.write_text(json.dumps(summary, indent=2))
    return report_path


def main() -> None:
    args = _parse_args()
    model_client = _choose_model_client(args)
    entries: List[Dict[str, Any]] = []

    print("Starting security evaluation on", len(TEST_CASES), "test cases.")
    for test_case in TEST_CASES:
        print(f"- Running {test_case.name}: {test_case.title}")
        try:
            actual = model_client.analyze(test_case)
        except Exception as exc:
            entries.append(
                {
                    "test_name": test_case.name,
                    "status": "fail",
                    "expected_issues": len(test_case.expected_issues),
                    "actual_issues": 0,
                    "details": [f"Model execution failed: {exc}"],
                    "edge_case_flags": test_case.edge_case_flags,
                }
            )
            continue
        entries.append(_evaluate(test_case, actual))

    report_dir = Path(args.report_dir)
    report_path = _write_report(report_dir, entries)

    print("Evaluation complete. Report saved to", report_path)


if __name__ == "__main__":
    main()
