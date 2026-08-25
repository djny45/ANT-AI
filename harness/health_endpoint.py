"""
ANT AI Harness health endpoint layer.

Exposes service readiness information for API integration.
"""

from .health import get_health_status


def health_endpoint():
    """Return current Harness health state."""
    return get_health_status()
