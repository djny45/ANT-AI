class ResearchAnt:
    name = "Research Ant"

    def execute(self, task):
        return {
            "agent": self.name,
            "task": task,
            "status": "research_pending"
        }
