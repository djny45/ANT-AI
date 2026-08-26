"""
Runtime factory for ANT AI execution.

Provides a single initialization boundary between Harness
services and the runtime implementation.
"""

from .agent_runtime_adapter import AgentRuntimeAdapter
from .runtime_controller import RuntimeController


def create_runtime_controller():
    """Create the configured runtime controller instance."""
    runtime = AgentRuntimeAdapter()
    return RuntimeController(runtime)
