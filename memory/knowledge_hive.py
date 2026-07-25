"""ANT AI Knowledge Hive foundation."""

class KnowledgeHive:
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def search(self, query):
        return [doc for doc in self.documents if query.lower() in doc.lower()]
