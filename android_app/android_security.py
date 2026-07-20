"""ANT AI Android security controls."""

class AndroidSecurity:
    def check_permission(self, permission):
        return {
            "permission": permission,
            "allowed": False,
            "review": True
        }
