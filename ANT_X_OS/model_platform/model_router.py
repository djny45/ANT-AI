class ModelRouter:
    def select(self, task, requirements=None):
        requirements = requirements or {}

        if requirements.get("privacy"):
            return "local_model"

        if requirements.get("speed"):
            return "fast_model"

        if "code" in task.lower():
            return "coding_model"

        return "general_model"
