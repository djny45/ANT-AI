import { motion } from 'framer-motion'
import { Github, Star, GitFork, ArrowUpRight, Sparkles } from 'lucide-react'
import { project } from '../data/project'
import SwarmCanvas from './SwarmCanvas'

export default function CTA() {
  return (
    <section className="relative w-full overflow-hidden bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5">
      {/* Background swarm */}
      <div className="absolute inset-0">
        <SwarmCanvas density={0.00005} />
      </div>

      {/* Center radial */}
      <div className="absolute inset-0 bg-gradient-radial from-transparent via-[#0a0a0a]/80 to-[#0a0a0a]" />

      <div className="relative mx-auto max-w-4xl px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
        >
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/5 px-4 py-1.5 text-xs font-medium text-amber-400 backdrop-blur-sm">
            <Sparkles className="h-3.5 w-3.5" />
            <span className="font-mono uppercase tracking-wider">
              Open source · MIT
            </span>
          </div>

          <h2 className="font-display text-5xl font-bold leading-[1.05] text-white sm:text-6xl md:text-7xl">
            Run the colony.
            <br />
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Watch it learn.
            </span>
          </h2>

          <p className="mx-auto mt-6 max-w-xl text-base text-zinc-400 sm:text-lg">
            Clone the repo, install the requirements, and start the Queen.
            Every capability you spawn is verified, audited, and remembered.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-3">
            <a
              href={project.repo}
              target="_blank"
              rel="noreferrer"
              className="group inline-flex items-center gap-2 rounded-full bg-amber-500 px-7 py-3.5 text-sm font-semibold text-black transition-all hover:bg-amber-400 hover:shadow-[0_0_40px_-5px_rgba(245,158,11,0.6)]"
            >
              <Github className="h-4 w-4" />
              <span>Get started</span>
              <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </a>
            <a
              href={`${project.repo}#readme`}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-7 py-3.5 text-sm font-medium text-white transition-all hover:bg-white/[0.08] hover:border-white/20"
            >
              <span>Read the docs</span>
            </a>
          </div>

          {/* Repo meta */}
          <div className="mt-12 inline-flex flex-wrap items-center justify-center gap-3 rounded-full border border-white/10 bg-white/[0.02] px-2 py-2 backdrop-blur-sm">
            <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1.5 text-xs">
              <Star className="h-3 w-3 text-amber-400 fill-amber-400" />
              <span className="text-zinc-300">{project.stars}</span>
              <span className="text-zinc-500">stars</span>
            </div>
            <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1.5 text-xs">
              <GitFork className="h-3 w-3 text-zinc-400" />
              <span className="text-zinc-300">{project.forks}</span>
              <span className="text-zinc-500">forks</span>
            </div>
            <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1.5 text-xs">
              <span className="font-mono text-zinc-300">{project.language}</span>
              <span className="text-zinc-500">primary</span>
            </div>
            <div className="flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400">
              <span className="relative flex h-1.5 w-1.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500" />
              </span>
              <span className="font-mono">active</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}