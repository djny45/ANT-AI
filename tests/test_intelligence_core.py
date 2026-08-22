from ant_core.decision_engine.decision import DecisionEngine
from ant_core.orchestrator.orchestrator import IntelligenceOrchestrator
from ant_langgraph.router import route_request


def test_route_simple_request():
    assert route_request("what is Python?") == "direct"


def test_route_coding_request():
    assert route_request("debug my Python API") == "coding"


def test_route_complex_request():
    assert route_request("implement and integrate a repository workflow") == "complex"


def test_decision_engine():
    decision = DecisionEngine().decide("build an API", 1)
    assert decision.route == "unified_focused"


def test_orchestrator_prepares_unified_state():
    state = IntelligenceOrchestrator().prepare("analyze my repository and suggest improvements")
    assert state.status == "planned"
    assert state.selected_capabilities
    assert "decision" in state.context
    assert state.context["decision"]["route"] == "unified_focused"
