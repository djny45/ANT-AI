"""ANT Runtime Health Checks"""

class HealthCheck:
    def check(self):
        return {
            "runtime": "ok",
            "services": "ready"
        }
