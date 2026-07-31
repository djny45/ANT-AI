class EmbeddingPipeline:
    def __init__(self, encoder=None):
        self.encoder = encoder

    def encode(self, text):
        if self.encoder:
            return self.encoder(text)
        return []

    def build_record(self, text, metadata=None):
        return {
            "text": text,
            "metadata": metadata or {},
            "vector": self.encode(text)
        }
