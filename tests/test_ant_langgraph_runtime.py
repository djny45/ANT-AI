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

    def test_request_model_api_profile_selects_runtime(self):
        class FakeRuntime:
            def __init__(self, api_key=None, provider="custom", model="", base_url=None):
                self.api_key = api_key
                self.provider = provider
                self.default_model = model

            def generate(self, prompt, model=None):
                return {"response": "ok", "latency_ms": 1}

        state = AgentState(
            user_input="test",
            user_context={
                "model_api_key": "test-key",
                "model_provider": "custom",
                "model": "test-model",
                "model_base_url": "https://example.test/v1",
            },
        )
        with patch("intelligence.model_api_connector.ModelApiConnector", FakeRuntime):
            result = build_default_graph().run(state)

        self.assertEqual(result.audit_metadata["model_provider"], "custom")
        self.assertEqual(result.audit_metadata["model"], "test-model")


if __name__ == "__main__":
    unittest.main()
