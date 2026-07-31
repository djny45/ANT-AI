class QdrantAdapter:
    def __init__(self, client=None, collection="antx_memory"):
        self.client = client
        self.collection = collection

    def store(self, vector, payload):
        return {"stored": True, "payload": payload}

    def search(self, vector, limit=5):
        return []
