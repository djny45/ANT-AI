import pytest

from ant_langgraph.executor import WorkflowExecutor
from ant_langgraph.memory import MemoryAdapter
from ant_langgraph.state import AgentState


def test_memory_adapter_empty_load_and_in_memory_round_trip():
    memory = MemoryAdapter()

    assert memory.load(None) == {"short_term": []}
    assert memory.load("conversation") == {"short_term": []}

    memory.save("conversation", {"role": "user", "content": "hello"})
    memory.save("conversation", {"role": "assistant", "content": "hi"})

    assert memory.load("conversation") == {
        "short_term": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ]
    }


def test_memory_adapter_delegates_to_backend():
    class Backend:
        def __init__(self):
            self.items = {}
            self.saved = []

        def load(self, conversation_id):
            return {"backend": self.items.get(conversation_id, [])}

        def save(self, conversation_id, item):
            self.saved.append((conversation_id, item))
            self.items.setdefault(conversation_id, []).append(item)

    backend = Backend()
    memory = MemoryAdapter(backend)
    item = {"content": "hello"}

    memory.save("conversation", item)

    assert backend.saved == [("conversation", item)]
    assert memory.load("conversation") == {"backend": [item]}


def test_memory_adapter_falls_back_when_backend_has_no_methods():
    memory = MemoryAdapter(object())

    memory.save("conversation", {"content": "hello"})

    assert memory.load("conversation") == {"short_term": [{"content": "hello"}]}


def test_workflow_executor_registers_and_executes_keyword_arguments():
    calls = []

    def handler(**kwargs):
        calls.append(kwargs)
        return "done"

    executor = WorkflowExecutor()
    executor.register("agent-a", handler)
    task = {"name": "task"}
    context = {"trace": True}

    assert executor.execute("agent-a", task, context) == "done"
    assert calls == [{"task": task, "context": context}]


def test_workflow_executor_uses_constructor_handlers_and_rejects_unknown_agent():
    def handler(**kwargs):
        return kwargs["task"]["id"]

    executor = WorkflowExecutor({"agent-a": handler})

    assert executor.execute("agent-a", {"id": 7}, {}) == 7
    with pytest.raises(KeyError, match="missing"):
        executor.execute("missing", {}, {})


def test_agent_state_records_clamped_results_and_accumulates_failures():
    state = AgentState(user_input="hello")

    state.record_result("agent-a", {"ok": True}, confidence=2)
    state.record_result("agent-b", {"ok": False}, confidence=-1)
    state.fail("first")
    state.fail("second")

    assert state.agent_results == [
        {"agent": "agent-a", "result": {"ok": True}, "confidence": 1.0},
        {"agent": "agent-b", "result": {"ok": False}, "confidence": 0.0},
    ]
    assert state.errors == ["first", "second"]
