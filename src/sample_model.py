"""Reference implementation of a tiny security scanner.

This deterministic model is not intended to replace a real AI system. Instead
it demonstrates the JSON output contract expected by ``src/evaluator.py`` and
provides an executable baseline so the test harness can run out of the box.
"""
from __future__ import annotations

import re
from typing import Any

Issue = dict[str, str]


class SampleSecurityModel:
    """Naive heuristic-based detector used for local regression tests."""

    secret_patterns = [
        re.compile(r"api[_-]?key\s*=\s*['\"]?[A-Za-z0-9-_]{16,}['\"]?", re.I),
        re.compile(r"aws[_-]?secret[_-]?access[_-]?key\s*=", re.I),
    ]

    def analyze(self, input_payload: dict[str, Any]) -> list[Issue]:
        raw_code = input_payload.get("code")
        if raw_code is None:
            return [
                self._issue(
                    "Invalid Input",
                    "Input payload is missing the 'code' field.",
                    "Provide the source snippet inside the 'code' entry.",
                )
            ]

        if not isinstance(raw_code, str):
            return [
                self._issue(
                    "Invalid Input",
                    "Expected 'code' to be a string payload.",
                    "Serialize the code as text before calling the model.",
                )
            ]

        code = raw_code.strip()
        if not code:
            return [
                self._issue(
                    "Invalid Input",
                    "Submitted code was empty.",
                    "Ensure the snippet contains source instructions to scan.",
                )
            ]

        issues: list[Issue] = []
        lowered = code.lower()

        if "@@@" in code or "<<<" in code:
            issues.append(
                self._issue(
                    "Malformed Code",
                    "The snippet appears to be corrupted or truncated.",
                    "Re-submit syntactically valid code before scanning.",
                )
            )

        if self._looks_like_sql_injection(code, lowered):
            issues.append(
                self._issue(
                    "SQL Injection",
                    "SQL statement concatenates unsanitized user input.",
                    "Use parameterized queries or an ORM with bound parameters.",
                )
            )

        if "innerhtml" in lowered and ("request" in lowered or "input" in lowered):
            issues.append(
                self._issue(
                    "Cross-Site Scripting",
                    "DOM sinks assign unsanitized data to innerHTML.",
                    "Sanitize or escape input and prefer textContent assignments.",
                )
            )

        if "os.system" in lowered or "subprocess.call" in lowered:
            if "input(" in lowered or "user_input" in lowered:
                issues.append(
                    self._issue(
                        "Command Injection",
                        "System command string incorporates user input directly.",
                        "Whitelist commands and use shlex.split with explicit arguments.",
                    )
                )

        for pattern in self.secret_patterns:
            if pattern.search(code):
                issues.append(
                    self._issue(
                        "Secrets Exposure",
                        "Detected hard-coded credential material.",
                        "Move secrets into a vault or environment variable store.",
                    )
                )
                break

        return issues or [
            self._issue(
                "No Issues Detected",
                "The snippet did not trigger the sample heuristics.",
                "Verify with production scanners for comprehensive coverage.",
            )
        ]

    @staticmethod
    def _looks_like_sql_injection(code: str, lowered: str) -> bool:
        if "select" not in lowered:
            return False
        sql_concat_tokens = ["+", "%", "format", "f\""]
        user_data_hints = ("input(", "request", "params", "form[")
        return any(token in code for token in sql_concat_tokens) and any(
            hint in lowered for hint in user_data_hints
        )

    @staticmethod
    def _issue(issue_type: str, description: str, fix: str) -> Issue:
        return {
            "Issue Type": issue_type,
            "Description": description,
            "Recommended Fix": fix,
        }


__all__ = ["SampleSecurityModel"]
