import asyncio

import pytest

from ANT_X_OS.core.memory import Memory
from ANT_X_OS.skills.orchestrator import SkillOrchestrator
from ANT_X_OS.skills.registry import SkillRegistry
from ANT_X_OS.tools.mcp_executor import MCPExecutor
from agents.workflow_runtime import WorkflowRuntime
from ant_langgraph.errors import NodeExecutionError, UnknownNodeError
from ant_langgraph.graph import WorkflowGraph, build_default_graph
from ant_langgraph.state import AgentState


class ExplodingSkill:
    name = "Exploding Skill"

    def validate(self, context):
        return True

    def execute(self, task, memory=None):
        raise RuntimeError("skill blew up")


class FailingMemory(Memory):
    def store_workflow(self, workflow, permanent=False):
        raise IOError("memory backend offline")


class FailingAgent:
    async def execute(self, step):
        raise ValueError("agent failure")


def test_orchestrator_uses_injected_registry():
    registry = SkillRegistry()
    registry.register(ExplodingSkill())
    orchestrator = SkillOrchestrator(registry=registry)

    workflow = orchestrator.run({"skills": ["Exploding Skill"]})["workflow"]

    assert workflow["success"] is False
    assert workflow["validation"]["Exploding Skill"]["error_type"] == "RuntimeError"


def test_orchestrator_reports_memory_failure():
    registry = SkillRegistry()
    orchestrator = SkillOrchestrator(registry=registry, memory=FailingMemory())

    workflow = orchestrator.run({"skills": []})["workflow"]

    assert workflow["memory_error"]["error_type"] == "OSError"


def test_mcp_executor_reports_error_type():
    executor = MCPExecutor()
    executor.register("boom", lambda payload: (_ for _ in ()).throw(KeyError("missing")))

    result = executor.execute("boom", {})

    assert result["success"] is False
    assert result["error_type"] == "KeyError"
    assert result["tool"] == "boom"


def test_workflow_runtime_marks_failure():
    runtime = WorkflowRuntime(agents={"a": FailingAgent()})

    result = asyncio.run(runtime.execute({"goal": "g", "steps": [{"agent": "a"}]}))

    assert result["status"] == "failed"
    assert result["errors"][0]["error_type"] == "ValueError"


def test_workflow_runtime_reports_unavailable_agent():
    runtime = WorkflowRuntime()

    result = asyncio.run(runtime.execute({"goal": "g", "steps": [{"agent": "missing"}]}))

    assert result["status"] == "failed"
    assert result["errors"][0]["error_type"] == "AgentUnavailable"


def test_graph_wraps_node_exception():
    def boom(state):
        raise RuntimeError("node down")

    graph = WorkflowGraph().add_node("planner", boom)
    state = AgentState(user_input="x")

    with pytest.raises(NodeExecutionError) as excinfo:
        graph.run(state)

    assert excinfo.value.node == "planner"
    assert isinstance(excinfo.value.cause, RuntimeError)
    assert state.errors


def test_graph_rejects_unknown_start_node():
    with pytest.raises(UnknownNodeError):
        build_default_graph().run(AgentState(user_input="x"), start="nope")
