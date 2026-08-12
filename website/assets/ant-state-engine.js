// ANT State Engine v1
// Controls visual states for future AI connection

const ANT_STATE = {
  IDLE: 'idle',
  LISTENING: 'listening',
  THINKING: 'thinking',
  RESPONSE: 'response'
};

let currentState = ANT_STATE.IDLE;

function setANTState(state) {
  currentState = state;
  document.body.setAttribute('data-ant-state', state);
  window.dispatchEvent(new CustomEvent('ant-state-change', {
    detail: { state }
  }));
}

function getANTState() {
  return currentState;
}

window.ANTState = {
  set: setANTState,
  get: getANTState,
  states: ANT_STATE
};

setANTState(ANT_STATE.IDLE);
