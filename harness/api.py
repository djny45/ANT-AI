"""
ANT AI Harness HTTP API layer.

Provides the boundary between frontend clients and the internal
Harness execution pipeline.
"""

from .execution_service import HarnessExecutionService
from .api_registry import initialize_api_registry
from .error_middleware import handle_api_error


ROUTES = initialize_api_registry()
execution_service = HarnessExecutionService()


@handle_api_error
def handle_request(payload):
    """Receive frontend request and execute through the harness pipeline."""
    result = execution_service.execute(payload)
    return {
        "status": "completed",
        "message": "Request processed by ANT AI Harness",
        "result": result,
    }


@handle_api_error
def health_check():
    """Basic service health response."""
    return ROUTES["GET /health"]()
