from dataclasses import dataclass, field
from typing import Any, Protocol

class ExecutableAgent(Protocol):
    async def execute(self, task: dict[str, Any]) -> Any: ...

@dataclass
class AgentProfile:
    name: str
    mission: str = ""
    capabilities: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    memory_scope: str = "task"
    health: str = "unknown"
    executions: int = 0
    failures: int = 0

class AgentRuntime:
    def __init__(self, profile: AgentProfile, implementation: ExecutableAgent | None = None):
        self.profile = profile
        self.implementation = implementation

    async def execute(self, task: dict[str, Any]) -> Any:
        if self.implementation is None:
            raise RuntimeError(f"No implementation registered for {self.profile.name}")
        self.profile.executions += 1
        try:
            result = await self.implementation.execute(task)
            self.profile.health = "healthy"
            return result
        except Exception:
            self.profile.failures += 1
            self.profile.health = "degraded"
            raise
