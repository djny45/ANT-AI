export type ClawMode = 'idle' | 'listening' | 'thinking' | 'responding';

export interface ClawState {
  mode: ClawMode;
  connected: boolean;
  intensity: number;
}

export const defaultClawState: ClawState = {
  mode: 'idle',
  connected: false,
  intensity: 0.4,
};
