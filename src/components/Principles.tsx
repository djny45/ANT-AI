import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { ShieldCheck, Zap, GitBranch, Lock, KeyRound, UserCheck } from 'lucide-react'
import { principles } from '../data/project'

const icons = [ShieldCheck, Zap, GitBranch, Lock, KeyRound, UserCheck]

function Counter({ to, suffix = '' }: { to: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null)
  const [val, setVal] = useState(0)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          const start = performance.now()
          const dur = 1500
          const tick = (now: number) => {
            const p = Math.min(1, (now - start) / dur)
            const eased = 1 - Math.pow(1 - p, 3)
            setVal(Math.floor(to * eased))
            if (p < 1) requestAnimationFrame(tick)
          }
          requestAnimationFrame(tick)
          obs.disconnect()
        }
      },
      { threshold: 0.5 },
    )
    obs.observe(node)
    return () => obs.disconnect()
  }, [to])

  return (
    <span ref={ref}>
      {val}
      {suffix}
    </span>
  )
}

const stats = [
  { value: 100, suffix: '%', label: 'Verified', sub: 'Every result tested before integration' },
  { value: 1, suffix: '', label: 'Intelligence', sub: 'One core, many capabilities' },
  { value: 0, suffix: '', label: 'Permanent agents', sub: 'Capabilities spawn on demand' },
  { value: 6, suffix: '', label: 'Security layers', sub: 'Governance is not optional' },
]

export default function Principles() {
  return (
    <section
      id="principles"
      className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5"
    >
      {/* Subtle backdrop glow */}
      <div className="absolute inset-x-0 top-0 mx-auto h-96 max-w-5xl rounded-full bg-amber-500/5 blur-3xl" />

      <div className="relative mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 max-w-2xl"
        >
          <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
            <span className="h-px w-6 bg-amber-500" />
            Principles
          </div>
          <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
            Governed by design.
            <br />
            <span className="text-zinc-500">Verified by default.</span>
          </h2>
        </motion.div>

        {/* Stats */}
        <div className="mb-16 grid grid-cols-2 lg:grid-cols-4 gap-px overflow-hidden rounded-3xl border border-white/10 bg-white/5">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="group relative bg-[#0a0a0a]/90 p-8 transition-colors hover:bg-[#0a0a0a]/70"
            >
              <div className="font-display text-5xl font-bold text-white sm:text-6xl">
                <span className="bg-gradient-to-br from-white to-zinc-500 bg-clip-text text-transparent">
                  <Counter to={s.value} suffix={s.suffix} />
                </span>
              </div>
              <div className="mt-3 text-sm font-semibold text-amber-400">
                {s.label}
              </div>
              <div className="mt-1 text-xs text-zinc-500">{s.sub}</div>
              <div className="absolute bottom-0 left-0 h-px w-0 bg-gradient-to-r from-amber-500 to-orange-500 transition-all duration-500 group-hover:w-full" />
            </motion.div>
          ))}
        </div>

        {/* Principles grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {principles.map((p, i) => {
            const Icon = icons[i]
            return (
              <motion.div
                key={p.title}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.4, delay: i * 0.05 }}
                className="group relative overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.015] p-6 transition-all hover:border-amber-500/30 hover:bg-white/[0.03]"
              >
                <div className="flex items-start gap-4">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-amber-500/10 text-amber-400 group-hover:bg-amber-500/20 transition-colors">
                    <Icon className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                      Principle · {String(i + 1).padStart(2, '0')}
                    </div>
                    <h3 className="mt-1 text-base font-semibold text-white">
                      {p.title}
                    </h3>
                    <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
                      {p.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}