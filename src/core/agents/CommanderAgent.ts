export interface AgentTask {
  id: string;
  goal: string;
  type?: string;
}

export class CommanderAgent {
  private specialists: Map<string, any> = new Map();

  registerSpecialist(name: string, agent: any) {
    this.specialists.set(name, agent);
  }

  async execute(goal: string) {
    const plan: AgentTask[] = [{ id: 'task-1', goal }];
    const results = [];

    for (const task of plan) {
      const specialist = this.specialists.values().next().value;
      if (specialist) {
        results.push(await specialist.execute(task));
      }
    }

    return {
      goal,
      plan,
      results
    };
  }
}
