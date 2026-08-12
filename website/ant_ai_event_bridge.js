// ANT-AI Hologram Event Bridge
// Connect this module to WebSocket agent events.

export const ANT_STATES = {
  IDLE: 'idle',
  LISTENING: 'listening',
  THINKING: 'thinking',
  RESPONDING: 'responding'
};

export function updateSphereGlow(state, sphere) {
  if (!sphere) return;

  switch (state) {
    case ANT_STATES.LISTENING:
      sphere.material.emissiveIntensity = 1.8;
      break;

    case ANT_STATES.THINKING:
      sphere.material.emissiveIntensity = 3.0;
      break;

    case ANT_STATES.RESPONDING:
      sphere.material.emissiveIntensity = 2.2;
      break;

    default:
      sphere.material.emissiveIntensity = 1.0;
  }
}

// Example WebSocket integration:
// ws.onmessage = (event) => {
//   const data = JSON.parse(event.data);
//   updateSphereGlow(data.agent_state, antSphere);
// };
