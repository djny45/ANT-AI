"""Generate ANT runtime integration status reports."""


class IntegrationReport:
    def generate(self, validation_result):
        return {
            "status": "ready" if validation_result.get("ready") else "incomplete",
            "details": validation_result,
        }
