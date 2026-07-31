from dataclasses import dataclass, field
from typing import Dict, Any

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
        self.agents = {}

    def register(self, agent: AgentWorker):
        self.agents[agent.name] = agent

    def dispatch(self, agent_name: str, task: str):
        return self.agents[agent_name].execute(task)
