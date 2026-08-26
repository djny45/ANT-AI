"""
ANT AI runtime controller.

Provides a controlled execution boundary between the orchestrator
and the intelligence runtime implementation.
"""

from typing import Any, Dict

from .runtime_interface import RuntimeInterface


class RuntimeController:
    """Coordinates runtime execution requests."""

    def __init__(self, runtime: RuntimeInterface):
        self.runtime = runtime

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.runtime.execute(context)
