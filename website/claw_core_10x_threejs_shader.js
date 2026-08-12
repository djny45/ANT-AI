// CLAW CORE 10X - Three.js holographic sphere controller
// Minimal cinematic AI core interface

export const CLAW_STATES = {
  IDLE: 'idle',
  LISTENING: 'listening',
  THINKING: 'thinking',
  RESPONDING: 'responding'
};

export function applyClawEnergy(state, core) {
  if (!core) return;

  const levels = {
    idle: 1.0,
    listening: 2.0,
    thinking: 3.5,
    responding: 2.5
  };

  core.energy = levels[state] || levels.idle;
}

export function createClawPulse(time, energy = 1) {
  return 1 + Math.sin(time * 0.003) * 0.05 * energy;
}

// Connect this module with ANT-AI WebSocket events:
// agent_state -> applyClawEnergy(agent_state, clawCore)
