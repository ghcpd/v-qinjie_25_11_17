"""
Generate a detailed JSON report for the test cases using the scanner.

Report structure:
{
  "summary": {"total": n, "passed": m, "failed": k},
  "results": [
     {"name": "...", "expected": [...], "actual": [...], "passed": True|False, "issues": [...] }
  ]
}

This script is useful for CI and to create reproducible reports about the AI model's detection capabilities.
"""
import json
import os
import sys

# Ensure project root is on sys.path for imports
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import runpy
from src.security_scanner import scan_source
# Execute test module and extract TEST_CASES without requiring it to be a package import
module_globals = runpy.run_path(os.path.join(ROOT, 'tests', 'test_scanner.py'))
TEST_CASES = module_globals.get('TEST_CASES', [])


def canonicalize(issues):
    # keep minimal data for comparison and normalize multi-line suffix
    def base_type(t):
        if isinstance(t, str) and ' (multi-line)' in t:
            return t.replace(' (multi-line)', '')
        return t
    return sorted([{"issue_type": base_type(i["issue_type"]), "line": i["line"]} for i in issues], key=lambda x: (x['issue_type'], x['line']))


results = []
passed = 0
failed = 0
for case in TEST_CASES:
    actual = scan_source(case['input'], filename=case['name'])
    actual_min = canonicalize(actual)
    expected_min = canonicalize(case['expected']) if case['expected'] is not None else []
    ok = actual_min == expected_min
    if ok:
        passed += 1
    else:
        failed += 1
    results.append({
        'name': case['name'],
        'expected': expected_min,
        'actual': actual_min,
        'passed': ok,
        'issues': actual
    })

summary = {
    'total': len(TEST_CASES),
    'passed': passed,
    'failed': failed
}

report = {
    'summary': summary,
    'results': results
}

os.makedirs('reports', exist_ok=True)
with open('reports/test_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print('Report written to reports/test_report.json')
