import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Brain,
  Network,
  Route as RouteIcon,
  Database,
  BookOpen,
  Wrench,
  Shield,
  Gavel,
  LucideIcon,
} from 'lucide-react'
import { capabilities } from '../data/project'

const iconMap: Record<string, LucideIcon> = {
  brain: Brain,
  network: Network,
  route: RouteIcon,
  memory: Database,
  book: BookOpen,
  wrench: Wrench,
  shield: Shield,
  gavel: Gavel,
}

export default function Capabilities() {
  const [hovered, setHovered] = useState<string | null>(null)

  return (
    <section
      id="capabilities"
      className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5"
    >
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 flex flex-col md:flex-row md:items-end md:justify-between gap-6"
        >
          <div className="max-w-2xl">
            <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
              <span className="h-px w-6 bg-amber-500" />
              Capabilities
            </div>
            <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
              Eight systems.
              <br />
              <span className="text-zinc-500">One intelligence.</span>
            </h2>
          </div>
          <p className="text-zinc-400 max-w-md">
            Each capability is a small, focused unit that the Queen spawns only
            when the goal demands it. Hover to peek.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {capabilities.map((c, i) => {
            const Icon = iconMap[c.icon]
            return (
              <motion.div
                key={c.id}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.4, delay: i * 0.04 }}
                onMouseEnter={() => setHovered(c.id)}
                onMouseLeave={() => setHovered(null)}
                className="group relative cursor-pointer"
              >
                <div
                  className={`relative h-full overflow-hidden rounded-2xl border bg-white/[0.015] p-5 transition-all duration-300 ${
                    hovered === c.id
                      ? 'border-amber-500/40 bg-white/[0.04] -translate-y-1'
                      : 'border-white/[0.06]'
                  }`}
                >
                  {/* Background number */}
                  <div className="absolute -top-2 -right-2 font-display text-7xl font-bold text-white/[0.03] select-none">
                    {String(i + 1).padStart(2, '0')}
                  </div>

                  {/* Glow */}
                  <AnimatePresence>
                    {hovered === c.id && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute -inset-px rounded-2xl bg-gradient-to-br from-amber-500/20 via-transparent to-orange-500/10 -z-10 blur-sm"
                      />
                    )}
                  </AnimatePresence>

                  {/* Icon */}
                  <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-white/[0.04] text-zinc-300 group-hover:bg-amber-500/15 group-hover:text-amber-400 transition-all">
                    <Icon className="h-5 w-5" />
                  </div>

                  {/* Sub label */}
                  <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                    {c.subtitle}
                  </div>

                  {/* Title */}
                  <h3 className="mt-1 text-lg font-semibold text-white">
                    {c.title}
                  </h3>

                  {/* Description */}
                  <p className="mt-3 text-sm leading-relaxed text-zinc-400">
                    {c.description}
                  </p>

                  {/* Bottom indicator */}
                  <div className="mt-5 flex items-center justify-between">
                    <div className="h-px flex-1 bg-gradient-to-r from-white/10 to-transparent" />
                    <div className="ml-3 font-mono text-[10px] text-zinc-600">
                      {String(i + 1).padStart(2, '0')} / {capabilities.length}
                    </div>
                  </div>

                  {/* Hover line */}
                  <motion.div
                    initial={{ scaleX: 0 }}
                    animate={{ scaleX: hovered === c.id ? 1 : 0 }}
                    transition={{ duration: 0.3 }}
                    className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-amber-500 to-transparent origin-center"
                  />
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Bottom: live indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3 }}
          className="mt-12 flex items-center justify-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500"
        >
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" />
            <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-amber-500" />
          </span>
          all systems nominal · capabilities spawned on demand
        </motion.div>
      </div>
    </section>
  )
}