import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

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


SANDBOX_TOOL = {
    "type": "function",
    "function": {
        "name": "sandbox",
        "description": (
            "Use ANT's isolated per-run sandbox. You may create and inspect files in the "
            "writable workspace and read the current ANT repository snapshot read-only. "
            "Never assume access to the host filesystem or write to the repository snapshot."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "list_files", "read_file", "write_file", "check_python",
                        "repo_list_files", "repo_read_file",
                    ],
                },
                "path": {
                    "type": "string",
                    "description": "Relative workspace or repository path, depending on operation.",
                },
                "content": {"type": "string", "description": "UTF-8 content for write_file."},
            },
            "required": ["operation"],
            "additionalProperties": False,
        },
    },
}


def build_default_graph() -> WorkflowGraph:
    """Build the default execution path using OpenRouter as the model runtime."""

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
        from intelligence.openrouter_connector import OpenRouterConnector
        from sandbox.client import RemoteSandbox, RemoteSandboxError
        from sandbox.runtime import SandboxError, SkillSandbox

        decision = ApprovalFlow().evaluate(int(state.audit_metadata.get("risk_score", 0)))
        state.audit_metadata["governance_approved"] = decision.approved
        state.audit_metadata["governance_reason"] = decision.reason
        if not decision.approved:
            state.fail(decision.reason)
            return state

        request_api_key = str(state.user_context.get("openrouter_api_key", "")).strip()
        selected_model = str(state.user_context.get("openrouter_model", "")).strip()
        model_runtime = OpenRouterConnector(api_key=request_api_key or None)
        model_name = selected_model or model_runtime.default_model
        state.audit_metadata["model_provider"] = "openrouter"
        state.audit_metadata["model"] = model_name

        def generate(runtime: Any, prompt: str, model: str) -> dict:
            """Call real or lightweight fake runtimes without forcing a model kwarg."""
            try:
                return runtime.generate(prompt, model=model)
            except TypeError as exc:
                if "unexpected keyword argument 'model'" not in str(exc):
                    raise
                return runtime.generate(prompt)

        def execute_capability(item: Dict[str, str]):
            capability = item["capability"]
            prompt = (
                "You are the full ANT Intelligence Core. Do not describe separate agents.\n"
                f"Current temporary capability: {capability}.\n"
                "Work on the user's request and return useful findings.\n"
                f"User request: {item['task']}"
            )

            if capability not in {"coding", "testing"}:
                return capability, generate(model_runtime, prompt, model_name), 0

            execution_id = str(state.audit_metadata.get("execution_id", "ant-run"))
            remote_url = os.getenv("ANT_SANDBOX_URL", "").strip()
            if remote_url:
                sandbox = RemoteSandbox(execution_id=execution_id, url=remote_url)
            else:
                sandbox = SkillSandbox(execution_id=execution_id)

            def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
                if name != "sandbox":
                    return {"error": f"tool not allowed: {name}"}
                try:
                    return sandbox.execute(**arguments)
                except (SandboxError, RemoteSandboxError, TypeError, ValueError) as exc:
                    return {"error": str(exc)}

            prompt += (
                "\nYou have access to the ANT sandbox tool. Use it when needed to create, "
                "inspect, or syntax-check files. You may read the ANT repository through "
                "repo_list_files/repo_read_file, but repository files are read-only. "
                "Keep generated work inside the writable workspace."
            )
            try:
                if not hasattr(model_runtime, "generate_with_tools"):
                    result = generate(model_runtime, prompt, model_name)
                    return capability, result, 0
                result = model_runtime.generate_with_tools(
                    prompt=prompt,
                    model=model_name,
                    tools=[SANDBOX_TOOL],
                    tool_executor=execute_tool,
                    max_tool_calls=int(os.getenv("ANT_MAX_SANDBOX_TOOL_CALLS", "3")),
                )
                return capability, result, int(result.get("tool_calls", 0))
            finally:
                # Each coding/testing capability owns its sandbox lifecycle.
                # Always stop it so an execution cannot leak a running VM.
                close = getattr(sandbox, "close", None)
                if callable(close):
                    close()

        started_results: Dict[str, dict] = {}
        tool_call_count = 0
        if len(state.execution_plan) == 1:
            capability, result, calls = execute_capability(state.execution_plan[0])
            started_results[capability] = result
            tool_call_count += calls
        else:
            with ThreadPoolExecutor(max_workers=len(state.execution_plan)) as pool:
                futures = [pool.submit(execute_capability, item) for item in state.execution_plan]
                for future in as_completed(futures):
                    capability, result, calls = future.result()
                    started_results[capability] = result
                    tool_call_count += calls

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

        state.audit_metadata["sandbox_tool_calls"] = tool_call_count
        state.audit_metadata["sandbox_mode"] = "remote" if os.getenv("ANT_SANDBOX_URL", "").strip() else "local-bounded"
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
            "sandbox_tool_calls": int(state.audit_metadata.get("sandbox_tool_calls", 0)),
            "sandbox_mode": state.audit_metadata.get("sandbox_mode", "disabled"),
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
            state.final_response = "ANT could not generate a model response. Check the OpenRouter configuration."
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