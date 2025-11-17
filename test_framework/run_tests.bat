@echo off
REM Security Test Framework - Windows Test Runner
REM Automates setup, test execution, and report generation

setlocal enabledelayedexpansion

echo.
echo ====================================================================
echo Security Vulnerability Detection - Test Runner (Windows)
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Set directories
set SCRIPT_DIR=%~dp0
set VENV_DIR=%SCRIPT_DIR%venv
set REPORTS_DIR=%SCRIPT_DIR%reports

REM Create reports directory
if not exist "%REPORTS_DIR%" (
    mkdir "%REPORTS_DIR%"
    echo [*] Created reports directory
)

REM Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
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

REM Install dependencies
echo [*] Installing dependencies...
pip install -q -r "%SCRIPT_DIR%requirements.txt"
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [+] Dependencies installed

echo.
echo [*] Running security vulnerability detection tests...
echo.

REM Run tests
cd /d "%SCRIPT_DIR%"
python test_runner.py

REM Capture exit code
set TEST_EXIT_CODE=!errorlevel!

echo.
if !TEST_EXIT_CODE! equ 0 (
    echo [+] All tests completed successfully
) else (
    echo [!] Some tests failed. Check the report for details.
)

REM Show report location
for /f "tokens=*" %%A in ('dir /b /od "%REPORTS_DIR%\test_report_*.json" 2^>nul') do (
    set LATEST_REPORT=%%A
)

if defined LATEST_REPORT (
    echo.
    echo [*] Latest test report: %REPORTS_DIR%\!LATEST_REPORT!
)

REM Deactivate virtual environment
call "%VENV_DIR%\Scripts\deactivate.bat"

exit /b !TEST_EXIT_CODE!
