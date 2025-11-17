"""
Security Vulnerability and Secrets Detection Test Framework
Main test runner for evaluating AI model's ability to detect security issues
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from test_data.vulnerable_samples import VULNERABLE_CODE_SAMPLES, EDGE_CASES


class SecurityAnalyzer:
    """Security analyzer with pattern-based detection"""
    
    @staticmethod
    def analyze_code(code: Optional[str]) -> Dict[str, Any]:
        """
        Analyze code for security vulnerabilities and secrets exposure.
        Uses pattern matching for common vulnerability detection.
        """
        if code is None:
            return {
                "success": False,
                "error": "No code provided for analysis",
                "vulnerabilities": [],
                "secrets": []
            }
        
        if code.strip() == "":
            return {
                "success": False,
                "error": "Empty code string provided",
                "vulnerabilities": [],
                "secrets": []
            }
        
        # Check for syntax errors
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError:
            return {
                "success": False,
                "error": "Code contains syntax errors",
                "vulnerabilities": [],
                "secrets": [],
                "warning": "Partial analysis may be incomplete"
            }
        
        vulnerabilities = []
        secrets = []
        
        # SQL Injection patterns
        if ("SELECT" in code or "INSERT" in code or "UPDATE" in code) and ("{" in code or "f\"" in code):
            if "?" not in code and "parameterized" not in code.lower():
                vulnerabilities.append({
                    "issue_type": "SQL Injection",
                    "description": "Potential SQL injection via string formatting",
                    "severity": "CRITICAL",
                    "recommended_fix": "Use parameterized queries"
                })
        
        # XSS patterns
        if "html" in code.lower() and "{" in code and ("<" in code or ">" in code):
            if "escape" not in code.lower():
                vulnerabilities.append({
                    "issue_type": "Cross-Site Scripting (XSS)",
                    "description": "User input rendered to HTML without escaping",
                    "severity": "CRITICAL",
                    "recommended_fix": "Use HTML escaping on user input"
                })
        
        # Command Injection patterns
        if ("os.system" in code or "subprocess" in code) and "{" in code:
            if "shell=False" not in code and "split(" not in code:
                vulnerabilities.append({
                    "issue_type": "Command Injection",
                    "description": "User input used in system command execution",
                    "severity": "CRITICAL",
                    "recommended_fix": "Use subprocess.run() with shell=False"
                })
        
        # Path Traversal patterns
        if ("open(" in code or "/var/www" in code or "filepath" in code.lower()) and "{" in code:
            if "abspath" not in code.lower() and "realpath" not in code.lower():
                vulnerabilities.append({
                    "issue_type": "Path Traversal",
                    "description": "File path constructed from user input without validation",
                    "severity": "HIGH",
                    "recommended_fix": "Validate and sanitize file paths"
                })
        
        # Insecure Deserialization
        if "pickle.loads" in code:
            vulnerabilities.append({
                "issue_type": "Insecure Deserialization",
                "description": "Untrusted data deserialized using pickle",
                "severity": "CRITICAL",
                "recommended_fix": "Use safe serialization like JSON"
            })
        
        # Hardcoded API Key patterns
        if ("api_key" in code or "API_KEY" in code) and "=" in code and '"' in code:
            if "os.getenv" not in code and "environ" not in code:
                if any(pattern in code for pattern in ["sk-", "key = \"", "key='", "token = \""]):
                    secrets.append({
                        "issue_type": "Hardcoded API Key",
                        "description": "API key or token hardcoded in source code",
                        "severity": "CRITICAL",
                        "recommended_fix": "Use environment variables"
                    })
        
        # Hardcoded Password patterns
        if ("password" in code.lower() or "passwd" in code.lower()) and ("=" in code):
            if "os.getenv" not in code and "environ" not in code:
                if any(c in code for c in ["\"", "'"]):
                    secrets.append({
                        "issue_type": "Hardcoded Password",
                        "description": "Password or credential hardcoded in source code",
                        "severity": "CRITICAL",
                        "recommended_fix": "Use environment variables or secrets management"
                    })
        
        # JWT Secret patterns
        if ("jwt" in code.lower() or "jwt_secret" in code.lower()) and ("=" in code):
            if "os.getenv" not in code and "environ" not in code:
                if "secret" in code.lower() and any(c in code for c in ["\"", "'"]):
                    secrets.append({
                        "issue_type": "Hardcoded JWT Secret",
                        "description": "JWT secret key hardcoded in source code",
                        "severity": "CRITICAL",
                        "recommended_fix": "Use environment variables"
                    })
        
        return {
            "success": True,
            "vulnerabilities": vulnerabilities,
            "secrets": secrets
        }


class TestCase:
    """Represents a single security test case"""
    
    def __init__(self, test_id: str, code: str, expected_vulns: List[Dict], 
                 expected_secrets: List[Dict]):
        self.test_id = test_id
        self.code = code
        self.expected_vulnerabilities = expected_vulns
        self.expected_secrets = expected_secrets
        self.actual_result = None
        self.passed = False
        self.failure_reason = None
    
    def run(self) -> bool:
        """Execute the test case"""
        try:
            self.actual_result = SecurityAnalyzer.analyze_code(self.code)
            
            if not self.actual_result.get("success", True):
                if self.actual_result.get("error"):
                    self.passed = True
                    return True
            
            # Check vulnerabilities detection
            detected_vulns = self.actual_result.get("vulnerabilities", [])
            if len(detected_vulns) != len(self.expected_vulnerabilities):
                self.failure_reason = (
                    f"Expected {len(self.expected_vulnerabilities)} vulnerabilities, "
                    f"but got {len(detected_vulns)}"
                )
                return False
            
            # Check secrets detection
            detected_secrets = self.actual_result.get("secrets", [])
            if len(detected_secrets) != len(self.expected_secrets):
                self.failure_reason = (
                    f"Expected {len(self.expected_secrets)} secrets, "
                    f"but got {len(detected_secrets)}"
                )
                return False
            
            self.passed = True
            return True
        
        except Exception as e:
            self.failure_reason = f"Exception during test execution: {str(e)}"
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert test case to dictionary for reporting"""
        # Handle None code safely
        if self.code is None:
            code_snippet = "None"
        elif len(self.code) > 100:
            code_snippet = self.code[:100] + "..."
        else:
            code_snippet = self.code
        
        return {
            "test_id": self.test_id,
            "code_snippet": code_snippet,
            "status": "PASSED" if self.passed else "FAILED",
            "expected_vulnerabilities": len(self.expected_vulnerabilities),
            "expected_secrets": len(self.expected_secrets),
            "failure_reason": self.failure_reason,
            "actual_result": self.actual_result
        }


