from typing import Any

from .coding import CodingCapability
from .data import DataAnalysisCapability
from .research import ResearchCapability
from .security import SecurityCapability


def register_capability_handlers(executor: Any, skill_registry=None) -> Any:
    handlers = (
        ("coding", CodingCapability),
        ("research", ResearchCapability),
        ("security", SecurityCapability),
        ("data", DataAnalysisCapability),
    )
    for agent, capability_type in handlers:
        if agent not in executor.handlers:
            executor.register(agent, capability_type(skill_registry=skill_registry))
    return executor
