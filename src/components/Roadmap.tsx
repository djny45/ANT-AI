import { motion } from 'framer-motion'
import { CheckCircle2, Circle, Loader } from 'lucide-react'

const items = [
  { label: 'ANT Core intelligence engine', state: 'done' },
  { label: 'Adaptive orchestration', state: 'done' },
  { label: 'Nano-capability architecture', state: 'done' },
  { label: 'Self-learning framework', state: 'done' },
  { label: 'Self-repair workflows', state: 'done' },
  { label: 'Collective memory design', state: 'done' },
  { label: 'Development intelligence workflows', state: 'progress' },
  { label: 'End-to-end verification pipeline', state: 'progress' },
  { label: 'Multi-modal capability extension', state: 'planned' },
  { label: 'Distributed swarm across machines', state: 'planned' },
]

function StateIcon({ state }: { state: string }) {
  if (state === 'done') return <CheckCircle2 className="h-4 w-4 text-emerald-400" />
  if (state === 'progress')
    return <Loader className="h-4 w-4 text-amber-400 animate-spin" />
  return <Circle className="h-4 w-4 text-zinc-600" />
}

export default function Roadmap() {
  return (
    <section className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
              <span className="h-px w-6 bg-amber-500" />
              Status
            </div>
            <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl">
              Built in the open.
              <br />
              <span className="text-zinc-500">Shipped piece by piece.</span>
            </h2>
            <p className="mt-6 max-w-md text-zinc-400">
              ANT AI is in active development. The core is operational; the
              swarm is learning. Every commit is auditable on GitHub.
            </p>

            {/* Stats card */}
            <div className="mt-10 grid grid-cols-3 gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/5">
              {[
                { v: '6', l: 'Done' },
                { v: '2', l: 'In progress' },
                { v: '2', l: 'Planned' },
              ].map((s) => (
                <div key={s.l} className="bg-[#0a0a0a] px-4 py-5">
                  <div className="font-display text-3xl font-bold text-white">
                    {s.v}
                  </div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                    {s.l}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Timeline */}
          <div className="relative">
            <div className="absolute left-[7px] top-2 bottom-2 w-px bg-gradient-to-b from-amber-500/30 via-white/10 to-transparent" />
            <div className="space-y-3">
              {items.map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, x: 10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: '-30px' }}
                  transition={{ duration: 0.3, delay: i * 0.04 }}
                  className="group relative flex items-center gap-4 rounded-xl border border-white/[0.06] bg-white/[0.015] px-4 py-3 transition-all hover:border-amber-500/30 hover:bg-white/[0.04]"
                >
                  <div className="relative flex h-3.5 w-3.5 items-center justify-center">
                    <div className="absolute inset-0 rounded-full bg-[#0a0a0a]" />
                    <div
                      className={`relative h-2 w-2 rounded-full ${
                        item.state === 'done'
                          ? 'bg-emerald-400'
                          : item.state === 'progress'
                            ? 'bg-amber-400 pulse-dot'
                            : 'bg-zinc-700'
                      }`}
                    />
                  </div>
                  <div className="flex-1 text-sm text-white">{item.label}</div>
                  <div className="flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                    <StateIcon state={item.state} />
                    {item.state === 'done'
                      ? 'shipped'
                      : item.state === 'progress'
                        ? 'active'
                        : 'queued'}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}