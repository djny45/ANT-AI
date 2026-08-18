"""
ANT-X-OS Bridge

Integration adapter between the LangGraph-style orchestration runtime and
existing ANT-X-OS components.

This layer keeps existing agents, memory, governance and tools intact while
allowing graph execution to become the top-level workflow controller.
"""

from typing import Any, Dict


class ANTXOSBridge:
    """Adapter for existing ANT AI runtime components."""

    def __init__(self, master_runtime=None, agent_registry=None, memory=None, audit=None):
        self.master_runtime = master_runtime
        self.agent_registry = agent_registry
        self.memory = memory
        self.audit = audit

    def execute_agent(self, agent_name: str, task: Dict[str, Any]):
        if not self.agent_registry:
            return {"status": "registry_unavailable", "agent": agent_name}

        agent = self.agent_registry.get(agent_name)
        if not agent:
            return {"status": "agent_not_found", "agent": agent_name}

        result = agent.run(task)

        if self.audit:
            self.audit.record({
                "agent": agent_name,
                "task": task,
                "result": result,
            })

        return result

    def remember(self, data: Dict[str, Any]):
        if self.memory:
            return self.memory.store(data)
        return None


__all__ = ["ANTXOSBridge"]
