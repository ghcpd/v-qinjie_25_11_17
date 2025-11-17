Security Scanner Test Harness

This repository contains a simple static-pattern based security scanner and a test harness to evaluate an AI model's ability to detect vulnerabilities and secrets exposure.

What is included:
- src/security_scanner.py: pattern-based detector for common vulnerabilities
- tests/test_scanner.py: structured pytest cases and assertions, including edge cases
- run_tests.sh / run_tests.bat: Scripts to execute tests and generate a sample JSON report
- Dockerfile: lightweight reproducible environment for running tests
- setup scripts: setup.sh and setup.bat for local setup

Output format:
- The scanner returns JSON with the following fields per issue:
  - issue_type
  - description
  - recommended_fix
  - file
  - line
  - snippet

Run locally:
- Linux/macOS: ./setup.sh && ./run_tests.sh
- Windows: setup.bat & run_tests.bat

Run with Docker:
- docker build -t sec-scanner .
- docker run --rm -it sec-scanner bash
- inside container: pytest -q
