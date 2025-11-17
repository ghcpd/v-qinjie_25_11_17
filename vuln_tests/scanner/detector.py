import re
import json
from typing import List, Dict

# Heuristic based detectors for sample vulnerabilities and secrets

SQLI_PATTERNS = [
    re.compile(r"execute\(.+\+.+\)"),  # string concatenation used in DB execute
    re.compile(r"format\(.+\)"),  # format used in SQL
    # Assignment of SQL query using string concatenation
    re.compile(r"\bquery\s*=\s*['\"].*\+.*['\"]", re.IGNORECASE),
    # General heuristic: SQL keyword followed by concatenation
    re.compile(r"\bSELECT\b.*\+.*", re.IGNORECASE),
]

XSS_PATTERNS = [
    re.compile(r"innerHTML\s*=")
]

COMMAND_INJECTION_PATTERNS = [
    # Match common patterns calling shell-like functions; use non-capturing groups for alternation
    re.compile(r"(?:os\.system|subprocess\.call|subprocess\.Popen)\s*\(")
]

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key
    re.compile(r"(?:api[_-]?key|secret|access[_-]?token|password)\s*=\s*['\"]([^'\"]{8,})['\"]", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")  # Base64-like long strings
]


def scan_code(code: str) -> List[Dict]:
    issues = []

    # SQL injection heuristics
    for p in SQLI_PATTERNS:
        for m in p.finditer(code):
            issues.append({
                "Issue Type": "SQL injection",
                "Description": f"Potential SQL injection via unparameterized SQL in: {m.group(0)[:120]}",
                "Recommended Fix": "Use parameterized queries (e.g., db.execute(sql, params)) or an ORM that safely binds parameters."
            })

    # XSS heuristics
    for p in XSS_PATTERNS:
        for m in p.finditer(code):
            issues.append({
                "Issue Type": "Cross-Site Scripting (XSS)",
                "Description": f"Potential DOM XSS via assignment to innerHTML: {m.group(0)}",
                "Recommended Fix": "Avoid using innerHTML for untrusted data. Use textContent or proper encoding/sanitization."
            })

    # Command injection heuristics
    for p in COMMAND_INJECTION_PATTERNS:
        for m in p.finditer(code):
            issues.append({
                "Issue Type": "Command injection",
                "Description": f"Use of system calls with potentially concatenated args: {m.group(0)}",
                "Recommended Fix": "Use subprocess.run with a list and validate input; avoid shell=True and concatenate only sanitized values."
            })

    # Secrets detection
    for p in SECRET_PATTERNS:
        for m in p.finditer(code):
            val = m.group(0)
            if len(val) > 8:
                issues.append({
                    "Issue Type": "Exposed secret",
                    "Description": f"Hard-coded secret or token detected: {val[:60]}",
                    "Recommended Fix": "Move secrets to environment variables or a secret manager; rotate and remove historical exposure."
                })

    return issues


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file provided"}))
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    results = scan_code(code)
    print(json.dumps(results, indent=2))
