import { ExecutionStrategy, GoalAnalysis, TaskNode } from './IntelligenceTypes';

export class DecisionEngine {
  decide(goal: GoalAnalysis, tasks: TaskNode[]): ExecutionStrategy {
    const complex = goal.complexity > 50;

    return {
      tasks,
      parallel: complex,
      modelStrategy: complex ? 'highest-quality' : 'fallback'
    };
  }
}
