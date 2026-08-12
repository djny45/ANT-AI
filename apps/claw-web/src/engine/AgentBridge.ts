export type AgentEvent = {
  type: 'STATE_CHANGE' | 'MESSAGE';
  state?: 'IDLE' | 'LISTENING' | 'THINKING' | 'RESPONDING';
  message?: string;
};

export class AgentBridge {
  private socket?: WebSocket;

  connect(url: string, onEvent: (event: AgentEvent) => void) {
    this.socket = new WebSocket(url);

    this.socket.onmessage = (message) => {
      onEvent(JSON.parse(message.data) as AgentEvent);
    };
  }

  disconnect() {
    this.socket?.close();
  }
}
