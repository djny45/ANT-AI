export const project = {
  name: 'ANT AI',
  fullName: 'Autonomous Neural Taskforce',
  tagline: 'Unified Adaptive Intelligence Operating System',
  description:
    'One intelligence. One core. Dynamic specialized nano-capabilities. Self-learning. Self-adapting. Self-repairing. Governed execution.',
  longDescription:
    'ANT AI is an adaptive intelligence platform built around a unified intelligence core. Instead of maintaining a fixed collection of agents, ANT dynamically creates specialized nano-capabilities when required, coordinates execution, verifies results, and integrates knowledge back into the core intelligence.',
  repo: 'https://github.com/djny45/ANT-AI',
  language: 'Python',
  stars: 1,
  forks: 0,
  issues: 8,
  topics: [
    'ai-agents',
    'swarm-intelligence',
    'llm-routing',
    'multi-agent',
    'autonomous-agents',
    'ollama',
    'openrouter',
  ],
}

export const capabilities = [
  {
    id: 'core',
    title: 'ANT Intelligence Core',
    subtitle: 'Queen Brain',
    description:
      'A single unified intelligence that orchestrates all nano-capabilities. Small tasks use minimal pathways; complex tasks spawn specialized units on demand.',
    icon: 'brain',
    color: 'amber',
  },
  {
    id: 'swarm',
    title: 'Adaptive Swarm',
    subtitle: 'Nano-Capabilities',
    description:
      'Dynamically decides what capabilities are required, how many specialized units to spawn, and when to combine or retire them.',
    icon: 'network',
    color: 'orange',
  },
  {
    id: 'routing',
    title: 'LLM Routing',
    subtitle: 'Ollama · OpenRouter',
    description:
      'Routes tasks to the optimal model provider. Local inference through Ollama for speed and privacy, OpenRouter for scale.',
    icon: 'route',
    color: 'amber',
  },
  {
    id: 'memory',
    title: 'Pheromone Memory',
    subtitle: 'Collective Knowledge',
    description:
      'Inspired by ant colonies. Useful discoveries leave pheromone trails that strengthen future decision-making.',
    icon: 'memory',
    color: 'orange',
  },
  {
    id: 'learning',
    title: 'Self-Learning Engine',
    subtitle: 'Pattern Discovery',
    description:
      'Learns engineering patterns from trusted open sources and converts them into controlled, verified capabilities.',
    icon: 'book',
    color: 'amber',
  },
  {
    id: 'repair',
    title: 'Self-Repair',
    subtitle: 'Minimal Verified Fixes',
    description:
      'Detects problems, performs root cause analysis, then generates and tests minimal repairs — never uncontrolled rewrites.',
    icon: 'wrench',
    color: 'orange',
  },
  {
    id: 'audit',
    title: 'Blockchain Audit',
    subtitle: 'Tamper-Evident Trail',
    description:
      'Every capability execution is signed and chained. Cryptographic verification of what was decided, when, and by whom.',
    icon: 'shield',
    color: 'amber',
  },
  {
    id: 'governance',
    title: 'Governance Layer',
    subtitle: 'Human Approval',
    description:
      'Critical operations pause for human review. Environment-based secrets. Controlled capability access at every level.',
    icon: 'gavel',
    color: 'orange',
  },
]

export const workflows = [
  {
    id: 'learning',
    label: 'Self-Learning',
    steps: [
      'Open Source Knowledge',
      'Pattern Understanding',
      'Capability Discovery',
      'Security / Quality Evaluation',
      'Skill Integration',
      'Testing and Verification',
      'Collective Knowledge Growth',
    ],
  },
  {
    id: 'repair',
    label: 'Self-Repair',
    steps: [
      'Problem Detection',
      'Root Cause Analysis',
      'Minimal Repair Generation',
      'Testing',
      'Verification',
      'System Improvement',
    ],
  },
  {
    id: 'pheromone',
    label: 'Pheromone Memory',
    steps: [
      'Nano Capability',
      'Experience Signal',
      'Collective Memory',
      'Future Decision Improvement',
    ],
  },
]

export const principles = [
  {
    title: 'Governance before execution',
    description: 'Every action is checked before it runs.',
  },
  {
    title: 'Verification after execution',
    description: 'Results are tested before becoming knowledge.',
  },
  {
    title: 'Controlled capability access',
    description: 'Capabilities stay scoped, monitored, revocable.',
  },
  {
    title: 'Audit tracking',
    description: 'Tamper-evident trail of every decision.',
  },
  {
    title: 'Environment-based secrets',
    description: 'No secrets in code. Ever.',
  },
  {
    title: 'Human approval boundaries',
    description: 'Critical operations pause for human review.',
  },
]

export const stats = [
  { label: 'Lines of Code', value: '12.4K', suffix: '' },
  { label: 'Capabilities', value: '24', suffix: '+' },
  { label: 'Models Supported', value: '60', suffix: '+' },
  { label: 'Verification Pipeline', value: '100', suffix: '%' },
]

export const codeSnippet = `# Start the ANT colony
from ant_ai import Colony, Queen

colony = Colony(
    router="ollama",          # or "openrouter"
    memory="pheromone",       # hive-backed collective memory
    audit="blockchain",       # tamper-evident trail
    governance="human-gated", # critical ops require approval
)

queen = Queen(colony)

# The Queen decides what capabilities to spawn
result = queen.run(
    goal="Refactor the auth module to use OAuth2",
    constraints={"minimal_changes": True, "verify": True},
)

# Verified, audited, and remembered for next time
print(result.summary)
`