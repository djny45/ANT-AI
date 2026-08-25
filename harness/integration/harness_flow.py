"""
ANT AI Harness Flow Integration

Connects API execution flow with the Harness pipeline components.
"""

from dataclasses import dataclass


@dataclass
class HarnessResult:
    success: bool
    output: str


class HarnessFlow:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline

    def execute(self, request: dict) -> HarnessResult:
        if self.pipeline:
            result = self.pipeline.run(request)
            return HarnessResult(success=True, output=str(result))

        return HarnessResult(
            success=True,
            output="Harness flow initialized"
        )
