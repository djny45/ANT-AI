"""ANT AI permission management."""

class PermissionManager:
    def check(self, action, permissions):
        return {
            "action": action,
            "permissions": permissions,
            "approved": False,
            "review_required": True
        }
