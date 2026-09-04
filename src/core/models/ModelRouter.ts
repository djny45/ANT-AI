export type ModelStrategy = 'fallback' | 'fastest' | 'cheapest' | 'quality';

export interface ModelAdapter {
  name: string;
  model: string;
  available(): boolean;
  execute(input: unknown): Promise<unknown>;
}

export interface RouterConfig {
  models: ModelAdapter[];
  strategy?: ModelStrategy;
}

/**
 * ANT-AI Model Router
 * Central intelligence layer for selecting available models.
 */
export class ModelRouter {
  private models: ModelAdapter[];
  private strategy: ModelStrategy;

  constructor(config: RouterConfig) {
    this.models = config.models;
    this.strategy = config.strategy || 'fallback';
  }

  private selectModel(): ModelAdapter {
    const available = this.models.filter(model => model.available());

    if (!available.length) {
      throw new Error('No AI model providers available');
    }

    // Future adapters can add latency, cost and quality scoring.
    return available[0];
  }

  async run(input: unknown): Promise<unknown> {
    const model = this.selectModel();

    try {
      return await model.execute(input);
    } catch (error) {
      if (this.strategy === 'fallback') {
        const backup = this.models.find(m => m !== model && m.available());
        if (backup) return backup.execute(input);
      }
      throw error;
    }
  }
}
