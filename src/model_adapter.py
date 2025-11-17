"""Utilities for loading a security model implementation.

The evaluator expects the model to expose an ``analyze`` method that accepts
an input payload (typically containing the source code snippet) and returns a
JSON-serialisable object describing the detected issues. The object should be a
list of dictionaries. Each dictionary must contain the keys ``Issue Type``,
``Description`` and ``Recommended Fix``.

By default we instantiate ``SampleSecurityModel`` which performs lightweight
static checks. To integrate a real model, set the ``MODEL_CLASS`` environment
variable to ``"module_path:ClassName"`` so the adapter can import and
instantiate it at runtime.
"""
from __future__ import annotations

import importlib
import os
from typing import Any, Protocol


class SecurityModel(Protocol):
    """Protocol that all security models must implement."""

    def analyze(self, input_payload: dict[str, Any]) -> Any:  # pragma: no cover
        """Return the model output for the supplied payload."""


def _parse_class_path(class_path: str) -> tuple[str, str]:
    if ":" not in class_path:
        raise ValueError(
            "MODEL_CLASS must look like 'package.module:ClassName', "
            f"got {class_path!r}"
        )
    module_name, class_name = class_path.split(":", 1)
    return module_name, class_name


def load_model() -> SecurityModel:
    """Instantiate the configured security model implementation."""

    class_path = os.getenv("MODEL_CLASS", "src.sample_model:SampleSecurityModel")
    module_name, class_name = _parse_class_path(class_path)

    module = importlib.import_module(module_name)
    model_cls = getattr(module, class_name)
    return model_cls()


__all__ = ["SecurityModel", "load_model"]
