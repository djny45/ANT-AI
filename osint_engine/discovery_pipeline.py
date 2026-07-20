"""ANT OSINT discovery pipeline."""

class DiscoveryPipeline:
    def process(self, sources):
        return {
            "sources": sources,
            "status": "queued"
        }
