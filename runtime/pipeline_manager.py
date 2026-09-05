"""ANT-AI pipeline coordinator."""


class PipelineManager:
    def __init__(self):
        self.stages = []

    def register_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        for stage in self.stages:
            context = stage(context)
        return context
