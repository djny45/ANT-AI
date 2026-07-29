class TaskQueue:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def next(self):
        return self.tasks.pop(0) if self.tasks else None
