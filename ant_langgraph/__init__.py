"""LangGraph-style orchestration foundation for ANT AI.

This package intentionally uses a small internal graph abstraction so it can
integrate with the existing ANT_X_OS runtime without forcing a framework-wide
rewrite. A real LangGraph adapter can be added later behind the same interfaces.
"""

from .state import AgentState
from .graph import WorkflowGraph, build_default_graph
from .router import route_request

__all__ = ["AgentState", "WorkflowGraph", "build_default_graph", "route_request"]
