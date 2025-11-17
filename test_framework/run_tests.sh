#!/bin/bash

# Security Test Framework - Unix/Linux Test Runner
# Automates setup, test execution, and report generation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
REPORTS_DIR="${SCRIPT_DIR}/reports"

echo ""
echo "===================================================================="
echo "Security Vulnerability Detection - Test Runner (Unix/Linux)"
echo "===================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "[*] Found: $PYTHON_VERSION"

# Create reports directory
if [ ! -d "$REPORTS_DIR" ]; then
    mkdir -p "$REPORTS_DIR"
    echo "[*] Created reports directory"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "[+] Virtual environment created"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# Install dependencies
echo "[*] Installing dependencies..."
pip install -q -r "${SCRIPT_DIR}/requirements.txt"
echo "[+] Dependencies installed"

echo ""
echo "[*] Running security vulnerability detection tests..."
echo ""

# Run tests
cd "$SCRIPT_DIR"
python3 test_runner.py

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "[+] All tests completed successfully"
else
    echo "[!] Some tests failed. Check the report for details."
fi

# Show report location
LATEST_REPORT=$(ls -t "$REPORTS_DIR"/test_report_*.json 2>/dev/null | head -1)
if [ -n "$LATEST_REPORT" ]; then
    echo ""
    echo "[*] Latest test report: $LATEST_REPORT"
fi

# Deactivate virtual environment
deactivate

exit $TEST_EXIT_CODE
