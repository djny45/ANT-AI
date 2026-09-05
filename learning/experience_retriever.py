"""Retrieve relevant past execution experiences."""

class ExperienceRetriever:
    def retrieve(self, query, experiences=None):
        experiences = experiences or []
        return experiences[:5]
