import os


class Config:
    def __init__(self):
        self.environment = os.getenv("ANT_ENV", "development")
        self.memory_backend = os.getenv("MEMORY_BACKEND", "qdrant")
        self.model_provider = os.getenv("MODEL_PROVIDER", "local")
        self.debug = self.environment != "production"


config = Config()
