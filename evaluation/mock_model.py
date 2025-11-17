from typing import Dict, List

from .model_client import BaseModelClient
from .test_cases import TEST_CASES, TestCase


class MockModelClient(BaseModelClient):
    """Deterministic mock that mimics expected model outputs for each test case."""

    def __init__(self):
        self._responses: Dict[str, List[Dict[str, str]]] = {
            test_case.name: test_case.expectations_as_dicts()
            for test_case in TEST_CASES
        }

    def analyze(self, test_case: TestCase) -> List[Dict[str, str]]:
        return self._responses.get(test_case.name, [])
