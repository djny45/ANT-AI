"""ANT AI skill registry."""

import re


class SkillRegistry:
    def __init__(self):
        self.registry = []

    def add(self, skill):
        self.registry.append(skill)

    def search(self, keyword):
        """Return registered skills relevant to the supplied search terms."""
        query = str(keyword).strip().lower()
        if not query:
            return []

        def normalize(value: str) -> str:
            return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

        query_tokens = [token for token in normalize(query).split() if token not in {"skill", "skills"}]
        results = []
        for skill in self.registry:
            words = normalize(str(skill)).split()
            if not query_tokens:
                if normalize(query) in normalize(str(skill)):
                    results.append(skill)
                continue
            if all(
                any(word.startswith(token) or token.startswith(word) for word in words)
                for token in query_tokens
            ):
                results.append(skill)
        return results
