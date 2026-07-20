"""ANT AI knowledge graph query layer."""

class QueryEngine:
    def search(self, query, graph):
        return {
            "query": query,
            "results": graph
        }
