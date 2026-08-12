export type PerformanceSnapshot = {
  fps: number;
  frameTime: number;
};

export class PerformanceMonitor {
  private frames = 0;
  private last = performance.now();
  private snapshot: PerformanceSnapshot = { fps: 0, frameTime: 0 };

  tick(): PerformanceSnapshot {
    this.frames += 1;
    const now = performance.now();
    const elapsed = now - this.last;

    if (elapsed >= 1000) {
      this.snapshot = {
        fps: Math.round((this.frames * 1000) / elapsed),
        frameTime: elapsed / this.frames,
      };
      this.frames = 0;
      this.last = now;
    }

    return this.snapshot;
  }
}
