import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Brain,
  Network,
  Cpu,
  ShieldCheck,
  Database,
  Wrench,
  ArrowDown,
  Sparkles,
} from 'lucide-react'

interface NodeData {
  id: string
  label: string
  sub?: string
  icon: React.ReactNode
  x: number
  y: number
  description: string
}

const queenNode: NodeData = {
  id: 'queen',
  label: 'ANT Intelligence Core',
  sub: 'Queen Brain',
  icon: <Brain className="h-5 w-5" />,
  x: 50,
  y: 14,
  description:
    'A single unified intelligence. Routes tasks, decides what capabilities to spawn, coordinates execution, verifies results, and integrates knowledge back into the core.',
}

const nanos: NodeData[] = [
  {
    id: 'research',
    label: 'Research',
    sub: 'Nano',
    icon: <Sparkles className="h-4 w-4" />,
    x: 18,
    y: 48,
    description:
      'Spawned when knowledge gaps appear. Searches, reads, synthesizes, and reports findings back to the Queen.',
  },
  {
    id: 'dev',
    label: 'Development',
    sub: 'Nano',
    icon: <Cpu className="h-4 w-4" />,
    x: 38,
    y: 48,
    description:
      'Generated for code work. Repository understanding, pattern analysis, refactoring, testing — all under governance.',
  },
  {
    id: 'analysis',
    label: 'Analysis',
    sub: 'Nano',
    icon: <Database className="h-4 w-4" />,
    x: 58,
    y: 48,
    description:
      'Specialized for inspection. Audits code, detects bugs, profiles performance, surfaces optimization opportunities.',
  },
  {
    id: 'repair',
    label: 'Repair',
    sub: 'Nano',
    icon: <Wrench className="h-4 w-4" />,
    x: 78,
    y: 48,
    description:
      'Triggered by failures. Diagnoses root cause, generates minimal verified fixes, and tests before integrating.',
  },
]

const systems: NodeData[] = [
  {
    id: 'memory',
    label: 'Pheromone Memory',
    sub: 'Collective Knowledge',
    icon: <Database className="h-4 w-4" />,
    x: 25,
    y: 82,
    description:
      'Useful discoveries leave trails that strengthen future decisions. A hive memory shared across all capabilities.',
  },
  {
    id: 'audit',
    label: 'Blockchain Audit',
    sub: 'Tamper-Evident',
    icon: <ShieldCheck className="h-4 w-4" />,
    x: 50,
    y: 82,
    description:
      'Every capability execution is signed and chained. Cryptographic proof of what was decided, when, and by whom.',
  },
  {
    id: 'governance',
    label: 'Governance',
    sub: 'Human Approval',
    icon: <ShieldCheck className="h-4 w-4" />,
    x: 75,
    y: 82,
    description:
      'Critical operations pause for human review. Environment-based secrets. Controlled capability access.',
  },
]

const connections = [
  { from: 'queen', to: 'research' },
  { from: 'queen', to: 'dev' },
  { from: 'queen', to: 'analysis' },
  { from: 'queen', to: 'repair' },
  { from: 'research', to: 'memory' },
  { from: 'dev', to: 'audit' },
  { from: 'analysis', to: 'governance' },
  { from: 'repair', to: 'memory' },
  { from: 'repair', to: 'audit' },
]

