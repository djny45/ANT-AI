import { TaskNode, GoalAnalysis } from './IntelligenceTypes';

export class TaskDecomposer {
  decompose(goal: GoalAnalysis): TaskNode[] {
    const tasks: TaskNode[] = [
      {
        id: 'understand',
        description: `Analyze objective: ${goal.goal}`,
        dependencies: [],
        capability: 'reasoning'
      },
      {
        id: 'execute',
        description: 'Execute the required specialist work',
        dependencies: ['understand'],
        capability: goal.requiredCapabilities[0] || 'general'
      },
      {
        id: 'verify',
        description: 'Validate execution result',
        dependencies: ['execute'],
        capability: 'verification'
      }
    ];

    return tasks;
  }
}
