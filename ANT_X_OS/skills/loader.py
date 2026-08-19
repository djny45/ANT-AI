"""Loader for built-in skills. Keeps discovery simple and deterministic."""
from .coding_skill import CodingSkill
from .data_skill import DataSkill
from .debugging_skill import DebuggingSkill
from .deployment_skill import DeploymentSkill
from .engineering.goal_driven_execution import GoalDrivenExecution
from .engineering.simplicity_first import SimplicityFirst
from .engineering.surgical_changes import SurgicalChanges
from .engineering.think_before_coding import ThinkBeforeCoding
from .registry import registry
from .research_skill import ResearchSkill
from .review_skill import ReviewSkill
from .security_skill import SecuritySkill


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
    registry.register(ResearchSkill())
    registry.register(DataSkill())

    return registry
