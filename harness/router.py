"""ANT AI Harness routing boundary."""

from typing import Dict, Any


def route_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Route incoming requests into the harness execution pipeline."""
    return {
        "route": "unified_intelligence",
        "payload": payload,
    }
