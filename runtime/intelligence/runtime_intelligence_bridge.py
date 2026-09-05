"""ANT intelligence bridge.

Connects decision making capabilities with runtime execution.
"""


class RuntimeIntelligenceBridge:
    def __init__(self, decision_engine=None, capability_registry=None,
                 tool_selector=None, model_router=None):
        self.decision_engine = decision_engine
        self.capability_registry = capability_registry
        self.tool_selector = tool_selector
        self.model_router = model_router

    def prepare_execution(self, goal):
        capabilities = None
        if self.capability_registry:
            capabilities = self.capability_registry.list_capabilities()

        decision = None
        if self.decision_engine:
            decision = self.decision_engine.decide(goal, capabilities)

        tool = None
        if self.tool_selector:
            tool = self.tool_selector.select(goal)

        model = None
        if self.model_router:
            model = self.model_router.route(goal)

        return {
            "goal": goal,
            "decision": decision,
            "tool": tool,
            "model": model,
        }
