class CodingAnt:
    name = "Coding Ant"

    def execute(self, task):
        return {
            "agent": self.name,
            "task": task,
            "status": "coding_pending"
        }
