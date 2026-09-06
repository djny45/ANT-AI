"""NOVA Core v0.3 Cognitive Pipeline
Basic end-to-end intelligence flow.
"""


class CognitivePipeline:
    def __init__(self, controller):
        self.controller = controller

    def process(self, goal):
        return self.controller.run(goal)
