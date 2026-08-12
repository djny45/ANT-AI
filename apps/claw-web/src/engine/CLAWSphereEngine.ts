export type ClawState = 'IDLE' | 'LISTENING' | 'THINKING' | 'RESPONDING';

export interface ClawEngineConfig {
  glowIntensity: number;
  particleCount: number;
}

export class CLAWSphereEngine {
  private state: ClawState = 'IDLE';
  private config: ClawEngineConfig;

  constructor(config: ClawEngineConfig) {
    this.config = config;
  }

  setState(state: ClawState) {
    this.state = state;
  }

  getGlowMultiplier(): number {
    switch (this.state) {
      case 'LISTENING': return 1.5;
      case 'THINKING': return 2.2;
      case 'RESPONDING': return 1.8;
      default: return 1;
    }
  }
}
