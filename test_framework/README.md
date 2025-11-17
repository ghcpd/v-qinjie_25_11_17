# Security Vulnerability & Secrets Detection Test Framework

A comprehensive Python-based testing framework for evaluating AI model's ability to detect security vulnerabilities and exposed secrets in code.

## Overview

This framework provides:

- **Structured Test Data**: Pre-built vulnerable code samples covering multiple vulnerability types
- **Test Execution Engine**: Automated test runner with detailed result tracking
- **JSON Reporting**: Structured output in JSON format for easy integration
- **Reproducible Environment**: Docker, setup scripts, and requirements for consistency
- **Multi-Platform Support**: Windows (batch), Unix/Linux (bash), and Docker

## Vulnerability Types Detected

1. **SQL Injection** - Direct SQL query construction with user input
2. **Cross-Site Scripting (XSS)** - Unescaped HTML output
3. **Command Injection** - System commands with unsanitized input
4. **Path Traversal** - Unsafe file path construction
5. **Insecure Deserialization** - Unsafe pickle/object deserialization
6. **Hardcoded Secrets** - API keys, passwords, tokens in source code
7. **Configuration Issues** - Exposed database credentials, JWT secrets

## Project Structure

```
test_framework/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── test_runner.py                 # Main test framework
├── setup.bat                      # Windows setup script
├── setup.sh                        # Unix/Linux setup script
├── run_tests.bat                  # Windows test runner
├── run_tests.sh                   # Unix/Linux test runner
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── test_data/
│   └── vulnerable_samples.py      # Test data and vulnerable code samples
├── reports/
│   └── test_report_*.json         # Generated test reports
└── .gitignore                     # Git ignore file
```

## Quick Start

### Windows

```batch
# Setup environment
.\setup.bat

# Run tests
.\run_tests.bat
```

### Unix/Linux

```bash
# Setup environment
chmod +x setup.sh run_tests.sh
./setup.sh

# Run tests
./run_tests.sh
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up

# Or build and run manually
docker build -t security-test:latest .
docker run -v $(pwd)/reports:/app/reports security-test:latest
```

## Test Report Format

Each test report is generated in JSON format with the following structure:

```json
{
  "metadata": {
    "timestamp": "2024-11-17T10:30:45.123456",
    "framework": "Security Vulnerability Detection Test Suite",
    "version": "1.0.0"
  },
  "summary": {
    "total_tests": 11,
    "passed": 10,
    "failed": 1,
    "success_rate": "90.91%",
    "duration_seconds": 2.345
  },
  "detailed_results": [
    {
      "test_id": "SQL_INJECTION_001",
      "code_snippet": "def get_user(user_id): ...",
      "status": "PASSED",
      "expected_vulnerabilities": 1,
      "expected_secrets": 0,
      "failure_reason": null,
      "actual_result": {
        "success": true,
        "vulnerabilities": [...],
        "secrets": [...]
      }
    }
  ],
  "recommendations": [
    "All tests passed! Security detection framework is functioning correctly."
  ]
}
```

## Test Cases

The framework includes the following test cases:

### Vulnerability Detection Tests

1. **SQL_INJECTION_001** - Basic SQL injection vulnerability
2. **XSS_001** - Cross-Site Scripting vulnerability
3. **COMMAND_INJECTION_001** - OS command injection
4. **PATH_TRAVERSAL_001** - Directory traversal vulnerability
5. **INSECURE_DESERIALIZATION_001** - Unsafe pickle deserialization

### Secrets Detection Tests

1. **HARDCODED_API_KEY_001** - Exposed API key
2. **HARDCODED_PASSWORD_001** - Database password in connection string
3. **JWT_SECRET_EXPOSED_001** - JWT secret key hardcoded

### Safe Code Tests

1. **NO_VULNERABILITIES_001** - Properly parameterized queries

### Edge Case Tests

1. **MISSING_INPUT** - Null/missing code input
2. **EMPTY_STRING** - Empty code string
3. **MALFORMED_CODE** - Syntax errors in code

## Configuration

### Python Version

- Requires Python 3.8 or later
- Tested with Python 3.9, 3.10, and 3.11

### Dependencies

- `pytest` - Testing framework
- `pytest-json-report` - JSON report generation
- `requests` - HTTP client library
- `pyyaml` - YAML configuration support

### Environment Variables

- `PYTHONUNBUFFERED=1` - Disable Python output buffering
- `PYTHONDONTWRITEBYTECODE=1` - Don't write .pyc files

## Usage Examples

### Run All Tests

```bash
./run_tests.sh          # Unix/Linux
.\run_tests.bat         # Windows
```

### Run With Docker

```bash
docker-compose up --build

# Or run individual container
docker build -t security-test .
docker run -v $(pwd)/reports:/app/reports security-test
```

### Access Test Reports

Test reports are saved in the `reports/` directory with timestamps:
```
reports/test_report_20241117_103045.json
```

### Integration with CI/CD

The framework returns appropriate exit codes:
- Exit 0: All tests passed
- Exit 1: One or more tests failed

Example GitHub Actions workflow:
```yaml
- name: Run Security Tests
  run: ./run_tests.sh
```

## Expected Output Format

For each identified issue, the output includes:

```json
{
  "issue_type": "SQL Injection",
  "description": "User input is directly concatenated into SQL query without parameterization",
  "location": "line 4: query = f\"SELECT * FROM users WHERE id = {user_id}\"",
  "severity": "CRITICAL",
  "recommended_fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
}
```

## Best Practices

1. **Regular Testing**: Run tests as part of your CI/CD pipeline
2. **Report Review**: Examine generated reports for trends and patterns
3. **Environment Consistency**: Use Docker for cross-platform consistency
4. **Version Control**: Commit test data and scripts, exclude reports
5. **Continuous Improvement**: Update test cases as new vulnerabilities are discovered

## Troubleshooting

### Python Not Found

**Windows:**
```batch
# Add Python to PATH or use full path
C:\Python311\python.exe test_runner.py
```

**Unix/Linux:**
```bash
# Ensure python3 is installed
sudo apt-get install python3 python3-venv
```

### Virtual Environment Issues

**Windows:**
```batch
# Manually create and activate
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Unix/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Build Fails

```bash
# Clear Docker cache and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Security Considerations

1. **Test Data**: Contains intentionally vulnerable code for demonstration only
2. **Secrets**: Examples use fake/placeholder credentials, never use real ones
3. **Isolation**: Run tests in isolated environments (virtual machines or containers)
4. **Access Control**: Restrict access to test reports and logs

## Contributing

To add new test cases:

1. Add vulnerable code sample to `test_data/vulnerable_samples.py`
2. Include expected vulnerabilities and secrets
3. Update test case count in this README
4. Run full test suite to verify

Example:

```python
{
    "test_id": "NEW_VULN_001",
    "code": "vulnerable_code_here",
    "vulnerabilities": [
        {
            "issue_type": "Issue Type",
            "description": "Description",
            "location": "line X",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "recommended_fix": "Fix recommendation"
        }
    ],
    "secrets": []
}
```

## License

This test framework is provided as-is for security evaluation purposes.

## Support

For issues or improvements, please refer to the project documentation or contact the security team.

---

**Last Updated**: November 17, 2024
**Version**: 1.0.0
**Framework**: Python 3.8+
