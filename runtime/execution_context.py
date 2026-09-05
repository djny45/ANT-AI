"""ANT-AI execution context.

Carries task state through the runtime pipeline.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ExecutionContext:
    goal: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    status: str = "initialized"

    def update_status(self, status: str):
        self.status = status
