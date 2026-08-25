"""
ANT AI Harness bootstrap layer.

Provides application startup wiring for the Harness runtime.
"""

from .execution_service import ExecutionService


def create_harness_runtime():
    """Create the Harness execution runtime."""
    return ExecutionService()
