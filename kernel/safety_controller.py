"""ANT AI safety control layer."""

class SafetyController:
    def approve(self, action):
        return {
            "action": action,
            "approved": False,
            "requires_review": True
        }
