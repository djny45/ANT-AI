# CLAW CORE 10X Holographic Sphere

## Vision
Minimal AI interface. No dashboard. No extra panels.
Only a living holographic intelligence sphere.

## Rendering
- Three.js WebGL core
- Custom shader glow
- Volumetric light effect
- Particle-based energy field
- Smooth rotation

## Agent States

IDLE
- Low intensity orange glow
- Slow energy breathing

LISTENING
- Voice input detected
- Reactive pulse from microphone volume

THINKING
- High energy core pulse
- Faster light movement

RESPONDING
- Smooth expansion wave
- Return to idle state

## CLAW Integration

Frontend receives ANT-AI events through WebSocket:

voice_input -> LISTENING
agent_reasoning -> THINKING
answer_ready -> RESPONDING

## Design Rules

- Remove Jarvis references
- Keep CLAW branding
- Keep single command bar
- Full screen cinematic interface
