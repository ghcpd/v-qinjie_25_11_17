Vulnerability and Secrets Detection Test Suite

This small project provides:
- A heuristic-based detector for common vulnerabilities (SQLi, XSS, Command Injection) and secrets exposure.
- A set of sample vulnerable files in `sample_code/`.
- A test runner in `tests/test_runner.py` that scans the samples and writes a JSON report to `report.json`.
- Dockerfile and run scripts for reproducible test environments.

Run locally:
- Windows: run run_tests.bat
- Unix: run ./run_tests.sh

Docker:
- docker build -t vuln-tests .
- docker run --rm vuln-tests
