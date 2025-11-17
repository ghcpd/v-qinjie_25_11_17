"""
Security Test Framework - API Reference Documentation

This module provides detailed API documentation for extending and customizing
the security vulnerability detection test framework.
"""

# ============================================================================
# MAIN TEST CLASSES
# ============================================================================

class TestCase:
    """
    Represents a single security test case.
    
    Attributes:
        test_id (str): Unique identifier for the test
        code (str): Source code to analyze
        expected_vulnerabilities (List[Dict]): Expected vulnerability findings
        expected_secrets (List[Dict]): Expected secret findings
        actual_result (Dict): Result from analysis
        passed (bool): Test pass/fail status
        failure_reason (str): Reason for test failure
    
    Methods:
        run() -> bool:
            Execute the test case and return pass/fail status.
            
        to_dict() -> Dict[str, Any]:
            Convert test case to dictionary format for reporting.
    
    Example:
        >>> test = TestCase(
        ...     test_id="SQL_INJECTION_001",
        ...     code="SELECT * FROM users WHERE id = {user_id}",
        ...     expected_vulns=[{...}],
        ...     expected_secrets=[]
        ... )
        >>> test.run()
        True
        >>> report = test.to_dict()
    """
    
    def run(self) -> bool:
        """Execute the test case."""
        pass
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        pass


class TestSuite:
    """
    Collection of test cases for batch execution.
    
    Attributes:
        test_cases (List[TestCase]): List of test cases
        results (List[Dict]): Test results
        start_time (datetime): Suite execution start time
        end_time (datetime): Suite execution end time
    
    Methods:
        add_test_case(test_case: TestCase) -> None:
            Add a test case to the suite.
        
        build_from_samples() -> None:
            Build test suite from vulnerable code samples.
        
        build_edge_cases() -> None:
            Add edge case tests to suite.
        
        run_all() -> Dict[str, Any]:
            Execute all test cases and return results.
        
        generate_report(output_file: str) -> str:
            Generate JSON report of test results.
    
    Example:
        >>> suite = TestSuite()
        >>> suite.build_from_samples()
        >>> suite.build_edge_cases()
        >>> results = suite.run_all()
        >>> suite.generate_report("reports/test_report.json")
    """
    
    def run_all(self) -> dict:
        """Run all tests and return results."""
        pass
    
    def generate_report(self, output_file: str) -> str:
        """Generate JSON report."""
        pass


class SecurityAnalyzer:
    """
    Core security analysis engine.
    
    This class should be implemented to provide actual vulnerability detection.
    Override the analyze_code() method with your detection logic.
    
    Methods:
        analyze_code(code: Optional[str]) -> Dict[str, Any]:
            Analyze code for vulnerabilities and secrets.
            
            Returns:
                {
                    "success": bool,
                    "vulnerabilities": List[Dict],
                    "secrets": List[Dict],
                    "error": str (if success=False)
                }
    
    Example Implementation:
        >>> analyzer = SecurityAnalyzer()
        >>> result = analyzer.analyze_code(vulnerable_code)
        >>> if result["success"]:
        ...     for vuln in result["vulnerabilities"]:
        ...         print(f"Found: {vuln['issue_type']}")
    """
    
    @staticmethod
    def analyze_code(code: str) -> dict:
        """Analyze code for security issues."""
        pass


# ============================================================================
# DATA STRUCTURES
# ============================================================================

# Vulnerability Detection Result
"""
{
    "issue_type": str,              # Type of vulnerability
    "description": str,             # Detailed description
    "location": str,                # Code location (line, function)
    "severity": str,                # CRITICAL|HIGH|MEDIUM|LOW
    "recommended_fix": str          # How to fix the vulnerability
}
"""

# Secret Detection Result
"""
{
    "issue_type": str,              # Type of secret (API Key, Password, etc)
    "description": str,             # What was exposed
    "location": str,                # Where it was found
    "severity": str,                # CRITICAL|HIGH|MEDIUM|LOW
    "recommended_fix": str          # Remediation guidance
}
"""

# Test Result Entry
"""
{
    "test_id": str,                 # Unique test identifier
    "code_snippet": str,            # Truncated source code
    "status": str,                  # PASSED|FAILED
    "expected_vulnerabilities": int,
    "expected_secrets": int,
    "failure_reason": Optional[str],
    "actual_result": {
        "success": bool,
        "vulnerabilities": List[Dict],
        "secrets": List[Dict],
        "error": Optional[str]
    }
}
"""

# Suite Report
"""
{
    "metadata": {
        "timestamp": str,           # ISO 8601 format
        "framework": str,
        "version": str
    },
    "summary": {
        "total_tests": int,
        "passed": int,
        "failed": int,
        "success_rate": str,        # Percentage as string
        "duration_seconds": float
    },
    "detailed_results": List[TestResult],
    "recommendations": List[str]
}
"""


# ============================================================================
# EXTENDING THE FRAMEWORK
# ============================================================================

