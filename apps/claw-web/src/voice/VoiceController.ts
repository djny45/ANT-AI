export type VoiceState = 'idle' | 'listening' | 'processing' | 'speaking';

export class VoiceController {
  private state: VoiceState = 'idle';
  private listeners: Array<(state: VoiceState) => void> = [];

  setState(next: VoiceState) {
    this.state = next;
    this.listeners.forEach((listener) => listener(next));
  }

  getState(): VoiceState {
    return this.state;
  }

  subscribe(listener: (state: VoiceState) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((item) => item !== listener);
    };
  }
}
