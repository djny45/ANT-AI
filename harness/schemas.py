"""Request and response schemas for ANT AI Harness API.

Defines the contract between the frontend and the execution pipeline.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class HarnessRequest:
    task: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HarnessResponse:
    status: str
    result: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
