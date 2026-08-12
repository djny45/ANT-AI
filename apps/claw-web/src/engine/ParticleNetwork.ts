export interface ParticleNetworkConfig {
  count: number;
  radius: number;
}

export function createParticleNetwork(config: ParticleNetworkConfig) {
  return {
    count: config.count,
    radius: config.radius,
  };
}
