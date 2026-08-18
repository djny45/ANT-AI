import unittest

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


if __name__ == "__main__":
    unittest.main()
