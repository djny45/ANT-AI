"""ANT AI internal task marketplace."""

class TaskMarket:
    def __init__(self):
        self.tasks = []

    def publish(self, task):
        self.tasks.append(task)

    def available(self):
        return self.tasks
