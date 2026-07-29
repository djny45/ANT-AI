from dataclasses import dataclass
from typing import Any

@dataclass
class AgentResult:
    success: bool
    output: Any
    error: str | None = None

class Agent:
    def __init__(self, name: str):
        self.name = name

    def run(self, task: str) -> AgentResult:
        return AgentResult(True, task)
