from dataclasses import dataclass, field
from typing import Callable, Dict, List

from ANT_X_OS.core.evaluator import Evaluator
from ANT_X_OS.core.executor import Executor as CoreExecutor
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.selector import SkillSelector
from ant_core import IntelligenceOrchestrator
from security.audit_logger import AuditLogger
from security.hash_ledger import HashLedger

from .executor import WorkflowExecutor
from .memory import MemoryAdapter
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


def build_default_graph(
    *,
    orchestrator=None,
    skill_selector=None,
    workflow_executor=None,
    core_executor=None,
    evaluator=None,
    memory=None,
    audit_logger=None,
    hash_ledger=None,
) -> WorkflowGraph:
    planner_service = orchestrator or IntelligenceOrchestrator()
    load_builtin_skills()
    selector = skill_selector or SkillSelector()
    graph_executor = workflow_executor or WorkflowExecutor()
    fallback_executor = core_executor or CoreExecutor()
    result_evaluator = evaluator or Evaluator()
    memory_adapter = memory or MemoryAdapter()
    logger = audit_logger or AuditLogger()
    ledger = hash_ledger or HashLedger()

    def planner(state: AgentState) -> AgentState:
        planned = planner_service.prepare(state.user_input, state.user_context)
        state.execution_plan = [dict(task) for task in planned.plan]
        state.selected_agents = list(planned.selected_agents)
        state.audit_metadata["decision"] = planned.context.get("decision", {})
        state.audit_metadata["planner_status"] = planned.status
        return state

    def capability(state: AgentState) -> AgentState:
        for task in state.execution_plan:
            selection_task = {
                "type": task.get("agent", ""),
                "description": task.get("objective", ""),
            }
            task["skills"] = selector.select_for_task(selection_task)
        return state

    def executor(state: AgentState) -> AgentState:
        handlers = graph_executor.handlers
        for task in state.execution_plan:
            agent = task.get("agent", "unknown")
            context = dict(state.user_context)
            context["skills"] = task.get("skills", [])
            try:
                if handlers.get(agent) is not None:
                    result = graph_executor.execute(agent, task, context)
                    outcome = {"execution_path": "workflow_executor", "result": result}
                else:
                    result = fallback_executor.execute(task)
                    outcome = {"execution_path": "core_executor", "result": result}
                state.record_result(agent, outcome)
            except Exception as error:
                state.fail(f"{agent}: {error}")
                state.record_result(
                    agent,
                    {"execution_path": "error", "error": str(error)},
                )
        return state

    def verifier(state: AgentState) -> AgentState:
        checks = []
        for recorded in state.agent_results:
            outcome = recorded["result"]
            raw_result = outcome.get("result", outcome)
            if isinstance(raw_result, dict) and "success" in raw_result:
                evaluation_input = raw_result
            else:
                evaluation_input = {"success": "error" not in outcome}
            check = result_evaluator.evaluate(evaluation_input)
            checks.append({
                "agent": recorded["agent"],
                "execution_path": outcome.get("execution_path"),
                "check": check,
            })

        passed = all(item["check"].get("success", False) for item in checks)
        status = "verified" if passed and not state.errors else "failed"
        state.verification_results = {
            "status": status,
            "overall": status,
            "checks": checks,
            "errors": list(state.errors),
        }
        return state

    def memory(state: AgentState) -> AgentState:
        conversation_id = state.conversation_id or "default"
        record = {
            "input": state.user_input,
            "results": list(state.agent_results),
            "verification": dict(state.verification_results),
        }
        try:
            memory_adapter.save(conversation_id, record)
            state.memory_context = memory_adapter.load(conversation_id)
            state.memory_saved = True
        except Exception as error:
            state.fail(f"memory: {error}")
            state.memory_context = {"short_term": []}
            state.memory_saved = False
        return state

    def audit(state: AgentState) -> AgentState:
        action = {
            "input": state.user_input,
            "agents": list(state.selected_agents),
            "verification": state.verification_results,
        }
        logger.record(action)
        block = ledger.add_action(action)
        state.audit_metadata["audit_id"] = block["hash"]
        state.audit_metadata["audit_chain_length"] = len(ledger.chain)
        return state

    def synthesizer(state: AgentState) -> AgentState:
        if not state.execution_plan:
            state.final_response = "No execution plan was generated for this request."
            return state
        agents = ", ".join(state.selected_agents) or "no agents"
        status = state.verification_results.get("status", "unknown")
        state.final_response = (
            f"Workflow completed for {agents}. Verification status: {status}."
        )
        return state

    return (
        WorkflowGraph()
        .add_node("planner", planner)
        .add_node("capability", capability)
        .add_node("executor", executor)
        .add_node("verifier", verifier)
        .add_node("memory", memory)
        .add_node("audit", audit)
        .add_node("synthesizer", synthesizer)
        .add_edge("planner", "capability")
        .add_edge("capability", "executor")
        .add_edge("executor", "verifier")
        .add_edge("verifier", "memory")
        .add_edge("memory", "audit")
        .add_edge("audit", "synthesizer")
    )
