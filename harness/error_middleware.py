"""
ANT AI Harness API error handling middleware.

Provides standardized exception handling and response formatting
for production API request management.
"""


def handle_error(error):
    """Convert internal exceptions into structured API responses."""
    return {
        "status": "error",
        "error_type": error.__class__.__name__,
        "message": str(error),
    }


class HarnessErrorMiddleware:
    def process(self, operation):
        """Execute operation with controlled error handling."""
        try:
            return operation()
        except Exception as error:
            return handle_error(error)
