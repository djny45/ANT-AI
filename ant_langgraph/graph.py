import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from .state import AgentState

NodeFn = Callable[[AgentState], AgentState]


@dataclass
class WorkflowGraph:
    """Small, dependency-free workflow graph for one unified ANT intelligence run."""

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
    """Form temporary internal capabilities from one ANT intelligence request."""
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


def _risk_score(capabilities: List[str]) -> int:
    score = min(100, len(capabilities) * 15)
    if any(capability in {"security", "coding"} for capability in capabilities):
        score = min(100, score + 10)
    return score


def build_default_graph() -> WorkflowGraph:
    """Build the default execution path for the single ANT intelligence."""

    def understand(state: AgentState) -> AgentState:
        state.audit_metadata["task_type"] = "general"
        return state

    def plan(state: AgentState) -> AgentState:
        capabilities = _classify_capabilities(state.user_input)
        state.selected_capabilities = capabilities
        state.execution_plan = [
            {"capability": capability, "task": state.user_input}
            for capability in capabilities
        ]
        state.audit_metadata["capability_count"] = len(capabilities)
        state.audit_metadata["risk_score"] = _risk_score(capabilities)
        state.audit_metadata["fast_path"] = capabilities == ["reasoning"]
        return state

    def execute(state: AgentState) -> AgentState:
        """Govern once, then execute independent temporary capabilities concurrently."""
        from governance_engine.governance.approval_flow import ApprovalFlow
        from intelligence.ollama_connector import OllamaConnector
        from intelligence.openrouter_connector import OpenRouterConnector

        decision = ApprovalFlow().evaluate(int(state.audit_metadata.get("risk_score", 0)))
        state.audit_metadata["governance_approved"] = decision.approved
        state.audit_metadata["governance_reason"] = decision.reason
        if not decision.approved:
            state.fail(decision.reason)
            return state

        provider = os.getenv("ANT_MODEL_PROVIDER", "ollama").strip().lower()
        if provider == "openrouter":
            model_runtime = OpenRouterConnector()
            model_name = model_runtime.default_model
        else:
            provider = "ollama"
            model_runtime = OllamaConnector()
            model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

        state.audit_metadata["model_provider"] = provider
        state.audit_metadata["model"] = model_name

        def execute_capability(item: Dict[str, str]):
            capability = item["capability"]
            if capability == "reasoning":
                prompt = (
                    "You are the full ANT Intelligence Core. Answer the user's request directly. "
                    "Do not describe internal capabilities or simulate separate agents.\n"
                    f"User request: {item['task']}"
                )
            else:
                prompt = (
                    "You are the full ANT Intelligence Core temporarily focusing on one internal capability. "
                    f"Current capability: {capability}.\n"
                    "Work only on the user's request and return concise, useful findings.\n"
                    f"User request: {item['task']}"
                )
            return capability, model_runtime.generate(prompt)

        started_results: Dict[str, dict] = {}
        if len(state.execution_plan) == 1:
            capability, result = execute_capability(state.execution_plan[0])
            started_results[capability] = result
        else:
            with ThreadPoolExecutor(max_workers=len(state.execution_plan)) as pool:
                futures = [pool.submit(execute_capability, item) for item in state.execution_plan]
                for future in as_completed(futures):
                    capability, result = future.result()
                    started_results[capability] = result

        total_latency = 0.0
        for item in state.execution_plan:
            capability = item["capability"]
            result = started_results[capability]
            if result.get("error"):
                state.fail(f"{capability}: model execution failed: {result['error']}")
                state.record_result(capability, result, confidence=0.0)
            else:
                state.record_result(capability, result, confidence=0.8)
            total_latency = max(total_latency, float(result.get("latency_ms", 0.0)))

        state.audit_metadata["latency_ms"] = total_latency
        state.audit_metadata["parallel_execution"] = len(state.execution_plan) > 1
        return state

    def verify(state: AgentState) -> AgentState:
        successful = [r for r in state.capability_results if r.get("result", {}).get("response")]
        state.verification_results = {
            "status": "passed" if successful and not state.errors else "failed",
            "capabilities_checked": list(state.selected_capabilities),
            "successful_capabilities": [r["capability"] for r in successful],
            "errors": list(state.errors),
            "governance_approved": state.audit_metadata.get("governance_approved", False),
        }
        return state

    def synthesize(state: AgentState) -> AgentState:
        if state.errors and not state.capability_results:
            state.final_response = "ANT could not complete the request safely: " + "; ".join(state.errors)
            return state

        responses = []
        for item in state.capability_results:
            response = item.get("result", {}).get("response")
            if response:
                if state.audit_metadata.get("fast_path"):
                    responses.append(response)
                else:
                    responses.append(f"[{item['capability']}] {response}")

        if not responses:
            state.final_response = "ANT could not generate a model response. Check the configured model runtime."
        else:
            state.final_response = "\n\n".join(responses)
            if state.errors:
                state.final_response += "\n\nSome internal capabilities failed and were excluded from the final result."
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
