"""ANT AI Knowledge Hive foundation."""

from ant_common import keyword_filter


class KnowledgeHive:
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def search(self, query):
        return keyword_filter(self.documents, query)
