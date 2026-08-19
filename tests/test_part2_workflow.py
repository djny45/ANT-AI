import asyncio
import re

from fastapi.testclient import TestClient

from ant_core.orchestrator.orchestrator import IntelligenceOrchestrator
from ant_langgraph.graph import build_default_graph
from ant_langgraph.integration_pipeline import run_pipeline
from ant_langgraph.memory import MemoryAdapter, SQLAlchemyMemoryBackend
from ant_langgraph.state import AgentState
from ANT_X_OS.api.server import app


def test_sqlalchemy_memory_persists_between_adapter_instances(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'memory.db'}"
    first = MemoryAdapter(SQLAlchemyMemoryBackend(database_url))
    first.save("conversation-1", {"input": "first"})

    second = MemoryAdapter(SQLAlchemyMemoryBackend(database_url))

    assert second.load("conversation-1") == {
        "short_term": [{"input": "first"}],
    }


def test_memory_is_loaded_before_planning_and_saved_after_execution():
    database_url = "sqlite://"
    memory = MemoryAdapter(SQLAlchemyMemoryBackend(database_url))
    memory.save("conversation-1", {"input": "previous"})

    class ContextProbe:
        def prepare(self, request, context):
            assert context["memory_context"]["short_term"] == [{"input": "previous"}]
            return IntelligenceOrchestrator().prepare(request, context)

    state = AgentState(
        user_input="implement a Python API",
        conversation_id="conversation-1",
    )
    result = build_default_graph(
        orchestrator=ContextProbe(),
        memory=memory,
    ).run(state)

    assert result.memory_context["short_term"][0] == {"input": "previous"}
    assert result.memory_context["short_term"][-1]["input"] == "implement a Python API"
    assert result.memory_saved is True


def test_audit_record_contains_required_execution_fields():
    class CapturingLogger:
        def __init__(self):
            self.records = []

        def record(self, event):
            self.records.append(event)

    logger = CapturingLogger()
    state = AgentState(
        user_input="implement a Python API",
        request_id="request-123",
    )
    result = build_default_graph(audit_logger=logger).run(state)
    record = logger.records[0]

    assert result.audit_metadata["request_id"] == "request-123"
    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T.*",
        record["timestamp"],
    )
    assert record["request"] == "implement a Python API"
    assert record["selected_capabilities"]
    assert record["tools_used"]
    assert record["tools_used"][0]["capabilities"]
    assert record["result"]
    assert record["verification"]["status"] in {"verified", "failed"}
    assert record["verification_status"] in {"verified", "failed"}
    assert record["errors"] == result.errors


def test_pipeline_trace_contains_all_sections_and_preserves_existing_keys():
    result = asyncio.run(
        run_pipeline({
            "user_input": "Analyze this Python project and suggest improvements",
            "conversation_id": "trace-test",
            "request_id": "trace-request",
        })
    )

    sections = {
        "request",
        "plan",
        "capability",
        "execution",
        "verification",
        "memory",
        "audit",
        "response",
    }
    assert sections.issubset(result)
    assert result["request"]["request_id"] == "trace-request"
    assert result["plan"]["plan"]
    assert result["capability"]["selections"]
    assert result["execution"]["results"]
    assert result["verification"]["result"]["status"] in {"verified", "failed"}
    assert result["memory"]["saved"] is True
    assert re.fullmatch(r"[0-9a-f]{64}", result["audit_id"])
    assert result["response"]["final_response"]
    for key in (
        "final_response",
        "selected_agents",
        "agent_results",
        "verification_results",
        "execution_plan",
        "memory_context",
        "memory_saved",
        "audit_id",
        "errors",
        "risk_score",
    ):
        assert key in result


def test_execute_rejects_invalid_input_before_pipeline():
    client = TestClient(app)

    response = client.post(
        "/execute",
        json={"message": "' OR 1=1 --"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "error": "Input validation failed",
        "stage": "validation",
        "recovery_action": "reject_invalid_input",
    }


def test_execute_returns_full_trace_for_required_request():
    client = TestClient(app)

    response = client.post(
        "/execute",
        json={
            "message": "Analyze this Python project and suggest improvements",
            "conversation_id": "api-trace-test",
            "request_id": "api-request",
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert {
        "request",
        "plan",
        "capability",
        "execution",
        "verification",
        "memory",
        "audit",
        "response",
    }.issubset(result)
    assert result["response"]["final_response"]
    assert result["request"]["request_id"] == "api-request"
    assert result["plan"]["plan"]
    assert result["capability"]["selections"]
    assert result["execution"]["results"]
    assert result["memory"]["saved"] is True
    assert re.fullmatch(r"[0-9a-f]{64}", result["audit_id"])
