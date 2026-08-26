"""
ANT AI deployment readiness checks.

Provides a lightweight validation layer for production preparation.
"""

from typing import Dict, List


REQUIRED_COMPONENTS = [
    "api",
    "pipeline",
    "runtime_controller",
    "memory_context",
    "telemetry",
]


def check_readiness(available_components: List[str]) -> Dict[str, object]:
    missing = [
        component
        for component in REQUIRED_COMPONENTS
        if component not in available_components
    ]

    return {
        "ready": len(missing) == 0,
        "missing_components": missing,
    }
