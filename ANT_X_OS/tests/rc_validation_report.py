class RCValidationReport:
    def __init__(self):
        self.results = {}

    def record(self, component, status):
        self.results[component] = status

    def generate(self):
        return {
            "release": "ANT-X v0.1 RC",
            "components": self.results,
            "ready": all(self.results.values()) if self.results else False
        }
