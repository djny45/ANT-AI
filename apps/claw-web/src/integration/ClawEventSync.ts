export type ClawState = 'IDLE' | 'LISTENING' | 'THINKING' | 'RESPONDING';

export interface ClawEvent {
  state: ClawState;
  message?: string;
  timestamp: number;
}

export class ClawEventSync {
  private socket: WebSocket | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  connect(url: string, onEvent: (event: ClawEvent) => void): void {
    this.socket = new WebSocket(url);

    this.socket.onmessage = (message: MessageEvent<string>) => {
      const event = JSON.parse(message.data) as ClawEvent;
      onEvent(event);
    };

    this.socket.onclose = () => {
      this.reconnectTimer = setTimeout(() => this.connect(url, onEvent), 3000);
    };
  }

  disconnect(): void {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.socket?.close();
  }
}
