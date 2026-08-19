from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ant_core import IntelligenceOrchestrator
from ant_core.event_bus.events import EventBus
from ant_langgraph.router import route_request
from ANT_X_OS.core.evaluator import Evaluator
from ANT_X_OS.core.executor import Executor as CoreExecutor
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.selector import SkillSelector
from capabilities import register_capability_handlers
from reliability.error_recovery import ErrorRecovery
from security.audit_logger import AuditLogger
from security.hash_ledger import HashLedger

from .executor import WorkflowExecutor
from .memory import MemoryAdapter
from .state import AgentState

NodeFn = Callable[[AgentState], AgentState]


@dataclass
class WorkflowGraph:
    nodes: dict[str, NodeFn] = field(default_factory=dict)
    edges: dict[str, list[str]] = field(default_factory=dict)

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
    event_bus=None,
    error_recovery=None,
) -> WorkflowGraph:
    planner_service = orchestrator or IntelligenceOrchestrator()
    load_builtin_skills()
    selector = skill_selector or SkillSelector()
    graph_executor = workflow_executor or WorkflowExecutor()
    register_capability_handlers(graph_executor)
    fallback_executor = core_executor or CoreExecutor()
    result_evaluator = evaluator or Evaluator()
    memory_adapter = memory or MemoryAdapter()
    logger = audit_logger or AuditLogger()
    ledger = hash_ledger or HashLedger()
    bus = event_bus or EventBus()
    recovery = error_recovery or ErrorRecovery()

    def record_failure(state: AgentState, stage: str, error: Exception) -> None:
        record = recovery.recover(error, stage)
        state.recovery_records.append(record)
        state.stage_status[stage] = "failed"
        state.fail(f"{stage}: {record['error']}")

    def emit(state: AgentState, stage: str, payload: dict[str, Any]) -> None:
        event = bus.publish(stage, payload)
        state.events.append(asdict(event))

    def stage_payload(state: AgentState, stage: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "stage": stage,
            "status": state.stage_status.get(stage, "completed"),
        }
        if stage == "planner":
            payload.update({
                "intent": state.intent,
                "complexity": state.complexity,
                "memory_context": dict(state.memory_context),
                "strategy": state.strategy,
                "required_capabilities": list(state.required_capabilities),
                "confidence": state.confidence,
                "task_count": len(state.execution_plan),
            })
        elif stage == "capability":
            payload["selections"] = list(state.capability_selections)
        elif stage == "executor":
            payload["result_count"] = len(state.agent_results)
        elif stage == "verifier":
            payload["verification"] = dict(state.verification_results)
        elif stage == "memory":
            payload["memory_saved"] = state.memory_saved
        elif stage == "audit":
            payload.update(state.audit_metadata)
        elif stage == "synthesizer":
            payload["final_response"] = state.final_response or ""
        if state.recovery_records:
            payload["recovery_records"] = list(state.recovery_records)
        return payload

    def planner(state: AgentState) -> AgentState:
        if not state.request_id:
            state.request_id = str(uuid4())
        if not state.request_timestamp:
            state.request_timestamp = datetime.now(timezone.utc).isoformat()
        conversation_id = state.conversation_id or "default"
        state.memory_context = memory_adapter.load(conversation_id)
        state.user_context = dict(state.user_context)
        state.user_context["memory_context"] = state.memory_context
        planned = planner_service.prepare(state.user_input, state.user_context)
        state.execution_plan = [dict(task) for task in planned.plan]
        state.selected_agents = list(planned.selected_agents)
        state.strategy = planned.strategy
        state.required_capabilities = list(planned.required_capabilities)
        state.confidence = planned.confidence
        state.intent = route_request(state.user_input)
        state.complexity = planned.complexity
        state.audit_metadata["decision"] = planned.context.get("decision", {})
        state.audit_metadata["intent_analysis"] = {
            "route": state.intent,
            "source": "ant_langgraph.router.route_request",
        }
        state.audit_metadata["complexity_detection"] = {
            "complexity": state.complexity,
            "source": "ant_core.DecisionEngine",
        }
        state.audit_metadata["planner_status"] = planned.status
        return state

    def capability(state: AgentState) -> AgentState:
        selections: list[dict[str, Any]] = []
        for task in state.execution_plan:
            selection_task = {
                "type": task.get("agent", ""),
                "description": f"{task.get('objective', '')} {state.user_input}",
            }
            rich_selections = selector.select_capabilities_for_task(selection_task)
            if not rich_selections:
                raise LookupError(
                    f"no capability selected for task: {task.get('objective', '')}"
                )
            task["skills"] = [
                selection["capability"] for selection in rich_selections
            ]
            selections.extend(rich_selections)
        state.capability_selections = selections
        return state

    def record_outcome(
        state: AgentState,
        agent: str,
        result: Any,
        metadata: dict[str, Any],
    ) -> None:
        state.record_result(
            agent,
            result,
            confidence=metadata.get("confidence", 0.0),
        )
        recorded = state.agent_results[-1]
        recorded.update(metadata)

    def executor(state: AgentState) -> AgentState:
        handlers = graph_executor.handlers
        for task in state.execution_plan:
            agent = task.get("agent", "unknown")
            context = dict(state.user_context)
            context["request"] = state.user_input
            context["skills"] = task.get("skills", [])
            try:
                if handlers.get(agent) is not None:
                    envelope = graph_executor.execute(agent, task, context)
                    metadata = {
                        "execution_path": "capability_handler",
                        "success": envelope.get("success", False),
                        "capability": envelope.get("capability"),
                        "handler": envelope.get("handler"),
                        "execution_target": envelope.get("execution_target"),
                        "confidence": envelope.get("confidence", 0.0),
                        "verification": envelope.get("verification", {}),
                    }
                    record_outcome(
                        state,
                        agent,
                        envelope.get("result"),
                        metadata,
                    )
                else:
                    result = fallback_executor.execute(task)
                    metadata = {"execution_path": "core_executor"}
                    if isinstance(result, dict) and "success" in result:
                        metadata["success"] = result["success"]
                    record_outcome(state, agent, result, metadata)
            except Exception as error:  # noqa: BLE001
                record_failure(state, "executor", error)
                record_outcome(
                    state,
                    agent,
                    None,
                    {
                        "execution_path": "error",
                        "success": False,
                        "error": str(error),
                    },
                )
        return state

    def verifier(state: AgentState) -> AgentState:
        checks = []
        for recorded in state.agent_results:
            evaluation_input = {
                "success": recorded.get(
                    "success",
                    "error" not in recorded,
                ),
                "result": recorded["result"],
            }
            check = result_evaluator.evaluate(evaluation_input)
            check_entry = {
                "agent": recorded["agent"],
                "execution_path": recorded.get("execution_path"),
                "check": check,
            }
            if "verification" in recorded:
                check_entry["handler_verification"] = recorded["verification"]
            checks.append(check_entry)

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
            "knowledge": {
                "capabilities_used": list(state.capability_selections),
                "verification_status": state.verification_results.get("status"),
            },
        }
        memory_adapter.save(conversation_id, record)
        state.memory_context = memory_adapter.load(conversation_id)
        state.memory_saved = True
        return state

    def audit(state: AgentState) -> AgentState:
        tools_used = [
            {
                "agent": recorded["agent"],
                "execution_path": recorded.get("execution_path"),
                "capabilities": next(
                    (
                        task.get("skills", [])
                        for task in state.execution_plan
                        if task.get("agent") == recorded["agent"]
                    ),
                    [],
                ),
            }
            for recorded in state.agent_results
        ]
        action = {
            "request_id": state.request_id,
            "timestamp": state.request_timestamp,
            "request": state.user_input,
            "selected_capabilities": list(state.capability_selections),
            "tools_used": tools_used,
            "result": list(state.agent_results),
            "verification": dict(state.verification_results),
            "verification_status": state.verification_results.get("status"),
            "errors": list(state.errors),
        }
        logger.record(action)
        block = ledger.add_action(action)
        state.audit_metadata["request_id"] = state.request_id
        state.audit_metadata["timestamp"] = state.request_timestamp
        state.audit_metadata["audit_record"] = action
        state.audit_metadata["audit_id"] = block["hash"]
        state.audit_metadata["audit_chain_length"] = len(ledger.chain)
        return state

    def synthesizer(state: AgentState) -> AgentState:
        if not state.execution_plan:
            state.final_response = "No execution plan was generated for this request."
            return state
        summaries = []
        for recorded in state.agent_results:
            capability = recorded.get("capability", recorded["agent"])
            result = recorded.get("result", {})
            headline = (
                result.get("headline")
                if isinstance(result, dict)
                else None
            )
            summaries.append(f"{capability}: {headline or 'execution result available'}")
        summary = " ".join(summaries)
        status = state.verification_results.get("status", "unknown")
        state.final_response = (
            f"{summary} Verification status: {status}."
        )
        return state

    def guarded(stage: str, fn: NodeFn) -> NodeFn:
        def run_stage(state: AgentState) -> AgentState:
            state.current_node = stage
            try:
                state = fn(state)
                if stage not in state.stage_status:
                    state.stage_status[stage] = "completed"
            except Exception as error:  # noqa: BLE001
                record_failure(state, stage, error)
            emit(state, stage, stage_payload(state, stage))
            return state

        return run_stage

    return (
        WorkflowGraph()
        .add_node("planner", guarded("planner", planner))
        .add_node("capability", guarded("capability", capability))
        .add_node("executor", guarded("executor", executor))
        .add_node("verifier", guarded("verifier", verifier))
        .add_node("memory", guarded("memory", memory))
        .add_node("audit", guarded("audit", audit))
        .add_node("synthesizer", guarded("synthesizer", synthesizer))
        .add_edge("planner", "capability")
        .add_edge("capability", "executor")
        .add_edge("executor", "verifier")
        .add_edge("verifier", "memory")
        .add_edge("memory", "audit")
        .add_edge("audit", "synthesizer")
    )
