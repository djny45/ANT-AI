from ANT_X_OS.graph.engine import GraphEngine, GraphNode
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry


def test_graph_node_receives_skills():
    registry.clear()
    load_builtin_skills()
    ge = GraphEngine()
    n = GraphNode("dev", "developer")
    ge.add_node(n)
    task = {"task": "implement feature", "description": "add X"}
    skills = ["Coding Skill", "Review Skill"]
    res = ge.run(task, {}, skills)
    assert res and isinstance(res[0].get("skills"), list)
