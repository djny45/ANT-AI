"""ANT web to app generation layer."""

class AppGenerator:
    def generate(self, project):
        return {
            "project": project,
            "platform": "android",
            "status": "generated_draft"
        }
