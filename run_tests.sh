#!/usr/bin/env bash
set -e

# create output dir
mkdir -p reports

# Run pytest and produce JSON report using pytest-json-report if available
pytest -q --disable-warnings --maxfail=1

# Generate aggregate report and a sample scan
python scripts/generate_report.py
python -c "from src.security_scanner import scan_source, as_json; import json; s='API_KEY=\"sk_test_abc123\"\n'; issues=scan_source(s, '<example>'); print(as_json(issues))" > reports/example_scan.json

echo "Tests passed. Reports in reports/" 
