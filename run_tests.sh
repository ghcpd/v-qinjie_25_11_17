#!/usr/bin/env bash
set -euo pipefail

PYTHON=${PYTHON:-python3}
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python interpreter '$PYTHON' not found"
  exit 1
fi
"$PYTHON" -m evaluation.evaluator --report-dir reports
