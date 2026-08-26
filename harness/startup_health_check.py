"""
ANT AI startup health validation layer.

Validates required services before runtime initialization.
"""

from typing import Dict, Any


class StartupHealthCheck:
    """Checks backend readiness before startup."""

    def validate(self, components: Dict[str, Any]) -> Dict[str, Any]:
        missing = [name for name, value in components.items() if value is None]

        return {
            "ready": len(missing) == 0,
            "missing_components": missing,
        }
