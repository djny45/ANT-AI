"""ANT AI open source repository scout."""

class OpenSourceScout:
    def __init__(self):
        self.repositories = []

    def add_candidate(self, repo):
        self.repositories.append(repo)

    def evaluate(self, repo):
        return {
            "repository": repo,
            "checks": [
                "activity",
                "license",
                "security",
                "usefulness"
            ],
            "status": "pending_review"
        }

    def recent_candidates(self):
        return self.repositories
