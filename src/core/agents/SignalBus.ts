export type SignalType = 'task' | 'result' | 'status' | 'error' | 'learning';

export interface AgentSignal {
  type: SignalType;
  source: string;
  payload: unknown;
  timestamp: number;
}

export type SignalHandler = (signal: AgentSignal) => void | Promise<void>;

export class SignalBus {
  private listeners = new Map<SignalType, SignalHandler[]>();

  subscribe(type: SignalType, handler: SignalHandler): void {
    const handlers = this.listeners.get(type) || [];
    handlers.push(handler);
    this.listeners.set(type, handlers);
  }

  async publish(signal: Omit<AgentSignal, 'timestamp'>): Promise<void> {
    const event: AgentSignal = { ...signal, timestamp: Date.now() };
    const handlers = this.listeners.get(event.type) || [];

    for (const handler of handlers) {
      await handler(event);
    }
  }
}
