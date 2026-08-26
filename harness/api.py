"""
ANT AI Harness HTTP API layer.

Provides the boundary between frontend clients and the internal
Harness execution pipeline.
"""

from .execution_service import HarnessExecutionService
from .api_registry import initialize_api_registry
from .error_middleware import handle_api_error
from .response_models import success_response
from .request_validation import validate_request


ROUTES = initialize_api_registry()
execution_service = HarnessExecutionService()


@handle_api_error
def handle_request(payload):
    """Receive validated frontend request and execute through the harness pipeline."""
    validate_request(payload)
    result = execution_service.execute(payload)
    return success_response(
        result=result,
        message="Request processed by ANT AI Harness",
    )


@handle_api_error
def health_check():
    """Basic service health response."""
    return ROUTES["GET /health"]()
