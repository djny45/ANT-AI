import asyncio
import re

from fastapi.testclient import TestClient

from ANT_X_OS.api.server import app
from ANT_X_OS.core.planner import Planner
from ANT_X_OS.master_agent.master_runtime import MasterAgentRuntime
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry
from ant_langgraph.graph import build_default_graph
from ant_langgraph.integration_pipeline import run_pipeline
from ant_langgraph.state import AgentState


def test_run_pipeline_exposes_evidence_for_each_stage():
    result = asyncio.run(
        run_pipeline({
            "user_input": "implement a Python API",
            "conversation_id": "e2e-test",
        })
    )

    assert result["execution_plan"]
    assert any(
        "Coding Skill" in task.get("skills", []) for task in result["execution_plan"]
    )
    assert result["agent_results"]
    assert result["verification_results"]["status"] in {"verified", "failed"}
    assert result["memory_context"]["short_term"]
    assert result["memory_context"]["short_term"][0]["input"] == "implement a Python API"
    assert result["memory_saved"] is True
    assert re.fullmatch(r"[0-9a-f]{64}", result["audit_id"])
    assert result["final_response"]


def test_default_graph_runs_all_nodes_in_order():
    graph = build_default_graph()
    state = graph.run(AgentState(user_input="test"))

    assert list(graph.nodes) == [
        "planner",
        "capability",
        "executor",
        "verifier",
        "memory",
        "audit",
        "synthesizer",
    ]
    assert state.current_node == "synthesizer"
    assert state.verification_results["status"] in {"verified", "failed"}
    assert state.memory_context["short_term"]
    assert state.audit_metadata["audit_chain_length"] == 1


def test_master_runtime_selects_skills_with_real_planner_and_agent_dict():
    registry.clear()
    load_builtin_skills()

    class FakeAgent:
        def run(self, task):
            return {"skills": task["skills"]}

    runtime = MasterAgentRuntime(Planner(), {"coder": FakeAgent()})
    results = runtime.run("implement feature X")

    assert results
    assert results[0]["skills"]


def test_execute_endpoint_runs_normalized_pipeline():
    client = TestClient(app)

    response = client.post(
        "/execute",
        json={
            "message": "implement a Python API",
            "conversation_id": "api-test",
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["final_response"]
    assert result["execution_plan"]
    assert result["verification_results"]["status"] in {"verified", "failed"}
    assert re.fullmatch(r"[0-9a-f]{64}", result["audit_id"])
