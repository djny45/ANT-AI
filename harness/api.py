"""
ANT AI Harness HTTP API layer.

Provides the boundary between frontend clients and the internal
Harness execution pipeline.
"""

from .execution_service import HarnessExecutionService
from .routes import register_routes


ROUTES = register_routes()
execution_service = HarnessExecutionService()


def handle_request(payload):
    """Receive frontend request and execute through the harness pipeline."""
    result = execution_service.execute(payload)
    return {
        "status": "completed",
        "message": "Request processed by ANT AI Harness",
        "result": result,
    }


def health_check():
    """Basic service health response."""
    return ROUTES["GET /health"]()
