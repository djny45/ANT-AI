"""
ANT AI Harness API response models.

Defines standardized response structures for API consumers.
"""


class APIResponse:
    def __init__(self, status, message, data=None, metadata=None):
        self.status = status
        self.message = message
        self.data = data
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "metadata": self.metadata,
        }


class ErrorResponse(APIResponse):
    def __init__(self, message, error_code=None):
        super().__init__("error", message, metadata={"error_code": error_code})
