export type ModelTaskType =
  | 'reasoning'
  | 'coding'
  | 'research'
  | 'summarization'
  | 'review';

export interface ModelSelectionContext {
  taskType: ModelTaskType;
  complexity: number;
  priority?: 'speed' | 'quality' | 'cost';
}

export interface ModelCandidate {
  name: string;
  provider: string;
  qualityScore: number;
  speedScore: number;
  costScore: number;
}

/**
 * ModelIntelligence selects a model strategy based on task requirements.
 * It is intentionally provider agnostic and connects later to ModelRouter.
 */
export class ModelIntelligence {
  selectStrategy(context: ModelSelectionContext): 'fastest' | 'cheapest' | 'highest-quality' {
    if (context.priority === 'speed') return 'fastest';
    if (context.priority === 'cost') return 'cheapest';

    if (context.complexity >= 70 || context.taskType === 'reasoning') {
      return 'highest-quality';
    }

    return 'fastest';
  }
}
