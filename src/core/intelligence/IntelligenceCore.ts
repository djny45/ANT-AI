import { GoalAnalyzer } from './GoalAnalyzer';
import { TaskDecomposer } from './TaskDecomposer';
import { DecisionEngine } from './DecisionEngine';
import { GoalAnalysis, TaskNode, ExecutionStrategy } from './IntelligenceTypes';

export interface IntelligenceResult {
  analysis: GoalAnalysis;
  tasks: TaskNode[];
  strategy: ExecutionStrategy;
}

/**
 * ANT Intelligence Core
 *
 * Connects the reasoning pipeline:
 * Goal Analysis -> Task Decomposition -> Decision Strategy
 */
export class IntelligenceCore {
  private analyzer: GoalAnalyzer;
  private decomposer: TaskDecomposer;
  private decisionEngine: DecisionEngine;

  constructor() {
    this.analyzer = new GoalAnalyzer();
    this.decomposer = new TaskDecomposer();
    this.decisionEngine = new DecisionEngine();
  }

  async process(goal: string): Promise<IntelligenceResult> {
    const analysis = this.analyzer.analyze(goal);
    const tasks = this.decomposer.decompose(analysis);
    const strategy = this.decisionEngine.decide(analysis, tasks);

    return {
      analysis,
      tasks,
      strategy,
    };
  }
}
