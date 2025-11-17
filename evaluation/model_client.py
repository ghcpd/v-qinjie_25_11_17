import json
import shlex
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List

from .test_cases import TestCase


class BaseModelClient(ABC):
    @abstractmethod
    def analyze(self, test_case: TestCase) -> List[Dict[str, str]]:
        """Return a list of issue dicts produced by the model."""


class SubprocessModelClient(BaseModelClient):
    def __init__(self, command: str):
        if not command:
            raise ValueError("Command must be provided to SubprocessModelClient.")
        self.command = shlex.split(command)

    def analyze(self, test_case: TestCase) -> List[Dict[str, str]]:
        payload = test_case.to_payload()
        process = subprocess.run(
            self.command,
            input=json.dumps(payload),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"Model command failed for {test_case.name}: {process.stderr.strip()}"
            )
        try:
            response = json.loads(process.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Model did not return valid JSON for {test_case.name}: {exc}"
            )
        if not isinstance(response, list):
            raise ValueError("Model output must be a list of issue dicts.")
        return response
