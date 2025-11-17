@echo off
REM Security Test Framework - Windows Setup Script
REM Prepares the environment for testing

echo.
echo ====================================================================
echo Security Test Framework - Setup (Windows)
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://www.python.org
    exit /b 1
)

echo [+] Python is installed
python --version

REM Set directories
set SCRIPT_DIR=%~dp0
set VENV_DIR=%SCRIPT_DIR%venv

REM Create virtual environment
if exist "%VENV_DIR%" (
    echo [*] Virtual environment already exists at %VENV_DIR%
    echo [*] To recreate, delete the venv directory and run this script again
) else (
    echo [*] Creating Python virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
    echo [+] Virtual environment created
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    exit /b 1
)

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --quiet --upgrade pip

REM Install dependencies
echo [*] Installing dependencies from requirements.txt...
pip install -q -r "%SCRIPT_DIR%requirements.txt"
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [+] Dependencies installed successfully

REM Verify installation
echo.
echo [*] Verifying installation...
python -c "import pytest; import yaml" 2>nul
if errorlevel 1 (
    echo [ERROR] Verification failed - some dependencies may not be installed correctly
    exit /b 1
)
echo [+] All dependencies verified

echo.
echo ====================================================================
echo Setup completed successfully!
echo ====================================================================
echo.
echo [*] To run the test suite, execute:
echo     run_tests.bat
echo.
echo [*] The virtual environment is activated. Type "deactivate" to exit.
echo.

REM Keep the prompt open if run from double-click
if "%1"=="" pause

exit /b 0
