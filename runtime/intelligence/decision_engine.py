"""ANT decision engine foundation.

Coordinates future autonomous decision policies.
"""


class DecisionEngine:
    def decide(self, options):
        if not options:
            return None
        return options[0]
