from ant_core.decision_engine.decision import DecisionEngine
from ant_core.planner.planner import IntelligencePlanner
from ant_core.state_manager.state import IntelligenceState


class IntelligenceOrchestrator:
    """Coordinates planning and routing while preserving existing runtimes."""
    def __init__(self, planner=None, decision_engine=None):
        self.planner = planner or IntelligencePlanner()
        self.decision_engine = decision_engine or DecisionEngine()

    def prepare(self, request: str, context=None) -> IntelligenceState:
        state = IntelligenceState(request=request, context=context or {})
        plan = self.planner.plan(request, state.context)
        state.plan = plan["tasks"]
        state.selected_agents = [task["agent"] for task in state.plan]
        decision = self.decision_engine.decide(request, len(state.plan))
        state.context["decision"] = decision.__dict__
        state.status = "planned"
        return state
