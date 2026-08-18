from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class ToolSpec:
    name: str
    owner_agent: str
    permission: str
    risk_level: int = 0
    handler: Callable[..., Any] | None = None


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.risk_level < 0 or spec.risk_level > 100:
            raise ValueError("risk_level must be 0..100")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        return self._tools[name]

    def list(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def execute(self, name: str, agent: str, **kwargs: Any) -> Any:
        spec = self.get(name)
        if spec.owner_agent != agent:
            raise PermissionError(f"Agent {agent} cannot use tool {name}")
        if spec.handler is None:
            raise RuntimeError(f"Tool {name} has no execution handler")
        return spec.handler(**kwargs)
