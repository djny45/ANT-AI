from runtime.runtime import ANTXRuntime
from runtime.config import config


def start(master_agent, memory, tools):
    runtime = ANTXRuntime(master_agent, memory, tools)
    return runtime


if __name__ == "__main__":
    print(f"ANT-X starting in {config.environment} mode")
