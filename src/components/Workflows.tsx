import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { workflows } from '../data/project'
import { BookOpen, Wrench, Database, ChevronRight } from 'lucide-react'

const icons = [BookOpen, Wrench, Database]

export default function Workflows() {
  const [active, setActive] = useState(workflows[0].id)
  const current = workflows.find((w) => w.id === active)!
  const ActiveIcon = icons[workflows.findIndex((w) => w.id === active)]

  return (
    <section
      id="workflows"
      className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5"
    >
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 max-w-2xl"
        >
          <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
            <span className="h-px w-6 bg-amber-500" />
            Workflows
          </div>
          <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
            Self-learning.
            <br />
            Self-adapting.
            <br />
            <span className="text-zinc-500">Self-repairing.</span>
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Tabs */}
          <div className="lg:col-span-4 space-y-2">
            {workflows.map((w, i) => {
              const Icon = icons[i]
              const isActive = active === w.id
              return (
                <button
                  key={w.id}
                  onClick={() => setActive(w.id)}
                  className={`group relative w-full overflow-hidden rounded-2xl border p-5 text-left transition-all ${
                    isActive
                      ? 'border-amber-500/40 bg-gradient-to-br from-amber-500/10 to-orange-500/5'
                      : 'border-white/5 bg-white/[0.02] hover:border-white/15 hover:bg-white/[0.04]'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="workflow-tab-bg"
                      className="absolute inset-0 -z-10 bg-gradient-to-br from-amber-500/10 to-orange-500/5"
                      transition={{ type: 'spring', stiffness: 220, damping: 28 }}
                    />
                  )}
                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-xl transition-colors ${
                        isActive
                          ? 'bg-amber-500/20 text-amber-400'
                          : 'bg-white/5 text-zinc-400 group-hover:text-white'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                      <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        workflow · {String(i + 1).padStart(2, '0')}
                      </div>
                      <div
                        className={`mt-0.5 text-lg font-semibold ${
                          isActive ? 'text-white' : 'text-zinc-300'
                        }`}
                      >
                        {w.label}
                      </div>
                    </div>
                    <ChevronRight
                      className={`h-4 w-4 transition-all ${
                        isActive
                          ? 'text-amber-400 translate-x-1'
                          : 'text-zinc-600'
                      }`}
                    />
                  </div>
                </button>
              )
            })}
          </div>

          {/* Steps */}
          <div className="lg:col-span-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={current.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.3 }}
                className="relative rounded-3xl border border-white/10 bg-white/[0.02] p-8 backdrop-blur-sm gradient-border"
              >
                <div className="flex items-center gap-3 mb-8">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-500/15 text-amber-400">
                    {ActiveIcon && <ActiveIcon className="h-4 w-4" />}
                  </div>
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                      pipeline
                    </div>
                    <div className="text-base font-semibold text-white">
                      {current.label}
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  {current.steps.map((step, i) => (
                    <motion.div
                      key={step}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.08 }}
                      className="group flex items-center gap-4"
                    >
                      <div className="relative">
                        <div
                          className={`flex h-9 w-9 items-center justify-center rounded-full font-mono text-xs font-bold transition-all ${
                            i === current.steps.length - 1
                              ? 'bg-amber-500 text-black shadow-[0_0_20px_-2px_rgba(245,158,11,0.5)]'
                              : 'bg-white/5 text-zinc-300 group-hover:bg-amber-500/15 group-hover:text-amber-300'
                          }`}
                        >
                          {i + 1}
                        </div>
                        {i < current.steps.length - 1 && (
                          <div className="absolute top-9 left-1/2 h-3 w-px -translate-x-1/2 bg-gradient-to-b from-white/10 to-transparent" />
                        )}
                      </div>
                      <div className="flex-1 rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3 transition-all group-hover:border-amber-500/30 group-hover:bg-amber-500/[0.04]">
                        <div className="text-sm font-medium text-white">{step}</div>
                      </div>
                      <div className="hidden sm:block font-mono text-[10px] uppercase tracking-widest text-zinc-600">
                        step
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Verification indicator */}
                <div className="mt-8 flex items-center justify-between rounded-xl border border-amber-500/20 bg-amber-500/5 px-4 py-3">
                  <div className="flex items-center gap-2 text-xs text-amber-300">
                    <span className="relative flex h-1.5 w-1.5">
                      <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" />
                      <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-amber-500" />
                    </span>
                    Every step is verified before the next begins
                  </div>
                  <div className="font-mono text-[10px] text-zinc-500">
                    verified · enforced
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  )
}