function Node({
  node,
  active,
  onClick,
  isQueen,
}: {
  node: NodeData
  active: boolean
  onClick: () => void
  isQueen?: boolean
}) {
  return (
    <motion.button
      onClick={onClick}
      initial={{ opacity: 0, scale: 0.7 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ type: 'spring', stiffness: 220, damping: 22 }}
      whileHover={{ scale: isQueen ? 1.05 : 1.08 }}
      className="group absolute -translate-x-1/2 -translate-y-1/2"
      style={{ left: `${node.x}%`, top: `${node.y}%` }}
    >
      <div
        className={`relative rounded-2xl border transition-all ${
          isQueen
            ? 'border-amber-500/40 bg-gradient-to-br from-amber-500/15 to-orange-500/10 px-6 py-4 shadow-[0_0_40px_-10px_rgba(245,158,11,0.4)]'
            : 'border-white/10 bg-white/[0.03] px-3.5 py-2.5 hover:border-amber-500/30 hover:bg-white/[0.06]'
        } ${active ? 'ring-2 ring-amber-500/50' : ''}`}
      >
        {isQueen && (
          <span className="absolute -top-1 -right-1 flex h-3 w-3">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" />
            <span className="relative inline-flex h-3 w-3 rounded-full bg-amber-500" />
          </span>
        )}
        <div className="flex items-center gap-2">
          <div
            className={`flex h-7 w-7 items-center justify-center rounded-lg ${
              isQueen
                ? 'bg-amber-500/20 text-amber-400'
                : 'bg-white/5 text-zinc-300 group-hover:text-amber-400 group-hover:bg-amber-500/10'
            } transition-colors`}
          >
            {node.icon}
          </div>
          <div className="text-left">
            <div
              className={`font-semibold leading-tight ${
                isQueen ? 'text-base text-white' : 'text-sm text-white'
              }`}
            >
              {node.label}
            </div>
            {node.sub && (
              <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mt-0.5">
                {node.sub}
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.button>
  )
}

export default function Architecture() {
  const [activeId, setActiveId] = useState<string>('queen')
  const active = [queenNode, ...nanos, ...systems].find((n) => n.id === activeId)

  return (
    <section
      id="architecture"
      className="relative w-full bg-[#0a0a0a] py-28 sm:py-36"
    >
      <div className="mx-auto max-w-7xl px-6">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 max-w-2xl"
        >
          <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
            <span className="h-px w-6 bg-amber-500" />
            Architecture
          </div>
          <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
            One core.
            <br />
            <span className="text-zinc-500">Dynamic capabilities</span>
            <br />
            on demand.
          </h2>
          <p className="mt-6 text-zinc-400 max-w-xl">
            ANT AI is not a fixed collection of permanent agents. It is one
            intelligence that divides into specialized nano-units when needed.
            Click any node to see what it does.
          </p>
        </motion.div>

        {/* Diagram */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-3 relative aspect-[4/5] sm:aspect-[5/4] lg:aspect-square rounded-3xl border border-white/5 bg-gradient-to-br from-white/[0.02] to-transparent overflow-hidden">
            {/* Background grid */}
            <div className="absolute inset-0 grid-bg opacity-30" />
            {/* Corner crosses */}
            <div className="absolute left-3 top-3 text-[10px] font-mono text-zinc-600">
              fig. 01 / nano-brain
            </div>
            <div className="absolute right-3 top-3 flex items-center gap-1.5 text-[10px] font-mono text-zinc-600">
              <span className="h-1.5 w-1.5 rounded-full bg-amber-500 pulse-dot" />
              live
            </div>

            {/* SVG connections */}
            <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
              <defs>
                <linearGradient id="line-grad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.1" />
                </linearGradient>
                <radialGradient id="queen-glow">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.15" />
                  <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
                </radialGradient>
              </defs>

              {/* Queen glow */}
              <circle cx="50" cy="14" r="22" fill="url(#queen-glow)" />

              {/* Connections */}
              {connections.map((c, i) => {
                const fromNode =
                  c.from === 'queen'
                    ? queenNode
                    : [...nanos, ...systems].find((n) => n.id === c.from)
                const toNode = [...nanos, ...systems].find((n) => n.id === c.to)
                if (!fromNode || !toNode) return null
                const isActive = activeId === c.from || activeId === c.to
                return (
                  <line
                    key={i}
                    x1={fromNode.x}
                    y1={fromNode.y + (c.from === 'queen' ? 3 : 2.5)}
                    x2={toNode.x}
                    y2={toNode.y - (c.to === 'queen' ? 3 : 2.5)}
                    stroke={isActive ? '#f59e0b' : '#3f3f46'}
                    strokeWidth={isActive ? 0.4 : 0.25}
                    className={isActive ? 'flow-line' : ''}
                  />
                )
              })}

              {/* Data dots traveling */}
              {connections.slice(0, 4).map((c, i) => (
                <circle key={`dot-${i}`} r="0.5" fill="#f59e0b">
                  <animateMotion
                    dur={`${2 + i * 0.3}s`}
                    repeatCount="indefinite"
                    path={`M ${queenNode.x} ${queenNode.y + 3} L ${nanos[i].x} ${nanos[i].y - 2.5}`}
                  />
                  <animate
                    attributeName="opacity"
                    values="0;1;1;0"
                    dur={`${2 + i * 0.3}s`}
                    repeatCount="indefinite"
                  />
                </circle>
              ))}
            </svg>

            {/* Layer labels */}
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[9px] font-mono uppercase tracking-widest text-zinc-600 [writing-mode:vertical-rl] rotate-180">
              Nano Layer
            </div>
            <div className="absolute left-3 bottom-3 text-[9px] font-mono uppercase tracking-widest text-zinc-600">
              Systems
            </div>

            {/* Nodes */}
            <Node
              node={queenNode}
              active={activeId === 'queen'}
              onClick={() => setActiveId('queen')}
              isQueen
            />
            {nanos.map((n) => (
              <Node
                key={n.id}
                node={n}
                active={activeId === n.id}
                onClick={() => setActiveId(n.id)}
              />
            ))}
            {systems.map((n) => (
              <Node
                key={n.id}
                node={n}
                active={activeId === n.id}
                onClick={() => setActiveId(n.id)}
              />
            ))}

            {/* Arrow flow indicators */}
            <motion.div
              animate={{ y: [0, 6, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="absolute left-1/2 -translate-x-1/2"
              style={{ top: '32%' }}
            >
              <ArrowDown className="h-4 w-4 text-amber-500/60" />
            </motion.div>
          </div>

          {/* Detail panel */}
          <div className="lg:col-span-2 relative">
            <motion.div
              key={activeId}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="rounded-3xl border border-white/10 bg-white/[0.02] p-8 backdrop-blur-sm gradient-border lg:sticky lg:top-24"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
                  {active?.icon}
                </div>
                <div>
                  <div className="text-xs font-mono uppercase tracking-widest text-zinc-500">
                    {active?.sub}
                  </div>
                  <div className="text-xl font-bold text-white">{active?.label}</div>
                </div>
              </div>

              <p className="mt-6 text-zinc-400 leading-relaxed">
                {active?.description}
              </p>

              {/* Mini visual */}
              <div className="mt-8 rounded-2xl border border-white/5 bg-black/40 p-5">
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">
                  Telemetry
                </div>
                <div className="space-y-2">
                  {[
                    { k: 'Status', v: 'online' },
                    { k: 'Spawn cost', v: 'minimal' },
                    { k: 'Lifetime', v: 'on-demand' },
                    { k: 'Governance', v: 'enforced' },
                  ].map((row) => (
                    <div
                      key={row.k}
                      className="flex items-center justify-between text-xs"
                    >
                      <span className="font-mono text-zinc-500">{row.k}</span>
                      <span className="text-zinc-200">{row.v}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-4 h-1.5 rounded-full bg-white/5 overflow-hidden">
                  <motion.div
                    key={`bar-${activeId}`}
                    initial={{ width: 0 }}
                    animate={{ width: '78%' }}
                    transition={{ duration: 1.2, ease: 'easeOut' }}
                    className="h-full bg-gradient-to-r from-amber-500 to-orange-500"
                  />
                </div>
              </div>

              {/* All nodes list */}
              <div className="mt-8">
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">
                  Components
                </div>
                <div className="space-y-1">
                  {[queenNode, ...nanos, ...systems].map((n) => (
                    <button
                      key={n.id}
                      onClick={() => setActiveId(n.id)}
                      className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-1.5 text-left text-xs transition-colors ${
                        activeId === n.id
                          ? 'bg-amber-500/10 text-amber-300'
                          : 'text-zinc-400 hover:bg-white/5 hover:text-white'
                      }`}
                    >
                      <div
                        className={`h-1.5 w-1.5 rounded-full ${
                          activeId === n.id
                            ? 'bg-amber-500'
                            : 'bg-zinc-700'
                        }`}
                      />
                      <span className="font-medium">{n.label}</span>
                      {n.sub && (
                        <span className="ml-auto font-mono text-[10px] uppercase text-zinc-600">
                          {n.sub}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}