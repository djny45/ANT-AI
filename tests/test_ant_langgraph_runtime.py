import os
import unittest
from unittest.mock import patch

from ant_langgraph.router import route_request
from ant_langgraph.state import AgentState
from ant_langgraph.graph import build_default_graph


class GraphRuntimeTests(unittest.TestCase):
    def test_router_categories(self):
        self.assertEqual(route_request("hello, how are you?"), "direct")
        self.assertEqual(route_request("debug this Python code"), "coding")
        self.assertEqual(route_request("research this market"), "research")
        self.assertEqual(route_request("build and integrate a secure API"), "complex")

    def test_graph_state_flow(self):
        state = AgentState(user_input="test")
        result = build_default_graph().run(state)
        self.assertEqual(result.current_node, "synthesizer")
        self.assertIsNotNone(result.final_response)

    def test_request_openrouter_key_selects_hosted_runtime(self):
        class FakeRuntime:
            default_model = "test-model"

            def __init__(self, api_key=None):
                self.api_key = api_key

            def generate(self, prompt):
                return {"response": "ok", "latency_ms": 1}

        state = AgentState(
            user_input="test",
            user_context={"openrouter_api_key": "sk-or-test"},
        )
        with patch.dict(os.environ, {"ANT_MODEL_PROVIDER": "ollama"}, clear=False), \
             patch("intelligence.openrouter_connector.OpenRouterConnector", FakeRuntime):
            result = build_default_graph().run(state)

        self.assertEqual(result.audit_metadata["model_provider"], "openrouter")
        self.assertEqual(result.audit_metadata["model"], "test-model")


if __name__ == "__main__":
    unittest.main()
