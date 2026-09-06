"""NOVA Core minimal command interface."""

from nova_core.pipeline.cognitive_pipeline import CognitivePipeline


def run(command: str):
    pipeline = CognitivePipeline()
    return pipeline.execute(command)


if __name__ == "__main__":
    print("NOVA CORE ONLINE")
    print("Type an objective to run the cognitive pipeline")
    while True:
        user_input = input("nova> ")
        if user_input.lower() in {"exit", "quit"}:
            break
        print(run(user_input))
