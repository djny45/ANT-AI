"""ANT AI browser automation agent foundation."""

class BrowserAgent:
    name = "Browser Ant"

    def search(self, query):
        return {
            "agent": self.name,
            "query": query,
            "status": "ready"
        }
