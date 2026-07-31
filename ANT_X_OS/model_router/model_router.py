class ModelRouter:
    def select(self, requirements):
        if requirements.get("privacy"):
            return "local_model"
        return "cloud_model"
