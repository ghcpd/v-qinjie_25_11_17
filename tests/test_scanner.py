import json
import os
import pytest
from src.security_scanner import scan_source, as_json

TEST_CASES = [
    {
        "name": "sql_injection_concat",
        "input": '''username = input()
query = "SELECT * FROM users WHERE name = '" + username + "'"
''',
        "expected": [
            {
                "issue_type": "SQL Injection",
                "line": 2
            }
        ]
    },
    {
        "name": "command_injection_shell",
        "input": "import os\ncmd = 'ls ' + user_input\nos.system(cmd)\n",
        "expected": [
            {
                "issue_type": "Command Injection",
                "line": 3
            }
        ]
    },
    {
        "name": "xss_innerhtml",
        "input": "// example js\ndocument.body.innerHTML = userInput;\n",
        "expected": [
            {
                "issue_type": "Cross Site Scripting (XSS)",
                "line": 2
            }
        ]
    },
    {
        "name": "exposed_secret",
        "input": "API_KEY = \"sk_test_1234567890\"\n",
        "expected": [
            {
                "issue_type": "Exposed Secret",
                "line": 1
            }
        ]
    },
    {
        "name": "no_issues_empty",
        "input": "",
        "expected": []
    },
    {
        "name": "null_input_none",
        "input": None,
        "expected": []
    },
    {
        "name": "malformed_code",
        "input": "query = \"SELECT * FROM users WHERE name = {\n",
        "expected": [
            {
                "issue_type": "SQL Injection",
                "line": 1
            }
        ]
    },
    {
        "name": "safe_parameterized_query",
        "input": "query = 'SELECT * FROM users WHERE id = %s'\ncursor.execute(query, (user_id,))\n",
        "expected": []
    },
    {
        "name": "safe_subprocess_list",
        "input": "import subprocess\ncmd = ['ls', user_input]\nsubprocess.run(cmd)\n",
        "expected": []
    }
]


def canonicalize(issues):
    # reduce details to type and line for easier assertions
    def base_type(t):
        if isinstance(t, str) and ' (multi-line)' in t:
            return t.replace(' (multi-line)', '')
        return t
    return sorted([{"issue_type": base_type(i["issue_type"]), "line": i["line"]} for i in issues], key=lambda x: (x['issue_type'], x['line']))


@pytest.mark.parametrize('case', TEST_CASES)
def test_scanner(case):
    issues = scan_source(case['input'], filename=case['name'])
    # Canonicalize to compare only types and lines
    actual = canonicalize(issues)
    expected = canonicalize(case['expected']) if case['expected'] is not None else []
    assert actual == expected, f"Test {case['name']} failed. Expected: {expected}, Actual: {actual}"


def test_output_json_file(tmp_path):
    # Run a case and write JSON, ensure it matches structure
    case = TEST_CASES[0]
    issues = scan_source(case['input'], filename=case['name'])
    json_str = as_json(issues)
    data = json.loads(json_str)
    assert 'issues' in data
    assert isinstance(data['issues'], list)
    # Ensure that the structure has the required fields
    if data['issues']:
        for i in data['issues']:
            assert 'issue_type' in i
            assert 'description' in i
            assert 'recommended_fix' in i
            assert 'file' in i
            assert 'line' in i


def test_scan_files(tmp_path):
    # ensure scanning a sample file works and reports issues
    sample = 'samples/vuln_example.py'
    issues = scan_source(open(sample, 'r', encoding='utf-8').read(), filename=sample)
    assert any(i['issue_type'].startswith('SQL Injection') for i in issues)
    assert any('Command Injection' in i['issue_type'] for i in issues)


if __name__ == '__main__':
    pytest.main(['-q', '--disable-warnings'])
