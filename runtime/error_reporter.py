"""ANT runtime error reporting utilities."""


class ErrorReporter:
    def __init__(self):
        self.errors = []

    def report(self, error, context=None):
        self.errors.append({"error": str(error), "context": context})

    def get_errors(self):
        return self.errors
