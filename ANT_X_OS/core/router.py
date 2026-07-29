class Router:
    def route(self, task):
        text = task.lower()
        if "code" in text:
            return "coding_agent"
        if "research" in text:
            return "research_agent"
        return "master_agent"
