"""ANT AI knowledge graph entities."""

class EntityGraph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_entity(self, entity):
        self.nodes.append(entity)

    def connect(self, source, target, relation):
        self.links.append({
            "source": source,
            "target": target,
            "relation": relation
        })
