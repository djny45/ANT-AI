"""Small enhancements to core memory to record workflows and skill usage."""
class Memory:
    def __init__(self):
        self.short_term = []
        self.long_term = []
        self.workflows = []

    def store(self, item, permanent=False):
        if permanent:
            self.long_term.append(item)
        else:
            self.short_term.append(item)

    def retrieve(self):
        return self.short_term + self.long_term

    def store_workflow(self, workflow: dict, permanent=False):
        # workflow should include selected skills, results, and status
        self.workflows.append(workflow)
        if permanent:
            self.long_term.append({"workflow": workflow})

    def retrieve_workflows(self):
        return list(self.workflows)
