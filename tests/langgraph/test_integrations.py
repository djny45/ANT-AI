import asyncio

from ant_langgraph.integrations.agent_manager_bridge import (
    AgentExecutionRequest,
    AgentManagerBridge,
)
from ant_langgraph.integrations.ant_xos_bridge import ANTXOSBridge
from ant_langgraph.integrations.authenticated_graph_chat import (
    AuthenticatedGraphRunner,
    GraphChatRequest,
)
from ant_langgraph.integrations.fastapi_bridge import process_chat_request
from ant_langgraph.integrations.master_planner_bridge import MasterPlannerBridge
from ant_langgraph.integrations.pipeline import ANTAIGraphPipeline


def test_agent_manager_bridge_fallback_and_delegation():
    request = AgentExecutionRequest(
        task="run task",
        context={"trace": True},
        selected_agents=["agent-a"],
    )

    fallback = asyncio.run(AgentManagerBridge().route(request))
    assert fallback == {
        "status": "ready",
        "agents": ["agent-a"],
        "message": "Agent manager bridge initialized",
    }

    class AgentManager:
        def __init__(self):
            self.calls = []

        async def execute(self, **kwargs):
            self.calls.append(kwargs)
            return {"status": "complete"}

    manager = AgentManager()
    result = asyncio.run(AgentManagerBridge(manager).route(request))

    assert result == {"status": "complete"}
    assert manager.calls == [{
        "task": "run task",
        "agents": ["agent-a"],
        "context": {"trace": True},
    }]


def test_ant_xos_bridge_registry_fallback_not_found_success_and_memory():
    task = {"input": "hello"}
    assert ANTXOSBridge().execute_agent("agent-a", task) == {
        "status": "registry_unavailable",
        "agent": "agent-a",
    }

    class Agent:
        def run(self, value):
            return {"answer": value["input"].upper()}

    class Registry:
        def get(self, name):
            return {"agent-a": Agent()}.get(name)

    class Audit:
        def __init__(self):
            self.events = []

        def record(self, event):
            self.events.append(event)

    audit = Audit()
    bridge = ANTXOSBridge(agent_registry=Registry(), audit=audit)

    assert bridge.execute_agent("missing", task) == {
        "status": "agent_not_found",
        "agent": "missing",
    }
    assert bridge.execute_agent("agent-a", task) == {"answer": "HELLO"}
    assert audit.events == [{
        "agent": "agent-a",
        "task": task,
        "result": {"answer": "HELLO"},
    }]

    class Memory:
        def __init__(self):
            self.items = []

        def store(self, item):
            self.items.append(item)
            return "stored"

    memory = Memory()
    assert ANTXOSBridge(memory=memory).remember(task) == "stored"
    assert memory.items == [task]
    assert ANTXOSBridge().remember(task) is None


def test_master_planner_bridge_fallback_and_master_agent():
    state = {"user_input": "build an API"}
    fallback = asyncio.run(MasterPlannerBridge().create_plan(state))

    assert fallback == {
        "execution_plan": {"goal": "build an API", "tasks": [], "agents": []},
        "planner": "fallback",
    }

    class MasterAgent:
        def __init__(self):
            self.requests = []

        async def receive_request(self, user_input):
            self.requests.append(user_input)
            return {"tasks": [{"agent": "agent-a"}]}

    master = MasterAgent()
    result = asyncio.run(MasterPlannerBridge(master).create_plan(state))

    assert result == {
        "execution_plan": {"tasks": [{"agent": "agent-a"}]},
        "planner": "master_agent",
    }
    assert master.requests == ["build an API"]


def test_master_planner_bridge_routes_task_agents():
    plan = {"tasks": [{"agent": "agent-a"}, {"agent": "agent-b"}, {}]}

    assert asyncio.run(MasterPlannerBridge().route_plan(plan)) == {
        "selected_agents": ["agent-a", "agent-b", None]
    }


def test_authenticated_graph_runner_without_optional_collaborators():
    class Graph:
        async def run(self, **kwargs):
            return {"response": kwargs}

    request = GraphChatRequest(user_id="user-1", message="hello")
    result = asyncio.run(AuthenticatedGraphRunner(graph_runtime=Graph()).execute(request))

    assert result == {
        "response": {
            "user_input": "hello",
            "context": {
                "user_id": "user-1",
                "conversation_id": None,
                "permissions": [],
            },
        }
    }


def test_authenticated_graph_runner_audits_and_uses_memory():
    class Graph:
        def __init__(self):
            self.calls = []

        async def run(self, **kwargs):
            self.calls.append(kwargs)
            return {"response": "done"}

    class Memory:
        def __init__(self):
            self.calls = []

        async def retrieve(self, user_id):
            self.calls.append(("retrieve", user_id))
            return [{"content": "prior"}]

        async def save(self, *args):
            self.calls.append(("save", *args))

    class Audit:
        def __init__(self):
            self.events = []

        async def log(self, event):
            self.events.append(event)

    graph = Graph()
    memory = Memory()
    audit = Audit()
    request = GraphChatRequest(
        user_id="user-1",
        message="hello",
        conversation_id="conversation-1",
        metadata={"permissions": ["chat"]},
    )

    result = asyncio.run(
        AuthenticatedGraphRunner(graph, memory, audit).execute(request)
    )

    assert result == {"response": "done"}
    assert graph.calls == [{
        "user_input": "hello",
        "context": {
            "user_id": "user-1",
            "conversation_id": "conversation-1",
            "permissions": ["chat"],
            "memory": [{"content": "prior"}],
        },
    }]
    assert memory.calls == [
        ("retrieve", "user-1"),
        ("save", "user-1", "hello", {"response": "done"}),
    ]
    assert [event["event"] for event in audit.events] == [
        "graph_request_started",
        "graph_request_completed",
    ]


def test_graph_pipeline_uses_async_run_and_saves_truthy_response():
    class Graph:
        async def run(self, state):
            assert state["user_input"] == "hello"
            assert state["context"] == {"trace": True}
            return {"final_response": "done"}

    class Audit:
        def __init__(self):
            self.events = []

        def log(self, event):
            self.events.append(event)

    class Memory:
        def __init__(self):
            self.saved = []

        def save(self, response):
            self.saved.append(response)

    audit = Audit()
    memory = Memory()
    result = asyncio.run(
        ANTAIGraphPipeline(Graph(), object(), audit, memory).execute(
            "hello", {"trace": True}
        )
    )

    assert result == {"final_response": "done"}
    assert memory.saved == ["done"]
    assert [event["event"] for event in audit.events] == [
        "graph_execution_started",
        "graph_execution_completed",
    ]


def test_graph_pipeline_uses_execute_and_skips_empty_response_memory_save():
    class Graph:
        def execute(self, state):
            assert state["user_input"] == "hello"
            return {"final_response": ""}

    class Memory:
        def save(self, response):
            raise AssertionError("empty responses must not be saved")

    result = asyncio.run(
        ANTAIGraphPipeline(Graph(), object(), memory=Memory()).execute("hello")
    )

    assert result == {"final_response": ""}


def test_fastapi_bridge_returns_normalized_pipeline_output():
    result = asyncio.run(
        process_chat_request(
            "hello",
            user_id="user-1",
            conversation_id="conversation-1",
            context={"trace": True},
        )
    )

    assert set(result) == {
        "response",
        "agents_used",
        "risk_score",
        "memory_saved",
        "audit_id",
    }
    assert result["response"]
    assert isinstance(result["agents_used"], list)
