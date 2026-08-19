from dataclasses import dataclass
from typing import Dict, Any

from ant_common import Registry

@dataclass
class AgentWorker:
    name: str
    role: str
    status: str = "idle"

    def execute(self, task: str) -> Dict[str, Any]:
        self.status = "working"
        result = {"agent": self.name, "task": task, "status": "completed"}
        self.status = "idle"
        return result


class AgentArmyCoordinator:
    def __init__(self):
        self._registry: Registry[AgentWorker] = Registry()

    @property
    def agents(self) -> Dict[str, AgentWorker]:
        return self._registry.mapping

    def register(self, agent: AgentWorker):
        self._registry.register(agent.name, agent)

    def dispatch(self, agent_name: str, task: str):
        return self._registry.mapping[agent_name].execute(task)
