#!/bin/bash

# Security Test Framework - Unix/Linux Setup Script
# Prepares the environment for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

echo ""
echo "===================================================================="
echo "Security Test Framework - Setup (Unix/Linux)"
echo "===================================================================="
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python 3.8 or later:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3"
    exit 1
fi

echo "[+] Python is installed"
python3 --version

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "[*] Virtual environment already exists at $VENV_DIR"
    echo "[*] To recreate, delete the venv directory and run this script again"
else
    echo "[*] Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "[+] Virtual environment created"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# Upgrade pip
echo "[*] Upgrading pip..."
python3 -m pip install --quiet --upgrade pip

# Install dependencies
echo "[*] Installing dependencies from requirements.txt..."
pip install -q -r "${SCRIPT_DIR}/requirements.txt"
echo "[+] Dependencies installed successfully"

# Verify installation
echo ""
echo "[*] Verifying installation..."
python3 -c "import pytest; import yaml" 2>/dev/null || {
    echo "[ERROR] Verification failed - some dependencies may not be installed correctly"
    exit 1
}
echo "[+] All dependencies verified"

echo ""
echo "===================================================================="
echo "Setup completed successfully!"
echo "===================================================================="
echo ""
echo "[*] To run the test suite, execute:"
echo "    ./run_tests.sh"
echo ""
echo "[*] The virtual environment is activated. Type 'deactivate' to exit."
echo ""

exit 0
