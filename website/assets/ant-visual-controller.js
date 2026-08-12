// ANT Visual Controller
// Connects AI states to sphere visual reactions

const ANTVisualController = {
  state: 'idle',
  setState(nextState) {
    this.state = nextState;
    document.dispatchEvent(new CustomEvent('ant-state-change', {
      detail: { state: nextState }
    }));
  },
  idle(){ this.setState('idle'); },
  listening(){ this.setState('listening'); },
  thinking(){ this.setState('thinking'); },
  response(){ this.setState('response'); }
};

window.ANTVisualController = ANTVisualController;
