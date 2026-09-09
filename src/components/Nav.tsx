import { useEffect, useState } from 'react'
import { Github, Menu, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const links = [
  { href: '#architecture', label: 'Architecture' },
  { href: '#capabilities', label: 'Capabilities' },
  { href: '#workflows', label: 'Workflows' },
  { href: '#principles', label: 'Principles' },
  { href: '#code', label: 'Code' },
  { href: '#api-key', label: 'API Key' },
  { href: '#chat', label: 'Chat' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all ${
        scrolled
          ? 'border-b border-white/5 bg-[#0a0a0a]/80 backdrop-blur-xl'
          : 'bg-transparent'
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <a href="#top" className="flex items-center gap-2.5 group">
          <div className="relative">
            <div className="absolute inset-0 bg-amber-500/30 blur-md rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
            <svg width="24" height="24" viewBox="0 0 32 32" fill="none" className="relative">
              <circle cx="16" cy="17" r="6" fill="#f59e0b" />
              <circle cx="11" cy="9" r="2.2" fill="#fafafa" />
              <circle cx="21" cy="9" r="2.2" fill="#fafafa" />
              <circle cx="6" cy="15" r="2" fill="#fafafa" />
              <circle cx="26" cy="15" r="2" fill="#fafafa" />
              <circle cx="9" cy="25" r="2" fill="#fafafa" />
              <circle cx="23" cy="25" r="2" fill="#fafafa" />
              <g stroke="#fafafa" strokeWidth="1.2">
                <line x1="11" y1="9" x2="16" y2="17" />
                <line x1="21" y1="9" x2="16" y2="17" />
                <line x1="6" y1="15" x2="16" y2="17" />
                <line x1="26" y1="15" x2="16" y2="17" />
                <line x1="9" y1="25" x2="16" y2="17" />
                <line x1="23" y1="25" x2="16" y2="17" />
              </g>
            </svg>
          </div>
          <div className="flex flex-col leading-none">
            <span className="text-sm font-bold tracking-tight text-white">ANT&nbsp;AI</span>
            <span className="text-[10px] text-zinc-500 font-mono">v0.1 · alpha</span>
          </div>
        </a>

        <div className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="relative px-3 py-1.5 text-sm text-zinc-400 hover:text-white transition-colors group"
            >
              {l.label}
              <span className="absolute left-3 right-3 -bottom-0.5 h-px scale-x-0 bg-amber-500 transition-transform group-hover:scale-x-100" />
            </a>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <a
            href="https://github.com/djny45/ANT-AI"
            target="_blank"
            rel="noreferrer"
            className="hidden sm:inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm font-medium text-white hover:bg-white/10 hover:border-white/20 transition-all"
          >
            <Github className="h-3.5 w-3.5" />
            <span>Star on GitHub</span>
          </a>
          <button
            onClick={() => setOpen((s) => !s)}
            className="md:hidden p-2 rounded-lg hover:bg-white/5"
            aria-label="Toggle menu"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden overflow-hidden border-t border-white/5 bg-[#0a0a0a]/95 backdrop-blur-xl"
          >
            <div className="flex flex-col px-6 py-4 gap-1">
              {links.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="px-3 py-2 text-sm text-zinc-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                >
                  {l.label}
                </a>
              ))}
              <a
                href="https://github.com/djny45/ANT-AI"
                target="_blank"
                rel="noreferrer"
                className="mt-2 inline-flex items-center justify-center gap-2 rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white"
              >
                <Github className="h-3.5 w-3.5" />
                Star on GitHub
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}