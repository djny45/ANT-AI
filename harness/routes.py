"""
ANT AI Harness route registration layer.

Provides route bindings between HTTP API and Harness services.
"""

from .health_endpoint import health_status


def register_routes():
    """Register Harness HTTP routes."""
    return {
        "GET /health": health_status
    }
