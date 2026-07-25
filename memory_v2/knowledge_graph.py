"""ANT AI knowledge graph foundation."""

class KnowledgeGraph:
    def __init__(self):
        self.nodes = []

    def add_relation(self, subject, relation, object):
        self.nodes.append({"subject": subject, "relation": relation, "object": object})

    def query(self, subject):
        return [n for n in self.nodes if n["subject"] == subject]
