import json
import os
import sys
from scanner.detector import scan_code

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SAMPLES = [
    ('sample_code/sql_injection.py', ['SQL injection']),
    ('sample_code/xss_example.html', ['Cross-Site Scripting (XSS)']),
    ('sample_code/command_injection.py', ['Command injection']),
    ('sample_code/secrets.py', ['Exposed secret']),
]

REPORT = {
    'tests_run': 0,
    'tests_passed': 0,
    'details': []
}


def run_test(sample_rel, expected_types):
    path = os.path.join(BASE_DIR, sample_rel)
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    results = scan_code(code)
    found_types = set([r['Issue Type'] for r in results])
    expected_set = set(expected_types)
    success = expected_set.issubset(found_types)
    detail = {
        'sample': sample_rel,
        'expected': list(expected_set),
        'found': list(found_types),
        'success': success,
        'issues': results
    }
    return success, detail


if __name__ == '__main__':
    for sample, expected in SAMPLES:
        REPORT['tests_run'] += 1
        ok, det = run_test(sample, expected)
        if ok:
            REPORT['tests_passed'] += 1
        REPORT['details'].append(det)

    REPORT['summary'] = f"{REPORT['tests_passed']} / {REPORT['tests_run']} passed"
    out = json.dumps(REPORT, indent=2)
    print(out)
    # Save report
    with open(os.path.join(BASE_DIR, 'report.json'), 'w', encoding='utf-8') as f:
        f.write(out)
    sys.exit(0 if REPORT['tests_passed'] == REPORT['tests_run'] else 2)
