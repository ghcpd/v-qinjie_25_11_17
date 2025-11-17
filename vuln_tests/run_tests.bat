@echo off
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m tests.test_runner
if %ERRORLEVEL% NEQ 0 (
    echo Some tests failed
    exit /b %ERRORLEVEL%
)
