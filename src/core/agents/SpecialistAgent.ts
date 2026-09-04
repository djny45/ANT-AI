export interface SpecialistResult {
  task: string;
  output: unknown;
}

export class SpecialistAgent {
  constructor(
    public name: string,
    private handler?: (task: string) => Promise<unknown>
  ) {}

  async execute(task: { goal: string }): Promise<SpecialistResult> {
    const output = this.handler
      ? await this.handler(task.goal)
      : `Completed by ${this.name}: ${task.goal}`;

    return {
      task: task.goal,
      output
    };
  }
}