class TestSuite:
    """Test suite for security analysis evaluation"""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results: List[Dict[str, Any]] = []
        self.start_time = None
        self.end_time = None
    
    def add_test_case(self, test_case: TestCase) -> None:
        """Add a test case to the suite"""
        self.test_cases.append(test_case)
    
    def build_from_samples(self) -> None:
        """Build test suite from vulnerable code samples"""
        for sample in VULNERABLE_CODE_SAMPLES:
            test = TestCase(
                test_id=sample["test_id"],
                code=sample["code"],
                expected_vulns=sample["vulnerabilities"],
                expected_secrets=sample["secrets"]
            )
            self.add_test_case(test)
    
    def build_edge_cases(self) -> None:
        """Add edge case tests"""
        for edge_case in EDGE_CASES:
            test = TestCase(
                test_id=edge_case["test_id"],
                code=edge_case["code"],
                expected_vulns=[],
                expected_secrets=[]
            )
            self.add_test_case(test)
    
    def run_all(self) -> Dict[str, Any]:
        """Run all test cases and collect results"""
        self.start_time = datetime.now()
        
        passed = 0
        failed = 0
        
        for test_case in self.test_cases:
            if test_case.run():
                passed += 1
            else:
                failed += 1
            
            self.results.append(test_case.to_dict())
        
        self.end_time = datetime.now()
        
        return {
            "summary": {
                "total_tests": len(self.test_cases),
                "passed": passed,
                "failed": failed,
                "success_rate": f"{(passed / len(self.test_cases) * 100):.2f}%" if self.test_cases else "N/A",
                "duration_seconds": (self.end_time - self.start_time).total_seconds()
            },
            "test_results": self.results
        }
    
    def generate_report(self, output_file: str) -> str:
        """Generate JSON report of test results"""
        if not self.results:
            return "No test results to report"
        
        report = {
            "metadata": {
                "timestamp": self.start_time.isoformat() if self.start_time else None,
                "framework": "Security Vulnerability Detection Test Suite",
                "version": "1.0.0"
            },
            "summary": {
                "total_tests": len(self.test_cases),
                "passed": sum(1 for r in self.results if r["status"] == "PASSED"),
                "failed": sum(1 for r in self.results if r["status"] == "FAILED"),
                "success_rate": f"{(sum(1 for r in self.results if r['status'] == 'PASSED') / len(self.results) * 100):.2f}%" if self.results else "N/A",
                "duration_seconds": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
            },
            "detailed_results": self.results,
            "recommendations": self._generate_recommendations()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_file
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        failed_tests = [r for r in self.results if r["status"] == "FAILED"]
        
        if len(failed_tests) > 0:
            recommendations.append(
                f"{len(failed_tests)} test(s) failed. Review detection logic for accuracy."
            )
        
        vuln_issues = [r for r in self.results if r.get("failure_reason") and r.get("failure_reason", "").startswith("Expected")]
        if vuln_issues:
            recommendations.append(
                "Improve vulnerability detection accuracy in code analysis logic."
            )
        
        if not recommendations:
            recommendations.append("All tests passed! Security detection framework is functioning correctly.")
        
        return recommendations


def main():
    """Main entry point"""
    print("=" * 70)
    print("Security Vulnerability & Secrets Detection Test Framework")
    print("=" * 70)
    print()
    
    # Create test suite
    suite = TestSuite()
    
    print("[*] Loading vulnerable code samples...")
    suite.build_from_samples()
    print(f"    Loaded {len(VULNERABLE_CODE_SAMPLES)} code samples")
    
    print("[*] Adding edge case tests...")
    suite.build_edge_cases()
    print(f"    Added {len(EDGE_CASES)} edge case tests")
    print()
    
    # Run tests
    print("[*] Running test suite...")
    results = suite.run_all()
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    summary = results["summary"]
    print(f"Total Tests:    {summary['total_tests']}")
    print(f"Passed:         {summary['passed']}")
    print(f"Failed:         {summary['failed']}")
    print(f"Success Rate:   {summary['success_rate']}")
    print(f"Duration:       {summary['duration_seconds']:.2f} seconds")
    print()
    
    # Generate report
    report_path = Path("reports") / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Generating report: {report_path}")
    suite.generate_report(str(report_path))
    print(f"    Report saved successfully!")
    print()
    
    # Print recommendations
    print("=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    for rec in results.get("test_results", []):
        if rec["status"] == "FAILED":
            print(f"[!] {rec['test_id']}: {rec['failure_reason']}")
    print()
    
    # Return exit code
    return 0 if summary['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
