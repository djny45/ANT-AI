class PatchGenerator:
    def create_patch(self, issue):
        return {
            "issue": issue,
            "requires_review": True,
            "status": "draft"
        }
