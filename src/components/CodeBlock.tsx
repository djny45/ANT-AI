import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Copy, Terminal } from 'lucide-react'
import { codeSnippet } from '../data/project'

// Simple Python syntax tokenizer
function tokenize(code: string) {
  const keywords = ['from', 'import', 'print', 'for', 'in', 'if', 'else', 'def', 'return', 'class', 'with', 'as', 'True', 'False', 'None']
  const tokens: { type: string; value: string }[] = []
  let i = 0
  while (i < code.length) {
    const c = code[i]
    if (c === '#') {
      const end = code.indexOf('\n', i)
      const comment = end === -1 ? code.slice(i) : code.slice(i, end)
      tokens.push({ type: 'comment', value: comment })
      i += comment.length
    } else if (c === '"' || c === "'") {
      const quote = c
      let j = i + 1
      while (j < code.length && code[j] !== quote) {
        if (code[j] === '\\') j++
        j++
      }
      tokens.push({ type: 'string', value: code.slice(i, j + 1) })
      i = j + 1
    } else if (/[a-zA-Z_]/.test(c)) {
      let j = i
      while (j < code.length && /[a-zA-Z0-9_]/.test(code[j])) j++
      const word = code.slice(i, j)
      if (keywords.includes(word)) tokens.push({ type: 'keyword', value: word })
      else tokens.push({ type: 'identifier', value: word })
      i = j
    } else if (/[0-9]/.test(c)) {
      let j = i
      while (j < code.length && /[0-9.]/.test(code[j])) j++
      tokens.push({ type: 'number', value: code.slice(i, j) })
      i = j
    } else {
      tokens.push({ type: 'plain', value: c })
      i++
    }
  }
  return tokens
}

function highlight(code: string) {
  const tokens = tokenize(code)
  return tokens.map((t, i) => {
    switch (t.type) {
      case 'keyword':
        return (
          <span key={i} className="text-amber-400">
            {t.value}
          </span>
        )
      case 'string':
        return (
          <span key={i} className="text-emerald-400">
            {t.value}
          </span>
        )
      case 'comment':
        return (
          <span key={i} className="text-zinc-500 italic">
            {t.value}
          </span>
        )
      case 'number':
        return (
          <span key={i} className="text-orange-300">
            {t.value}
          </span>
        )
      case 'identifier':
        // Check if it's followed by (
        const next = tokens[i + 1]
        const isFunc = next && next.type === 'plain' && next.value === '('
        if (isFunc) {
          return (
            <span key={i} className="text-sky-300">
              {t.value}
            </span>
          )
        }
        if (/^[A-Z]/.test(t.value)) {
          return (
            <span key={i} className="text-white font-semibold">
              {t.value}
            </span>
          )
        }
        return (
          <span key={i} className="text-zinc-300">
            {t.value}
          </span>
        )
      default:
        return <span key={i}>{t.value}</span>
    }
  })
}

export default function CodeBlock() {
  const [copied, setCopied] = useState(false)

  const copy = () => {
    navigator.clipboard.writeText(codeSnippet)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <section id="code" className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-6"
        >
          <div className="max-w-2xl">
            <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400">
              <span className="h-px w-6 bg-amber-500" />
              Start a colony
            </div>
            <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
              Six lines.
              <br />
              <span className="text-zinc-500">A complete hive.</span>
            </h2>
          </div>
          <p className="text-zinc-400 max-w-md">
            Configure the colony, summon the Queen, and give it a goal. The
            intelligence decides what capabilities to spawn — you describe the
            outcome.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="group relative overflow-hidden rounded-3xl border border-white/10 bg-black/60 backdrop-blur-sm gradient-border"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-5 py-3">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-full bg-red-500/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-yellow-500/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-green-500/70" />
              </div>
              <div className="flex items-center gap-2 text-[10px] font-mono text-zinc-500">
                <Terminal className="h-3 w-3" />
                <span>examples/queen_run.py</span>
              </div>
            </div>
            <button
              onClick={copy}
              className="flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-mono text-zinc-300 transition-all hover:bg-white/10 hover:text-white"
            >
              {copied ? (
                <>
                  <Check className="h-3 w-3 text-emerald-400" />
                  <span>copied</span>
                </>
              ) : (
                <>
                  <Copy className="h-3 w-3" />
                  <span>copy</span>
                </>
              )}
            </button>
          </div>

          {/* Code body */}
          <pre className="overflow-x-auto px-6 py-6 font-mono text-sm leading-relaxed">
            <code>{highlight(codeSnippet)}</code>
          </pre>

          {/* Footer with command */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-t border-white/5 bg-white/[0.02] px-5 py-3">
            <div className="flex items-center gap-2 font-mono text-xs text-zinc-400">
              <span className="text-amber-500">$</span>
              <span>git clone https://github.com/djny45/ANT-AI</span>
            </div>
            <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500">
              <span>python</span>
              <span>·</span>
              <span>3.11+</span>
            </div>
          </div>

          {/* Corner glow */}
          <div className="absolute -top-1 -right-1 h-20 w-20 rounded-full bg-amber-500/10 blur-2xl" />
        </motion.div>
      </div>
    </section>
  )
}