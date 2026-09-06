"""NOVA Core v0.1 minimal runtime bootstrap.

Foundation runtime for the first executable NOVA intelligence loop.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RuntimeState:
    status: str = "OFFLINE"
    agents: list = field(default_factory=list)
    memories: list = field(default_factory=list)


class NOVARuntime:
    def __init__(self):
        self.state = RuntimeState()

    def boot(self):
        self.state.status = "ONLINE"
        return "NOVA CORE ONLINE"

    def create_agent(self, name, capability):
        agent = {
            "id": f"NOVA-{len(self.state.agents)+1:03d}",
            "name": name,
            "capability": capability,
            "created": datetime.utcnow().isoformat(),
        }
        self.state.agents.append(agent)
        return agent

    def remember(self, experience):
        self.state.memories.append(experience)

    def status(self):
        return {
            "runtime": self.state.status,
            "agents": len(self.state.agents),
            "memories": len(self.state.memories),
        }
