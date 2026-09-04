export interface AgentResult {
  agent: string;
  task: string;
  output: unknown;
  confidence?: number;
}

export class ResultAggregator {
  aggregate(results: AgentResult[]): AgentResult[] {
    return results.sort(
      (a, b) => (b.confidence || 0) - (a.confidence || 0)
    );
  }

  summarize(results: AgentResult[]): string {
    return results
      .map((result) => `${result.agent}: ${String(result.output)}`)
      .join('\n');
  }
}
