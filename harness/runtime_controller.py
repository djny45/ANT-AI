"""
ANT AI runtime controller.

Provides a controlled execution boundary between the orchestrator
and the intelligence runtime implementation.
"""

from typing import Any, Dict

from .runtime_interface import RuntimeInterface
from .runtime_validation import validate_runtime_context


class RuntimeController:
    """Coordinates validated runtime execution requests."""

    def __init__(self, runtime: RuntimeInterface):
        self.runtime = runtime

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        validation = validate_runtime_context(context)

        if not validation["valid"]:
            return {
                "status": "failed",
                "error": "invalid_runtime_context",
                "details": validation.get("errors", []),
            }

        return self.runtime.execute(context)
