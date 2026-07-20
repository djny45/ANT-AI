"""ANT AI task routing system."""

class TaskRouter:
    def route(self, task):
        if "code" in task.lower():
            return "coding_ant"
        if "research" in task.lower():
            return "research_ant"
        if "security" in task.lower():
            return "security_ant"
        return "commander"
