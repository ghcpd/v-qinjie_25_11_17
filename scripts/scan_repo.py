"""
Scan source files in the repository and produce a JSON file of detected issues.
This can be used as a baseline or additional test case for the AI model to evaluate
its ability to detect vulnerabilities and secrets exposure in a real repo.
"""
import os
import json
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.security_scanner import scan_files


def collect_files(root, extensions=None):
    if extensions is None:
        extensions = ['.py', '.js', '.html', '.env', '.cfg']
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip virtualenvs etc
        if '.venv' in dirpath or 'env' in dirpath or '__pycache__' in dirpath:
            continue
        for fn in filenames:
            if any(fn.endswith(ext) for ext in extensions):
                matches.append(os.path.join(dirpath, fn))
    return matches

files = collect_files(ROOT)
issues = scan_files(files)
with open('reports/repo_issues.json', 'w', encoding='utf-8') as f:
    json.dump({'issues': issues, 'scanned_files': len(files)}, f, indent=2)

print('Repo scan written to reports/repo_issues.json, scanned files:', len(files))
