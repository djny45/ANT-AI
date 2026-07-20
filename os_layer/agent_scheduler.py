"""ANT AI agent scheduling."""

class AgentScheduler:
    def __init__(self):
        self.queue = []

    def add(self, task):
        self.queue.append(task)

    def next_task(self):
        return self.queue.pop(0) if self.queue else None
