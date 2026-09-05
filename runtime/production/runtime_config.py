"""ANT production runtime configuration."""


class RuntimeConfig:
    def __init__(self, environment="development"):
        self.environment = environment
        self.enabled = True
