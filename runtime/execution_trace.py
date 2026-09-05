"""ANT runtime execution tracing.

Tracks lifecycle events for debugging and observability.
"""


class ExecutionTrace:
    def __init__(self):
        self.events = []

    def record(self, stage, data=None):
        self.events.append({"stage": stage, "data": data})

    def history(self):
        return self.events
