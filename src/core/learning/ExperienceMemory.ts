export interface ExperienceRecord {
  task: string;
  strategy: string;
  model?: string;
  success: boolean;
  score?: number;
  timestamp: number;
}

export class ExperienceMemory {
  private experiences: ExperienceRecord[] = [];

  add(record: ExperienceRecord): void {
    this.experiences.push(record);
  }

  getAll(): ExperienceRecord[] {
    return [...this.experiences];
  }

  findSimilar(task: string): ExperienceRecord[] {
    const keyword = task.toLowerCase();
    return this.experiences.filter(e => e.task.toLowerCase().includes(keyword));
  }
}
