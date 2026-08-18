from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List

from .state import AgentState

NodeFn = Callable[[AgentState], AgentState]


@dataclass
class WorkflowGraph:
    nodes: Dict[str, NodeFn] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)

    def add_node(self, name: str, fn: NodeFn) -> "WorkflowGraph":
        self.nodes[name] = fn
        self.edges.setdefault(name, [])
        return self

    def add_edge(self, source: str, target: str) -> "WorkflowGraph":
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("Both graph nodes must exist before adding an edge")
        self.edges.setdefault(source, []).append(target)
        return self

    def run(self, state: AgentState, start: str = "planner", max_steps: int = 32) -> AgentState:
        current = start
        steps = 0
        while current and steps < max_steps:
            steps += 1
            state.current_node = current
            fn = self.nodes[current]
            state = fn(state)
            next_nodes = self.edges.get(current, [])
            if not next_nodes:
                break
            current = next_nodes[0]
        if steps >= max_steps:
            state.fail("workflow exceeded max_steps")
        return state


def build_default_graph() -> WorkflowGraph:
    """Return a minimal graph; integration nodes are intentionally injectable."""
    def planner(state: AgentState) -> AgentState:
        state.execution_plan = [{"agent": "master_agent", "task": state.user_input}]
        return state

    def verifier(state: AgentState) -> AgentState:
        state.verification_results = {"status": "pending", "errors": state.errors}
        return state

    def synthesizer(state: AgentState) -> AgentState:
        if state.final_response is None:
            state.final_response = "Workflow completed with no synthesizer output configured."
        return state

    return (WorkflowGraph()
            .add_node("planner", planner)
            .add_node("verifier", verifier)
            .add_node("synthesizer", synthesizer)
            .add_edge("planner", "verifier")
            .add_edge("verifier", "synthesizer"))