class CustomSecurityAnalyzer(SecurityAnalyzer):
    """
    Example of extending SecurityAnalyzer with custom detection logic.
    
    Usage:
        1. Subclass SecurityAnalyzer
        2. Override analyze_code() method
        3. Implement your detection algorithms
        4. Use in test_runner.py
    """
    
    @staticmethod
    def analyze_code(code: str) -> dict:
        """
        Implement your custom vulnerability detection here.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Dictionary with vulnerabilities and secrets found
        """
        
        if code is None:
            return {
                "success": False,
                "error": "No code provided for analysis",
                "vulnerabilities": [],
                "secrets": []
            }
        
        vulnerabilities = []
        secrets = []
        
        # Example 1: Detect SQL Injection
        if "SELECT * FROM" in code and "{" in code:
            vulnerabilities.append({
                "issue_type": "SQL Injection",
                "description": "Potential SQL injection vulnerability detected",
                "location": "Code uses string formatting in SQL query",
                "severity": "CRITICAL",
                "recommended_fix": "Use parameterized queries with placeholders"
            })
        
        # Example 2: Detect hardcoded API keys
        if "api_key =" in code and "sk-" in code:
            secrets.append({
                "issue_type": "Hardcoded API Key",
                "description": "API key found hardcoded in source code",
                "location": "Variable assignment",
                "severity": "CRITICAL",
                "recommended_fix": "Use environment variables: api_key = os.getenv('API_KEY')"
            })
        
        return {
            "success": True,
            "vulnerabilities": vulnerabilities,
            "secrets": secrets
        }


# ============================================================================
# ADDING NEW TEST CASES
# ============================================================================

"""
To add new test cases, edit test_data/vulnerable_samples.py:

VULNERABLE_CODE_SAMPLES = [
    # ... existing cases ...
    {
        "test_id": "YOUR_VULN_001",
        "code": '''
def vulnerable_function(user_input):
    # Your vulnerable code here
    pass
        ''',
        "vulnerabilities": [
            {
                "issue_type": "Your Vulnerability Type",
                "description": "What makes this vulnerable",
                "location": "line X: where the vulnerability is",
                "severity": "CRITICAL",  # or HIGH, MEDIUM, LOW
                "recommended_fix": "How to fix this vulnerability"
            }
        ],
        "secrets": [
            # Any exposed secrets
        ]
    }
]
"""


# ============================================================================
# CONFIGURATION USAGE
# ============================================================================

"""
Configuration is read from config.yaml. Key settings:

logging:
  level: INFO              # DEBUG|INFO|WARNING|ERROR
  format: str              # Log format string

testing:
  timeout: 30              # Test timeout in seconds
  continue_on_failure: true
  verbosity: 1             # 0=quiet, 1=normal, 2=verbose

security:
  severity_levels:         # Which severities to report
    - CRITICAL
    - HIGH
  vulnerability_categories:
    - sql_injection
    - xss
    # ... more categories

reporting:
  format: json             # json|html|csv
  include_snippets: true
  snippet_length: 200
"""


# ============================================================================
# INTEGRATION PATTERNS
# ============================================================================

"""
Pattern 1: Custom Detection Logic

class MyAnalyzer(SecurityAnalyzer):
    @staticmethod
    def analyze_code(code):
        # Your ML model or heuristic analysis
        pass

# In test_runner.py:
result = MyAnalyzer.analyze_code(vulnerable_code)
"""

"""
Pattern 2: Batch Processing

suite = TestSuite()
suite.build_from_samples()
results = suite.run_all()
suite.generate_report("output.json")
"""

"""
Pattern 3: CI/CD Integration

import sys
import json
from test_runner import TestSuite

suite = TestSuite()
suite.build_from_samples()
results = suite.run_all()

# Check results
if results['summary']['failed'] > 0:
    sys.exit(1)  # Fail the build
else:
    sys.exit(0)  # Success
"""


# ============================================================================
# ERROR HANDLING
# ============================================================================

"""
Exception Handling:

try:
    test = TestCase(test_id="TEST_001", code=code, ...)
    if test.run():
        print("Test passed")
    else:
        print(f"Test failed: {test.failure_reason}")
except Exception as e:
    print(f"Error during test execution: {e}")
    # Log error, continue with next test
"""

"""
Edge Cases Handled:

- None/null code input
- Empty string code
- Malformed/invalid Python syntax
- Code with special characters
- Very large code samples
- Unicode content
"""


# ============================================================================
# OUTPUT EXAMPLES
# ============================================================================

"""
Successful Detection Example:

{
    "success": true,
    "vulnerabilities": [
        {
            "issue_type": "SQL Injection",
            "description": "User input directly concatenated in SQL",
            "location": "line 4: query = f\"SELECT * FROM users WHERE id = {user_id}\"",
            "severity": "CRITICAL",
            "recommended_fix": "Use parameterized queries with cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
        }
    ],
    "secrets": []
}
"""

"""
Error Handling Example:

{
    "success": false,
    "error": "Code contains syntax errors",
    "warning": "Partial analysis may be incomplete",
    "vulnerabilities": [],
    "secrets": []
}
"""


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

"""
Optimization Strategies:

1. Cache Analysis Results
   - Store results for identical code
   - Avoid re-analyzing same inputs

2. Parallel Execution
   - Use pytest plugin for parallel tests
   - Process multiple files concurrently

3. Memory Optimization
   - Stream large files instead of loading entirely
   - Use generators for test data iteration

4. Code Analysis Optimization
   - Use regex for pattern matching (faster than parsing)
   - Cache compiled patterns
   - Skip unnecessary checks for known-safe patterns
"""


# ============================================================================
# VERSION COMPATIBILITY
# ============================================================================

"""
Python Version Support:
- Python 3.8: Full support
- Python 3.9: Full support
- Python 3.10: Full support
- Python 3.11: Full support

Dependencies:
- pytest >= 7.4.3
- pyyaml >= 6.0.1
- requests >= 2.31.0
"""


# ============================================================================
# USEFUL LINKS
# ============================================================================

"""
Resources:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/
- Python Security: https://python.readthedocs.io/
- Bandit Tool: https://bandit.readthedocs.io/
- Semgrep: https://semgrep.dev/
"""
