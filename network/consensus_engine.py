"""ANT AI distributed decision consensus."""

class ConsensusEngine:
    def decide(self, votes):
        if not votes:
            return None
        result = {}
        for vote in votes:
            result[vote] = result.get(vote, 0) + 1
        return max(result, key=result.get)
