import { Github } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="relative w-full bg-[#0a0a0a] border-t border-white/5 py-12">
      <div className="mx-auto max-w-7xl px-6">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
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
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold text-white">ANT AI</span>
              <span className="text-[10px] font-mono text-zinc-500">
                Autonomous Neural Taskforce
              </span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs text-zinc-500">
            <a
              href="https://github.com/djny45/ANT-AI"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 transition-colors hover:text-white"
            >
              <Github className="h-3.5 w-3.5" />
              Source
            </a>
            <a
              href="https://github.com/djny45/ANT-AI/issues"
              target="_blank"
              rel="noreferrer"
              className="transition-colors hover:text-white"
            >
              Issues
            </a>
            <a
              href="https://github.com/djny45/ANT-AI#readme"
              target="_blank"
              rel="noreferrer"
              className="transition-colors hover:text-white"
            >
              README
            </a>
            <span className="text-zinc-700">·</span>
            <span>MIT License</span>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-[10px] font-mono uppercase tracking-widest text-zinc-600">
          <span>Built by the swarm · for the swarm</span>
          <span>v0.1 · alpha · 2026</span>
        </div>
      </div>
    </footer>
  )
}