"""
ANT-AI Unified Runtime Result Handler

Responsible for normalizing execution outputs,
tracking status, and preparing runtime responses.
"""


class ResultHandler:
    def __init__(self):
        self.history = []

    def success(self, result, context=None):
        response = {
            "status": "completed",
            "result": result,
            "context": context,
        }
        self.history.append(response)
        return response

    def failure(self, error, context=None):
        response = {
            "status": "failed",
            "error": str(error),
            "context": context,
        }
        self.history.append(response)
        return response

    def latest(self):
        if not self.history:
            return None
        return self.history[-1]
