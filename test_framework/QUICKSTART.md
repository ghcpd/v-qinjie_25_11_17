# Security Vulnerability Detection Framework - Quick Reference

## 📋 Project Overview

A comprehensive Python-based test framework for evaluating AI model's security detection capabilities, covering both vulnerability identification and secrets exposure detection.

## 🚀 Quick Start

### Windows
```batch
cd test_framework
setup.bat
run_tests.bat
```

### Linux/macOS
```bash
cd test_framework
chmod +x setup.sh run_tests.sh
./setup.sh
./run_tests.sh
```

### Docker
```bash
cd test_framework
docker-compose up --build
```

## 📁 Project Structure

```
test_framework/
├── README.md                    # Complete documentation
├── IMPLEMENTATION_GUIDE.md      # Detailed implementation guide
├── QUICKSTART.md               # This file
├── requirements.txt             # Python dependencies
├── config.yaml                  # Configuration settings
├── test_runner.py              # Main test framework
├── Dockerfile                  # Docker container definition
├── docker-compose.yml          # Docker Compose config
│
├── Setup Scripts:
├── setup.bat                   # Windows setup
├── setup.sh                    # Unix/Linux setup
├── run_tests.bat               # Windows test runner
├── run_tests.sh                # Unix/Linux test runner
│
├── test_data/
│   ├── __init__.py
│   └── vulnerable_samples.py   # Test cases (8 vulnerabilities + 3 edge cases)
│
└── reports/
    └── sample_test_report.json # Example output report
```

## 🔍 Test Coverage

### Vulnerability Tests (5)
- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal
- Insecure Deserialization

### Secrets Detection Tests (3)
- Hardcoded API Keys
- Exposed Database Passwords
- Exposed JWT Secrets

### Edge Case Tests (3)
- Missing/Null Input
- Empty String
- Malformed Code

### Safe Code (1)
- Properly Secured Code Sample

## 📊 Report Output Format

### JSON Structure
```json
{
  "metadata": { "timestamp", "framework", "version" },
  "summary": { "total_tests", "passed", "failed", "success_rate", "duration_seconds" },
  "detailed_results": [
    {
      "test_id", "status", "code_snippet",
      "expected_vulnerabilities", "expected_secrets",
      "actual_result": {
        "issue_type", "description", "location", "severity", "recommended_fix"
      }
    }
  ],
  "recommendations": ["..."]
}
```

### Sample Report Location
`reports/sample_test_report.json`

## ⚙️ Configuration

Edit `config.yaml` to customize:
- Logging level
- Test timeout (default: 30s)
- Severity levels to report
- Report output format
- Environment settings

## 🔧 System Requirements

| Component | Requirement |
|-----------|------------|
| Python | 3.8+ |
| Disk Space | ~50MB |
| Memory | ~100MB runtime |
| OS | Windows, Linux, macOS |

### Optional
- Docker 20.10+
- Docker Compose 1.29+

## 📦 Dependencies

All installed via `requirements.txt`:
- pytest (testing framework)
- pytest-json-report (JSON reporting)
- requests (HTTP client)
- pyyaml (YAML config support)

## 🎯 Key Features

✅ **Reproducible Environments**
- Virtual environment isolation
- Docker containerization
- Consistent cross-platform execution

✅ **Comprehensive Test Data**
- 8 vulnerable code samples
- 3 edge case tests
- 1 safe code reference
- Real-world vulnerability patterns

✅ **Structured Reporting**
- JSON format for integration
- Detailed remediation guidance
- Performance metrics
- Test coverage summary

✅ **Multi-Platform Support**
- Windows batch scripts
- Unix/Linux shell scripts
- Docker/Docker Compose
- Cross-OS compatibility

## 🚦 Running Tests

### View Help
```bash
python3 test_runner.py --help  # (if implemented)
```

### Run Full Suite
```bash
./run_tests.sh              # Linux/macOS
.\run_tests.bat             # Windows
docker-compose up           # Docker
```

### Check Results
Reports are saved to: `reports/test_report_YYYYMMDD_HHMMSS.json`

## 📈 Expected Metrics

- **Execution Time**: 2-3 seconds
- **Report Generation**: <1 second
- **Success Rate Target**: >90%
- **Memory Usage**: <100MB

## 🔐 Security Considerations

⚠️ **Important Notes:**
- Test data contains intentionally vulnerable code
- Uses fake/placeholder credentials only
- Never use real secrets in test cases
- Run in isolated environments
- Restrict access to test reports

## 🛠️ Extending the Framework

### Add New Test Case
1. Edit `test_data/vulnerable_samples.py`
2. Add entry to `VULNERABLE_CODE_SAMPLES`
3. Include expected vulnerabilities/secrets
4. Run test suite to verify

### Custom Detection Logic
Implement your AI model in `SecurityAnalyzer.analyze_code()` method in `test_runner.py`

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete feature documentation |
| IMPLEMENTATION_GUIDE.md | Detailed integration guide |
| QUICKSTART.md | This quick reference |
| config.yaml | Configuration settings |
| sample_test_report.json | Example output format |

## 🐛 Troubleshooting

### Python Not Found
```bash
# Windows: Add Python to PATH or use full path
# Linux: sudo apt-get install python3

# Verify installation
python3 --version
```

### Permission Denied (Linux)
```bash
chmod +x setup.sh run_tests.sh
```

### Virtual Environment Issues
```bash
# Recreate environment
rm -rf venv
./setup.sh
```

### Docker Issues
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 📞 Integration Examples

### GitHub Actions
```yaml
- name: Run Security Tests
  run: cd test_framework && ./run_tests.sh
```

### Jenkins
```groovy
stage('Test') {
  steps { sh 'cd test_framework && ./run_tests.sh' }
}
```

### CI/CD Pipeline
Tests return appropriate exit codes:
- Exit 0: All tests passed ✅
- Exit 1: Tests failed ❌

## 📝 Next Steps

1. **Review Documentation**: Read `README.md` for complete details
2. **Run Setup**: Execute `setup.bat` (Windows) or `./setup.sh` (Unix/Linux)
3. **Execute Tests**: Run `run_tests.bat` or `./run_tests.sh`
4. **Check Reports**: Open generated report in `reports/` directory
5. **Customize**: Modify test cases or detection logic as needed

## 📋 File Checklist

- ✅ Core Framework
  - ✅ test_runner.py
  - ✅ test_data/vulnerable_samples.py
  - ✅ requirements.txt
  - ✅ config.yaml

- ✅ Setup & Execution
  - ✅ setup.bat / setup.sh
  - ✅ run_tests.bat / run_tests.sh
  
- ✅ Containerization
  - ✅ Dockerfile
  - ✅ docker-compose.yml

- ✅ Documentation
  - ✅ README.md
  - ✅ IMPLEMENTATION_GUIDE.md
  - ✅ QUICKSTART.md (this file)

- ✅ Sample Outputs
  - ✅ sample_test_report.json

- ✅ Misc
  - ✅ .gitignore

## Version Info

- **Framework Version**: 1.0.0
- **Python Support**: 3.8+
- **Last Updated**: November 17, 2024
- **Status**: Production Ready

---

**For detailed information, see README.md or IMPLEMENTATION_GUIDE.md**
