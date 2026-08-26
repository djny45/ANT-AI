"""
ANT AI Harness request validation layer.

Validates incoming API payloads before execution enters the
orchestration pipeline.
"""


def validate_request(payload):
    """Validate required request structure."""
    if not isinstance(payload, dict):
        return {
            "valid": False,
            "error": "Request payload must be an object"
        }

    if "input" not in payload:
        return {
            "valid": False,
            "error": "Missing required field: input"
        }

    return {
        "valid": True,
        "error": None
    }
