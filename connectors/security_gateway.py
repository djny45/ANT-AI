"""ANT AI connector permission gateway."""

class SecurityGateway:
    def validate(self, connector, permissions):
        return {
            "connector": connector,
            "permissions": permissions,
            "approved": False,
            "review_required": True
        }
