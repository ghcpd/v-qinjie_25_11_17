"""
Simple static-pattern based security scanner for detecting common vulnerabilities and secrets exposure.

This is intended for evaluation and testing an AI model that detects and remediates vulnerabilities.
"""
import re
import json
from typing import List, Dict, Optional

# Detection patterns
PATTERNS = [
    {
        "type": "SQL Injection",
        "regex": re.compile(r"(\bSELECT\b|\bUPDATE\b|\bDELETE\b|\bINSERT\b)\b.*(\+|f\"|format\(|%\(|\{).*", re.IGNORECASE | re.DOTALL),
        "description": "SQL query constructed by concatenating or interpolating user input, which may lead to SQL Injection.",
        "fix": "Use parameterized queries or ORM parameter binding. Avoid building SQL with string concatenation or f-strings."
    },
    {
        "type": "Command Injection",
        "regex": re.compile(r"\b(os\.system|subprocess\.(?:Popen|call|run))\b.*(\+|f\"|format\()", re.IGNORECASE | re.DOTALL),
        "description": "Shell or OS command constructed using potentially unsafe string concatenation or interpolation.",
        "fix": "Use argument lists instead of shell=True; validate or sanitize inputs. Avoid concatenating user input into shell commands."
    },
    {
        "type": "Cross Site Scripting (XSS)",
        "regex": re.compile(r"(innerHTML\s*=\s*|document\.write\(|<script>).*{?%?\s*\w+\s*%?}?", re.IGNORECASE),
        "description": "User input is inserted into HTML without proper escaping, which can lead to XSS.",
        "fix": "Escape or sanitize user-supplied data before inserting into HTML; use safe templating functions and Content Security Policy."
    },
    {
        "type": "Exposed Secret",
        "regex": re.compile(r"(sk_live_|sk_test_|AIza[0-9A-Za-z\-_]{35}|AKIA[0-9A-Z]{16}|['\"](?:password|passwd|secret|api_key|apikey|auth_token|token)['\"]\s*[:=]\s*['\"][^'\"]+['\"])", re.IGNORECASE),
        "description": "Hardcoded secret or API key found in code or configuration.",
        "fix": "Move secrets to secure storage (environment variables, secret manager). Remove keys from version control and rotate keys if they were committed."
    },
]


def scan_source(source: Optional[str], filename: str = "<input>") -> List[Dict]:
    """Scan source code string and return list of found issues.

    The returned list will follow the JSON structure required by tests:
    [
      {
        "issue_type": "...",
        "description": "...",
        "file": "...",
        "line": 123,
        "snippet": "...",
        "recommended_fix": "...",
      }
    ]
    """
    if source is None:
        return []

    issues = []
    lines = source.splitlines()
    for idx, line in enumerate(lines, start=1):
        for p in PATTERNS:
            if p['regex'].search(line):
                snippet = line.strip()
                issues.append({
                    "issue_type": p['type'],
                    "description": p['description'],
                    "file": filename,
                    "line": idx,
                    "snippet": snippet,
                    "recommended_fix": p['fix']
                })
    # Additional heuristic: detect concatenated SQL across multiple lines
    # Combine into blocks to catch multi-line queries built using + and variables
    # Search for "SELECT.*+.*" across blocks; simple approach
    combined = "\n".join(lines)
    for p in PATTERNS:
        if p['type'] == "Command Injection":
            # detect multi-line command injection by seeing both an invocation and unsafe concatenation anywhere in file
            has_invocation = re.search(r"\b(os\.system|subprocess\.(?:Popen|call|run))\b", combined, re.IGNORECASE)
            has_concat = re.search(r"\+|f\"|format\(|%\(|\.format\(", combined)
            if has_invocation and has_concat:
                base_type = p['type']
                if not any((i['issue_type'].startswith(base_type) and i['file'] == filename) for i in issues):
                    # find the line number of the invocation
                    invocation_match = re.search(r"\b(os\.system|subprocess\.(?:Popen|call|run))\b", combined, re.IGNORECASE)
                    line_no = 1
                    if invocation_match:
                        # count number of newlines before the match
                        line_no = combined[:invocation_match.start()].count('\n') + 1
                    issues.append({
                        "issue_type": p['type'] + " (multi-line)",
                        "description": "Potential multi-line %s. %s" % (p['type'], p['description']),
                        "file": filename,
                        "line": line_no,
                        "snippet": combined[:200] + ("..." if len(combined) > 200 else ""),
                        "recommended_fix": p['fix']
                    })
        elif p['type'] == "SQL Injection":
            if p['regex'].search(combined):
                base_type = p['type']
                if not any((i['issue_type'].startswith(base_type) and i['file'] == filename) for i in issues):
                    issues.append({
                        "issue_type": p['type'] + " (multi-line)",
                        "description": "Potential multi-line %s. %s" % (p['type'], p['description']),
                        "file": filename,
                        "line": 1,
                        "snippet": combined[:200] + ("..." if len(combined) > 200 else ""),
                        "recommended_fix": p['fix']
                    })

    # Deduplicate by (type, file, line, snippet)
    uniq = []
    seen = set()
    for i in issues:
        key = (i['issue_type'], i['file'], i['line'], i['snippet'])
        if key not in seen:
            seen.add(key)
            uniq.append(i)
    return uniq


def scan_files(file_paths: List[str]) -> List[Dict]:
    results = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as exc:
            results.append({
                "issue_type": "Error",
                "description": f"Could not read file: {exc}",
                "file": path,
                "line": 0,
                "snippet": "",
                "recommended_fix": "Check file path and permissions."
            })
            continue
        issues = scan_source(source, filename=path)
        results.extend(issues)
    return results


def as_json(issues: List[Dict]) -> str:
    return json.dumps({"issues": issues}, indent=2)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Security scanner for simple vulnerability detection')
    parser.add_argument('files', nargs='*', help='Files to scan')
    parser.add_argument('--output', '-o', help='Write JSON output to file')

    args = parser.parse_args()
    if not args.files:
        print('No files provided. Send input via stdin or pass file paths.')
        exit(1)

    issues = scan_files(args.files)
    json_out = as_json(issues)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_out)
    else:
        print(json_out)
