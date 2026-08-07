from ANT_X_OS.master_agent.master_runtime import MasterAgentRuntime
from ANT_X_OS.core.planner import Planner
from ANT_X_OS.master_agent import army_bridge
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry


def test_master_skill_flow():
    registry.clear()
    load_builtin_skills()
    planner = Planner()
    # simple fake registry for agents
    class FakeAgent:
        def run(self, task):
            return {"ok": True, "skills": task.get("skills")}

    agent_registry = {"coder": FakeAgent()}
    runtime = MasterAgentRuntime(planner, agent_registry)
    results = runtime.run("implement feature X")
    # result should contain skill annotations
    assert isinstance(results, list)
