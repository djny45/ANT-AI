"""ANT AI runtime validation layer.

Validates execution context before passing requests to the runtime controller.
"""


class RuntimeValidation:
    def validate(self, context):
        if not isinstance(context, dict):
            return {
                "valid": False,
                "error": "invalid_context_type",
            }

        if "request" not in context:
            return {
                "valid": False,
                "error": "missing_request_context",
            }

        return {
            "valid": True,
            "error": None,
        }
