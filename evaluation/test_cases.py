from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class IssueExpectation:
    issue_type: str
    description: str
    recommended_fix: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "Issue Type": self.issue_type,
            "Description": self.description,
            "Recommended Fix": self.recommended_fix,
        }


@dataclass
class TestCase:
    name: str
    title: str
    description: str
    code_snippet: Optional[str]
    context: Dict[str, str]
    expected_issues: List[IssueExpectation]
    edge_case_flags: List[str] = field(default_factory=list)

    def to_payload(self) -> Dict[str, object]:
        return {
            "test_name": self.name,
            "title": self.title,
            "description": self.description,
            "code": self.code_snippet,
            "context": self.context,
            "edge_cases": self.edge_case_flags,
        }

    def expectations_as_dicts(self) -> List[Dict[str, str]]:
        return [expectation.to_dict() for expectation in self.expected_issues]


TEST_CASES: List[TestCase] = [
    TestCase(
        name="sql_injection",
        title="Unparameterized SQL Query",
        description="Raw user input is interpolated directly into a SQL query string.",
        code_snippet=""
        "def get_user(cursor, user_id):\n"
        "    query = \"SELECT * FROM users WHERE id = \" + user_id\n"
        "    cursor.execute(query)\n",
        context={"language": "python", "entry_point": "user_service.py"},
        expected_issues=[
            IssueExpectation(
                issue_type="SQL injection",
                description="The SQL query concatenates user input without validation.",
                recommended_fix="Use parameterized queries (e.g., cursor.execute(query, (user_id,))) or an ORM.",
            )
        ],
    ),
    TestCase(
        name="xss_reflection",
        title="Reflective XSS",
        description="User-supplied profile data is rendered without escaping.",
        code_snippet=""
        "from flask import Flask, request\n"
        "app = Flask(__name__)\n\n"
        "@app.route('/greet')\n"
        "def greet():\n"
        "    name = request.args.get('name', '')\n"
        "    return f'<p>Hello, {name}</p>'\n",
        context={"language": "python", "entry_point": "profile.py"},
        expected_issues=[
            IssueExpectation(
                issue_type="Cross-Site Scripting (XSS)",
                description="HTTP response directly embeds the \"name\" query parameter into markup.",
                recommended_fix="Escape or sanitize `name` before rendering, or use a templating engine that auto-escapes.",
            )
        ],
    ),
    TestCase(
        name="command_injection",
        title="Shell command injection from user input",
        description="Directory names from requests are appended to a shell command.",
        code_snippet=""
        "import os\n"
        "def backup(directory):\n"
        "    os.system('tar -czf backup.tar.gz ' + directory)\n",
        context={"language": "python", "entry_point": "backup.py"},
        expected_issues=[
            IssueExpectation(
                issue_type="Command injection",
                description="`os.system` constructs a shell command that directly concatenates `directory`.",
                recommended_fix="Use subprocess.run with a list of arguments or validate/escape the directory variable.",
            )
        ],
    ),
    TestCase(
        name="hardcoded_secret",
        title="Hardcoded API credential",
        description="An AWS API key is stored directly in source control.",
        code_snippet=""
        "API_KEY = 'AKIAFAKEEXAMPLEKEY12345'\n"
        "def upload(data):\n"
        "    send_to_service(data, API_KEY)\n",
        context={"language": "python", "entry_point": "secrets.py"},
        expected_issues=[
            IssueExpectation(
                issue_type="Exposed secret",
                description="The AWS key is hardcoded in the module instead of being read from the environment.",
                recommended_fix="Move secrets to environment variables, configuration stores, or vaults and document rotation steps.",
            )
        ],
    ),
    TestCase(
        name="missing_input",
        title="Missing input payload",
        description="The model receives a null payload instead of source code.",
        code_snippet=None,
        context={"language": "python", "entry_point": "missing_input"},
        expected_issues=[
            IssueExpectation(
                issue_type="Missing input",
                description="No code snippet was provided for analysis.",
                recommended_fix="Validate inputs before analysis and prompt for the missing content.",
            )
        ],
        edge_case_flags=["null", "missing"],
    ),
    TestCase(
        name="malformed_code",
        title="Malformed or truncated source",
        description="Code snippet is not syntactically valid, which should still prompt a best-effort assessment.",
        code_snippet="def broken(\n    return 1",
        context={"language": "python", "entry_point": "broken.py"},
        expected_issues=[
            IssueExpectation(
                issue_type="Malformed code",
                description="The submitted code snippet fails to parse because of unbalanced parentheses.",
                recommended_fix="Acknowledge the malformed code, request a complete snippet, and skip assumptions.",
            )
        ],
        edge_case_flags=["malformed"],
    ),
]
