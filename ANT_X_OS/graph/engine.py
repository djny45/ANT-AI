"""Graph engine integration: nodes receive task, state, and selected skills."""
from typing import Dict, Any, List


class GraphNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type

    def execute(self, task: Dict[str, Any], state: Dict[str, Any], skills: List[str]):
        # Node logic should use skills to influence execution. Keep light-weight here.
        return {"node": self.name, "task": task.get("task") if isinstance(task, dict) else task, "skills": skills}


class GraphEngine:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: GraphNode):
        self.nodes.append(node)

    def run(self, task: Dict[str, Any], state: Dict[str, Any], skills: List[str]):
        results = []
        for n in self.nodes:
            results.append(n.execute(task, state, skills))
        return results
