from ant_langgraph.graph import build_default_graph
from ant_langgraph.state import AgentState


def test_graph_contains_unified_execution_path():
    graph = build_default_graph()
    assert set(graph.nodes) == {"understand", "planner", "execute", "verifier", "synthesizer"}
    assert graph.edges["understand"] == ["planner"]
    assert graph.edges["planner"] == ["execute"]
    assert graph.edges["execute"] == ["verifier"]
    assert graph.edges["verifier"] == ["synthesizer"]


def test_graph_planner_selects_current_capabilities():
    graph = build_default_graph()
    state = AgentState(user_input="build and test a feature")
    planned = graph.nodes["planner"](state)
    assert planned.selected_capabilities == ["coding", "testing"]
    assert len(planned.execution_plan) == 2
