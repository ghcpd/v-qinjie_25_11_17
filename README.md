# Security Evaluation Harness

This project packages a reproducible test bench for validating whether an AI
model can detect common security vulnerabilities and exposed secrets, and return
JSON-formatted remediation guidance. The suite ships with a deterministic
`SampleSecurityModel` so the harness can run immediately, but it is designed to
allow you to plug in your own model implementation via configuration.

## What's Included

- **Structured test cases** (`tests/test_cases.json`) covering SQL injection,
  XSS, command injection, exposed secrets, safe code, and edge cases such as
  missing, null, and malformed inputs.
- **Evaluation runner** (`src/evaluator.py`) that feeds test prompts to the
  model, validates that the output JSON contains `Issue Type`, `Description`,
  and `Recommended Fix`, and compares the detected issues against expectations.
- **Reporting** automatically writes `reports/security_evaluation_report.json`
  summarizing pass/fail status plus per-case diagnostics.
- **Sample model + adapter** (`src/sample_model.py`, `src/model_adapter.py`)
  showing the required `analyze(input_payload: dict) -> list[dict]` interface.
- **Reproducible environment helpers** (`requirements.txt`, `setup.sh`,
  `setup.bat`) and **runtime scripts** (`run_tests.sh`, `run_tests.bat`).

## Getting Started

1. **Create a virtual environment and install dependencies**

   ```bash
   ./setup.sh
   ```

   On Windows use `setup.bat`. The current harness only uses the Python
   standard library, but the scripts keep the process reproducible if you add
   more dependencies later.

2. **Run the evaluation suite**

   ```bash
   ./run_tests.sh
   ```

   The script activates `.venv` when present and executes `python -m
   src.evaluator`. Reports are written into `reports/security_evaluation_report.json`
   and the CLI prints a short JSON summary with case counts.

## Integrating Your Model

- Implement a class with an `analyze(input_payload: dict[str, Any]) -> Any`
  method that returns JSON (or a JSON string) describing every detected issue as
  a list of objects containing the three required fields.
- Place the implementation on the Python path and set the `MODEL_CLASS`
  environment variable before running tests, e.g.

  ```bash
  export MODEL_CLASS="my_package.ai_client:CloudSecurityModel"
  ./run_tests.sh
  ```

  The adapter dynamically imports the class and instantiates it. Use the sample
  model as a template for the expected structure.

## Output Contract

Each detected issue must be encoded as JSON with the following shape:

```json
{
  "Issue Type": "SQL Injection",
  "Description": "SQL statement concatenates unsanitized user input.",
  "Recommended Fix": "Use parameterized queries."
}
```

The evaluator validates the presence of these fields, checks optional keyword
hints supplied in the fixture data, and enforces that edge cases such as missing
input payloads are handled gracefully.

## Test Reports

`src/evaluator.py` produces a machine-readable report with:

- ISO-8601 timestamps for reproducibility.
- Pass/fail counters and per-case diagnostics (missing issue types, keyword
  mismatches, and unexpected findings).
- Captured raw model output for debugging alongside the normalized issues.

All JSON artifacts live under the `reports/` directory so they can be archived or
fed into CI dashboards.
