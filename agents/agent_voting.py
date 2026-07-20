"""ANT swarm decision voting."""

class AgentVoting:
    def vote(self, decisions):
        counts = {}
        for decision in decisions:
            counts[decision] = counts.get(decision, 0) + 1
        return max(counts, key=counts.get) if counts else None
