import { motion } from 'framer-motion'
import { ArrowRight, BrainCircuit, Layers3, Network, Sparkles } from 'lucide-react'

const layers = [
  { label: 'Cognitive Kernel', icon: BrainCircuit },
  { label: 'Memory + Knowledge', icon: Layers3 },
  { label: 'Learning & Evolution', icon: Sparkles },
  { label: 'Intelligence Mesh', icon: Network },
]

export default function NovaCore() {
  return (
    <section id="nova-core" className="relative w-full bg-[#0a0a0a] py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative overflow-hidden rounded-3xl border border-amber-500/15 bg-gradient-to-br from-amber-500/[0.06] via-white/[0.02] to-transparent p-7 sm:p-10"
        >
          <div className="absolute -right-24 -top-24 h-56 w-56 rounded-full bg-amber-500/10 blur-3xl" />
          <div className="relative grid gap-8 lg:grid-cols-[1.1fr_1fr] lg:items-center">
            <div>
              <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
                <span className="h-px w-6 bg-amber-500" />
                NOVA Core
              </div>
              <h2 className="font-display text-3xl font-bold leading-tight text-white sm:text-4xl">
                The deeper intelligence layer behind the swarm.
              </h2>
              <p className="mt-4 max-w-xl text-sm leading-relaxed text-zinc-400 sm:text-base">
                NOVA Core is the adaptive intelligence operating-system architecture for cognitive processing, memory, autonomous agents, learning, simulation, governance, and distributed intelligence.
              </p>
              <a
                href="/docs/nova-core-overview.html"
                className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-amber-400 transition-colors hover:text-amber-300"
              >
                Explore NOVA Core <ArrowRight className="h-4 w-4" />
              </a>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {layers.map(({ label, icon: Icon }, index) => (
                <motion.div
                  key={label}
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.08, duration: 0.35 }}
                  className="rounded-2xl border border-white/10 bg-black/30 p-4 backdrop-blur-sm"
                >
                  <Icon className="h-5 w-5 text-amber-400" />
                  <div className="mt-3 text-sm font-medium text-white">{label}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-wider text-zinc-600">
                    NOVA layer
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
