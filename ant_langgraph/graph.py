from dataclasses import dataclass, field
from typing import Callable, Dict, List

from .state import AgentState

NodeFn = Callable[[AgentState], AgentState]


@dataclass
class WorkflowGraph:
    """Small, dependency-free workflow graph used by the ANT execution boundary."""

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

    def run(self, state: AgentState, start: str = "understand", max_steps: int = 32) -> AgentState:
        current = start
        steps = 0
        while current and steps < max_steps:
            steps += 1
            state.current_node = current
            state = self.nodes[current](state)
            next_nodes = self.edges.get(current, [])
            if not next_nodes:
                break
            current = next_nodes[0]
        if steps >= max_steps:
            state.fail("workflow exceeded max_steps")
        return state


def _classify_capabilities(user_input: str) -> List[str]:
    """Form temporary cognitive capabilities from a request; no permanent agents are created."""
    text = user_input.lower()
    capabilities: List[str] = []
    if any(word in text for word in ("research", "analyze", "compare", "investigate")):
        capabilities.append("research")
    if any(word in text for word in ("code", "coding", "build", "implement", "debug", "develop")):
        capabilities.append("coding")
    if any(word in text for word in ("security", "secure", "vulnerability", "audit")):
        capabilities.append("security")
    if any(word in text for word in ("test", "testing", "validate")):
        capabilities.append("testing")
    return capabilities or ["reasoning"]


def build_default_graph() -> WorkflowGraph:
    """Build the default unified-intelligence execution path."""
    def understand(state: AgentState) -> AgentState:
        state.audit_metadata["task_type"] = "general"
        return state

    def plan(state: AgentState) -> AgentState:
        capabilities = _classify_capabilities(state.user_input)
        state.selected_agents = capabilities
        state.execution_plan = [
            {"capability": capability, "task": state.user_input}
            for capability in capabilities
        ]
        state.audit_metadata["capability_count"] = len(capabilities)
        return state

    def execute(state: AgentState) -> AgentState:
        """Execute formed capabilities using the local model when available."""
        from intelligence.ollama_connector import OllamaConnector

        connector = OllamaConnector()
        for item in state.execution_plan:
            capability = item["capability"]
            prompt = (
                "You are a temporary cognitive capability inside ANT AI. "
                f"Capability: {capability}.\n"
                "Work only on the user's request and return concise, useful findings.\n"
                f"User request: {item['task']}"
            )
            result = connector.generate(prompt)
            if result.get("error"):
                state.fail(f"{capability}: model execution failed: {result['error']}")
                state.record_result(capability, result, confidence=0.0)
            else:
                state.record_result(capability, result, confidence=0.8)
                state.audit_metadata.setdefault("latency_ms", 0.0)
                state.audit_metadata["latency_ms"] += result.get("latency_ms", 0.0)
        return state

    def verify(state: AgentState) -> AgentState:
        successful = [r for r in state.agent_results if r.get("result", {}).get("response")]
        state.verification_results = {
            "status": "passed" if successful and not state.errors else "failed",
            "capabilities_checked": list(state.selected_agents),
            "successful_capabilities": [r["agent"] for r in successful],
            "errors": list(state.errors),
        }
        return state

    def synthesize(state: AgentState) -> AgentState:
        if state.errors and not state.agent_results:
            state.final_response = "ANT could not complete the request safely: " + "; ".join(state.errors)
            return state

        responses = []
        for item in state.agent_results:
            response = item.get("result", {}).get("response")
            if response:
                responses.append(f"[{item['agent']}] {response}")

        if not responses:
            state.final_response = "ANT could not generate a model response. Check local Ollama availability."
        else:
            state.final_response = "\n\n".join(responses)
            if state.errors:
                state.final_response += "\n\nSome capabilities failed and were excluded from the final result."
        return state

    return (
        WorkflowGraph()
        .add_node("understand", understand)
        .add_node("planner", plan)
        .add_node("execute", execute)
        .add_node("verifier", verify)
        .add_node("synthesizer", synthesize)
        .add_edge("understand", "planner")
        .add_edge("planner", "execute")
        .add_edge("execute", "verifier")
        .add_edge("verifier", "synthesizer")
    )
