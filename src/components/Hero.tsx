import { useEffect, useRef, useState } from 'react'
import { motion, useMotionValue, useSpring } from 'framer-motion'
import { ArrowRight, Github, Terminal, Sparkles } from 'lucide-react'
import SwarmCanvas from './SwarmCanvas'

export default function Hero() {
  const ref = useRef<HTMLDivElement>(null)
  const mx = useMotionValue(0)
  const my = useMotionValue(0)
  const sx = useSpring(mx, { stiffness: 60, damping: 20 })
  const sy = useSpring(my, { stiffness: 60, damping: 20 })
  const [typed, setTyped] = useState('')

  const phrase = 'queen.run("build, adapt, repair")'

  useEffect(() => {
    let i = 0
    let forward = true
    let timer: ReturnType<typeof setTimeout>
    const tick = () => {
      setTyped(phrase.slice(0, i))
      if (forward) {
        i++
        if (i > phrase.length + 30) forward = false
      } else {
        i--
        if (i < 0) {
          i = 0
          forward = true
        }
      }
      timer = setTimeout(tick, forward ? 60 + Math.random() * 40 : 25)
    }
    timer = setTimeout(tick, 800)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!ref.current) return
      const rect = ref.current.getBoundingClientRect()
      mx.set(((e.clientX - rect.left) / rect.width - 0.5) * 30)
      my.set(((e.clientY - rect.top) / rect.height - 0.5) * 30)
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [mx, my])

  return (
    <section id="top" ref={ref} className="relative min-h-screen w-full overflow-hidden bg-[#0a0a0a]">
      <div className="absolute inset-0 grid-bg grid-bg-fade opacity-50" />
      <SwarmCanvas density={0.00012} />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#0a0a0a]" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-[#0a0a0a]" />
      <div className="absolute left-0 top-0 h-full w-px bg-gradient-to-b from-transparent via-amber-500/20 to-transparent" />
      <div className="absolute right-0 top-0 h-full w-px bg-gradient-to-b from-transparent via-amber-500/20 to-transparent" />

      <div className="relative z-10 mx-auto flex min-h-screen max-w-7xl flex-col items-center justify-center px-6 pt-32 pb-20">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="mb-8 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/5 px-4 py-1.5 text-xs font-medium text-amber-400 backdrop-blur-sm">
          <span className="relative flex h-1.5 w-1.5"><span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" /><span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-amber-500" /></span>
          <span className="font-mono uppercase tracking-wider">Adaptive Intelligence · OpenRouter Runtime</span>
        </motion.div>

        <motion.div style={{ x: sx, y: sy }} className="relative">
          <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.8 }} className="text-center font-display text-6xl font-bold leading-[0.95] tracking-tight text-white sm:text-7xl md:text-8xl lg:text-9xl">
            <span className="block">One intelligence.</span>
            <span className="block text-zinc-500">A swarm at</span>
            <span className="block"><span className="relative inline-block"><span className="shimmer-text">your command</span><svg className="absolute -bottom-2 left-0 w-full" viewBox="0 0 300 12" fill="none" preserveAspectRatio="none"><path d="M2 8 Q 75 2, 150 6 T 298 5" stroke="url(#underline-grad)" strokeWidth="2" fill="none" strokeLinecap="round" /><defs><linearGradient id="underline-grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stopColor="#f59e0b" stopOpacity="0" /><stop offset="50%" stopColor="#f59e0b" stopOpacity="1" /><stop offset="100%" stopColor="#f59e0b" stopOpacity="0" /></linearGradient></defs></svg></span></span>
          </motion.h1>
        </motion.div>

        <motion.p initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.55 }} className="mt-8 max-w-2xl text-center text-base text-zinc-400 sm:text-lg">
          ANT AI is a personal autonomous agent framework with multi-agent swarm intelligence, OpenRouter model routing, hive-backed memory, and a blockchain-inspired audit system.{' '}
          <span className="text-zinc-200">One core. Many capabilities. Zero local-model baggage.</span>
        </motion.p>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className="mt-10 w-full max-w-2xl">
          <div className="overflow-hidden rounded-xl border border-white/10 bg-black/60 backdrop-blur-sm gradient-border">
            <div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-4 py-2.5"><div className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-red-500/70" /><span className="h-2.5 w-2.5 rounded-full bg-yellow-500/70" /><span className="h-2.5 w-2.5 rounded-full bg-green-500/70" /></div><div className="flex items-center gap-2 text-[10px] font-mono text-zinc-500"><Terminal className="h-3 w-3" />~/ant-ai</div><div className="text-[10px] font-mono text-zinc-600">openrouter</div></div>
            <div className="px-5 py-4 font-mono text-sm"><div className="flex items-center gap-2"><span className="text-amber-500">$</span><span className="text-zinc-300">{typed}</span><span className="h-4 w-2 bg-amber-500 pulse-dot" /></div></div>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.85 }} className="mt-10 flex flex-col sm:flex-row items-center gap-3">
          <a href="https://github.com/djny45/ANT-AI" target="_blank" rel="noreferrer" className="group inline-flex items-center gap-2 rounded-full bg-amber-500 px-6 py-3 text-sm font-semibold text-black transition-all hover:bg-amber-400 hover:shadow-[0_0_30px_-5px_rgba(245,158,11,0.6)]"><Github className="h-4 w-4" /><span>View on GitHub</span><ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" /></a>
          <a href="#architecture" className="group inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-6 py-3 text-sm font-medium text-white transition-all hover:bg-white/[0.08] hover:border-white/20"><Sparkles className="h-4 w-4 text-amber-400" /><span>Explore the architecture</span></a>
        </motion.div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.1 }} className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/5 text-left">
          {[
            { k: 'Language', v: 'Python' },
            { k: 'Runtime', v: 'OpenRouter' },
            { k: 'Memory', v: 'Pheromone Hive' },
            { k: 'Audit', v: 'Blockchain' },
          ].map((m) => <div key={m.k} className="bg-[#0a0a0a]/80 px-5 py-4 backdrop-blur-sm"><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">{m.k}</div><div className="mt-1 text-sm font-medium text-white">{m.v}</div></div>)}
        </motion.div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.4 }} className="absolute bottom-8 left-1/2 -translate-x-1/2"><div className="flex flex-col items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500"><span>scroll</span><div className="h-8 w-px bg-gradient-to-b from-amber-500 to-transparent" /></div></motion.div>
      </div>
    </section>
  )
}
