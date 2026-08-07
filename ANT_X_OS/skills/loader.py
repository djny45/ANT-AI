"""Loader for built-in skills. Keeps discovery simple and deterministic."""
from .registry import registry
from .engineering.think_before_coding import ThinkBeforeCoding
from .engineering.simplicity_first import SimplicityFirst
from .engineering.surgical_changes import SurgicalChanges
from .engineering.goal_driven_execution import GoalDrivenExecution
from .coding_skill import CodingSkill
from .review_skill import ReviewSkill
from .debugging_skill import DebuggingSkill
from .security_skill import SecuritySkill
from .deployment_skill import DeploymentSkill


def load_builtin_skills():
    # engineering heuristics
    registry.register(ThinkBeforeCoding())
    registry.register(SimplicityFirst())
    registry.register(SurgicalChanges())
    registry.register(GoalDrivenExecution())

    # core skills
    registry.register(CodingSkill())
    registry.register(ReviewSkill())
    registry.register(DebuggingSkill())
    registry.register(SecuritySkill())
    registry.register(DeploymentSkill())

    return registry
