from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry
from ANT_X_OS.skills.selector import SkillSelector
from ant_core.event_bus.events import EventBus
from ant_core.planner.planner import IntelligencePlanner
from ant_langgraph.graph import build_default_graph
from ant_langgraph.state import AgentState


def test_intelligence_planner_returns_stage_contract_fields():
    plan = IntelligencePlanner().plan("implement a secure data API")

    assert plan["strategy"] == "multi-agent"
    assert plan["required_capabilities"] == ["coding", "security", "data"]
    assert plan["confidence"] == 0.90


def test_selector_returns_rich_evidence_for_all_capability_families():
    registry.clear()
    load_builtin_skills()
    selector = SkillSelector(registry)

    requests = {
        "research": "research market information",
        "coding": "implement a Python feature",
        "security": "review a vulnerability",
        "data": "analyze a CSV dataset",
    }
    for family, text in requests.items():
        selections = selector.select_capabilities_for_task({"description": text})
        matching = [selection for selection in selections if selection["execution_target"] == family]
        assert matching
        assert matching[0]["capability"]
        assert matching[0]["reason"]
        assert 0.0 <= matching[0]["confidence"] <= 1.0

    assert selector.select_for_task({"description": requests["data"]}) == ["Data Skill"]


def test_planner_node_records_intent_and_complexity_evidence():
    graph = build_default_graph()
    state = graph.run(AgentState(user_input="implement and integrate a repository workflow"))

    assert state.intent == "complex"
    assert state.complexity == "complex"
    assert state.audit_metadata["intent_analysis"]["route"] == "complex"
    assert state.audit_metadata["complexity_detection"]["complexity"] == "complex"


def test_graph_emits_one_event_for_each_node():
    event_bus = EventBus()
    graph = build_default_graph(event_bus=event_bus)
    state = graph.run(AgentState(user_input="implement a Python API"))

    expected = [
        "planner",
        "capability",
        "executor",
        "verifier",
        "memory",
        "audit",
        "synthesizer",
    ]
    assert [event.name for event in event_bus.events] == expected
    assert [event["name"] for event in state.events] == expected
    assert all(event["payload"]["stage"] in expected for event in state.events)


def test_timeout_failure_records_recovery_and_workflow_continues():
    class TimeoutOrchestrator:
        def prepare(self, user_input, user_context):
            raise TimeoutError("planner timed out")

    event_bus = EventBus()
    graph = build_default_graph(
        orchestrator=TimeoutOrchestrator(),
        event_bus=event_bus,
    )
    state = graph.run(AgentState(user_input="implement a Python API"))

    assert state.recovery_records == [{
        "error": "planner timed out",
        "stage": "planner",
        "recovery_action": "retry_stage",
    }]
    assert state.current_node == "synthesizer"
    assert len(event_bus.events) == 7
    assert state.final_response == "No execution plan was generated for this request."


def test_missing_capability_records_stage_recovery_and_continues():
    class EmptySelector:
        def select_for_task_with_evidence(self, task):
            return []

    graph = build_default_graph(skill_selector=EmptySelector())
    state = graph.run(AgentState(user_input="implement a Python API"))

    assert state.recovery_records[0]["stage"] == "capability"
    assert state.recovery_records[0]["recovery_action"] == "use_fallback_capability"
    assert "no capability selected" in state.recovery_records[0]["error"]
    assert state.current_node == "synthesizer"
