#!/usr/bin/env bash
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"
python -m venv venv || true
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m vuln_tests.tests.test_runner
