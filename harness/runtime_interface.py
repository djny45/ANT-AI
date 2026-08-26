"""
ANT AI runtime interface layer.

Defines the contract between orchestration services and the intelligence runtime.
Model/provider specific implementations must remain outside this interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class RuntimeInterface(ABC):
    """Abstract runtime contract for AI execution."""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a runtime task using provided context."""
        raise NotImplementedError
