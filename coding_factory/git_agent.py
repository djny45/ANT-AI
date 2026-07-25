"""ANT AI Git management agent."""

class GitAgent:
    def prepare_commit(self, changes):
        return {
            "changes": changes,
            "status": "review_before_commit"
        }
