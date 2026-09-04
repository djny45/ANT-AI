export interface PerformanceMetric {
  component: string;
  successes: number;
  failures: number;
  averageScore: number;
}

export class PerformanceTracker {
  private metrics = new Map<string, PerformanceMetric>();

  record(component: string, success: boolean, score = 0): void {
    const current = this.metrics.get(component) || {
      component,
      successes: 0,
      failures: 0,
      averageScore: 0,
    };

    if (success) current.successes++;
    else current.failures++;

    const total = current.successes + current.failures;
    current.averageScore = ((current.averageScore * (total - 1)) + score) / total;
    this.metrics.set(component, current);
  }

  get(component: string): PerformanceMetric | undefined {
    return this.metrics.get(component);
  }

  getAll(): PerformanceMetric[] {
    return Array.from(this.metrics.values());
  }
}
