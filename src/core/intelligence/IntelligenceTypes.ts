export interface GoalAnalysis {
  goal: string;
  complexity: number;
  domains: string[];
  requiredCapabilities: string[];
}

export interface TaskNode {
  id: string;
  description: string;
  dependencies: string[];
  capability?: string;
}

export interface ExecutionStrategy {
  tasks: TaskNode[];
  parallel: boolean;
  modelStrategy: 'cheapest' | 'fastest' | 'highest-quality' | 'fallback';
}
