"""ANT AI skill registry."""

import re


class SkillRegistry:
    def __init__(self):
        self.registry = []

    def add(self, skill):
        self.registry.append(skill)

    def search(self, keyword):
        """Return registered skills whose text matches the keyword or stem."""
        query = str(keyword).strip().lower()
        if not query:
            return []

        def normalize(value: str) -> str:
            return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

        normalized_query = normalize(query)
        query_tokens = normalized_query.split()
        results = []
        for skill in self.registry:
            text = normalize(str(skill))
            if normalized_query in text:
                results.append(skill)
                continue
            words = text.split()
            if any(
                token and any(word.startswith(token) or token.startswith(word) for word in words)
                for token in query_tokens
            ):
                results.append(skill)
        return results
