"""
Test Data Module - Contains sample vulnerable code and expected security issues
"""

VULNERABLE_CODE_SAMPLES = [
    {
        "test_id": "SQL_INJECTION_001",
        "code": """
def get_user(user_id):
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()
        """,
        "vulnerabilities": [
            {
                "issue_type": "SQL Injection",
                "description": "User input is directly concatenated into SQL query without parameterization",
                "location": "line 4: query = f\"SELECT * FROM users WHERE id = {user_id}\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
            }
        ],
        "secrets": []
    },
    {
        "test_id": "XSS_001",
        "code": """
def render_user_profile(user_input):
    html = f"<div><h1>{user_input['name']}</h1></div>"
    return html
        """,
        "vulnerabilities": [
            {
                "issue_type": "Cross-Site Scripting (XSS)",
                "description": "User input is directly rendered into HTML without escaping",
                "location": "line 2: html = f\"<div><h1>{user_input['name']}</h1></div>\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use HTML escaping: from html import escape; html = f\"<div><h1>{escape(user_input['name'])}</h1></div>\""
            }
        ],
        "secrets": []
    },
    {
        "test_id": "HARDCODED_API_KEY_001",
        "code": """
def connect_to_service():
    api_key = "sk-12345abcde67890fghij1234567890"
    service_url = "https://api.service.com"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(service_url, headers=headers)
    return response
        """,
        "vulnerabilities": [],
        "secrets": [
            {
                "issue_type": "Hardcoded API Key",
                "description": "API key is hardcoded in source code, exposing sensitive credential",
                "location": "line 2: api_key = \"sk-12345abcde67890fghij1234567890\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use environment variables: api_key = os.getenv('API_KEY'); or use secrets management tools like AWS Secrets Manager"
            }
        ]
    },
    {
        "test_id": "COMMAND_INJECTION_001",
        "code": """
def execute_command(user_input):
    import os
    command = f"ls {user_input}"
    os.system(command)
        """,
        "vulnerabilities": [
            {
                "issue_type": "Command Injection",
                "description": "User input is directly used in system command execution",
                "location": "line 4: command = f\"ls {user_input}\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use subprocess with argument list: subprocess.run(['ls', user_input], check=True)"
            }
        ],
        "secrets": []
    },
    {
        "test_id": "HARDCODED_PASSWORD_001",
        "code": """
def authenticate():
    username = "admin"
    password = "SecurePass123!@#"
    database_url = "mysql://admin:SecurePass123!@#@localhost:3306/mydb"
    return connect_db(database_url)
        """,
        "vulnerabilities": [],
        "secrets": [
            {
                "issue_type": "Hardcoded Database Password",
                "description": "Database password exposed in connection string",
                "location": "line 5: database_url = \"mysql://admin:SecurePass123!@#@localhost:3306/mydb\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use environment variables or secrets management: url = f\"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost:3306/mydb\""
            }
        ]
    },
    {
        "test_id": "PATH_TRAVERSAL_001",
        "code": """
def read_file(filename):
    filepath = f"/var/www/uploads/{filename}"
    with open(filepath, 'r') as f:
        return f.read()
        """,
        "vulnerabilities": [
            {
                "issue_type": "Path Traversal",
                "description": "User input is used to construct file path without validation, allowing directory traversal attacks",
                "location": "line 2: filepath = f\"/var/www/uploads/{filename}\"",
                "severity": "HIGH",
                "recommended_fix": "Validate and sanitize filename: import os.path; safe_path = os.path.abspath(os.path.join('/var/www/uploads', filename)); verify path is within allowed directory"
            }
        ],
        "secrets": []
    },
    {
        "test_id": "JWT_SECRET_EXPOSED_001",
        "code": """
def generate_token(user_id):
    import jwt
    secret_key = "my-secret-jwt-key-12345"
    token = jwt.encode({'user_id': user_id}, secret_key, algorithm='HS256')
    return token
        """,
        "vulnerabilities": [],
        "secrets": [
            {
                "issue_type": "Hardcoded JWT Secret",
                "description": "JWT secret key is hardcoded, compromising token security",
                "location": "line 3: secret_key = \"my-secret-jwt-key-12345\"",
                "severity": "CRITICAL",
                "recommended_fix": "Use environment variable: secret_key = os.getenv('JWT_SECRET')"
            }
        ]
    },
    {
        "test_id": "INSECURE_DESERIALIZATION_001",
        "code": """
def load_user_data(serialized_data):
    import pickle
    user_data = pickle.loads(serialized_data)
    return user_data
        """,
        "vulnerabilities": [
            {
                "issue_type": "Insecure Deserialization",
                "description": "Untrusted data is deserialized using pickle, allowing arbitrary code execution",
                "location": "line 3: user_data = pickle.loads(serialized_data)",
                "severity": "CRITICAL",
                "recommended_fix": "Use safe serialization: import json; user_data = json.loads(serialized_data); or use safer alternatives like marshal with restricted classes"
            }
        ],
        "secrets": []
    },
    {
        "test_id": "NO_VULNERABILITIES_001",
        "code": """
def safe_operation(user_id):
    import sqlite3
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchall()
        """,
        "vulnerabilities": [],
        "secrets": []
    }
]

EDGE_CASES = [
    {
        "test_id": "MISSING_INPUT",
        "code": None,
        "expected_output": "Error: No code provided for analysis"
    },
    {
        "test_id": "EMPTY_STRING",
        "code": "",
        "expected_output": "Warning: Empty code string provided"
    },
    {
        "test_id": "MALFORMED_CODE",
        "code": """
def incomplete_function(
    x = 10
    return x * 2
        """,
        "expected_output": "Warning: Code contains syntax errors"
    }
]
