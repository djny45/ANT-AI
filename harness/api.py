"""
ANT AI Harness HTTP API layer.

Provides the boundary between frontend clients and the internal
Harness execution pipeline.
"""


def handle_request(payload):
    """Receive frontend request and pass it to the harness pipeline."""
    return {
        "status": "accepted",
        "message": "Request received by ANT AI Harness",
        "input": payload,
    }


def health_check():
    """Basic service health response."""
    return {
        "service": "ANT AI Harness",
        "status": "online",
    }
