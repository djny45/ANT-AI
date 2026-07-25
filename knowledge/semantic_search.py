"""ANT AI semantic search layer."""

class SemanticSearch:
    def find(self, query, memory):
        return {
            "query": query,
            "results": memory
        }
