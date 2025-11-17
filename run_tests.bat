@echo off
REM Install dependencies (if needed) - user should have a virtualenv active
pip install -r requirements.txt

if not exist reports (
    mkdir reports
)

pytest -q --disable-warnings --maxfail=1

python scripts/generate_report.py

python - <<PY
from src.security_scanner import scan_source, as_json
s = 'API_KEY="sk_test_abc123"\n'
issues = scan_source(s, "<example>")
print(as_json(issues))
PY

IF %ERRORLEVEL% NEQ 0 (
    echo Tests failed.
    exit /b %ERRORLEVEL%
)

echo Tests passed. Reports in reports\
