class GitHubMonitor:
    def watch(self, repositories):
        return {
            "repositories": repositories,
            "status": "monitoring"
        }
