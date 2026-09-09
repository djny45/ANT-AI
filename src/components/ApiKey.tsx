import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  KeyRound,
  Eye,
  EyeOff,
  Copy,
  Check,
  Server,
  Cloud,
  ShieldCheck,
  Trash2,
  Lock,
  Sparkles,
} from 'lucide-react'

type Provider = 'ollama' | 'openrouter'

const providers: {
  id: Provider
  label: string
  sub: string
  icon: React.ReactNode
  placeholder: string
  prefix: string
  docs: string
  hint: string
}[] = [
  {
    id: 'ollama',
    label: 'Ollama',
    sub: 'Local inference',
    icon: <Server className="h-4 w-4" />,
    placeholder: 'http://localhost:11434',
    prefix: 'OLLAMA_HOST',
    docs: 'https://ollama.com',
    hint: 'No API key required when running Ollama locally. Provide the host URL to point the Queen at your local daemon.',
  },
  {
    id: 'openrouter',
    label: 'OpenRouter',
    sub: 'Cloud models',
    icon: <Cloud className="h-4 w-4" />,
    placeholder: 'sk-or-v1-••••••••••••••••',
    prefix: 'OPENROUTER_API_KEY',
    docs: 'https://openrouter.ai/keys',
    hint: 'Route tasks to 60+ cloud models. The Queen picks the optimal one per capability.',
  },
]

function maskKey(k: string) {
  if (k.length <= 8) return '•'.repeat(k.length)
  return `${k.slice(0, 4)}${'•'.repeat(Math.max(4, k.length - 8))}${k.slice(-4)}`
}

export default function ApiKey() {
  const [active, setActive] = useState<Provider>('openrouter')
  const [show, setShow] = useState(false)
  const [value, setValue] = useState('')
  const [copied, setCopied] = useState<string | null>(null)

  const current = providers.find((p) => p.id === active)!
  const isOllama = active === 'ollama'

  const envSnippet = `${current.prefix}=${isOllama ? 'http://localhost:11434' : value || '<your-key>'}`

  const codeSnippet = `# .env — keep this file out of version control
${envSnippet}

# Optional: pin a default model
ANT_DEFAULT_MODEL=${active === 'openrouter' ? 'anthropic/claude-3.5-sonnet' : 'llama3.1:70b'}

# Optional: enable governance logging
ANT_AUDIT=${active === 'openrouter' ? 'blockchain' : 'local'}`

  const onCopy = (label: string, text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(label)
    setTimeout(() => setCopied(null), 1600)
  }

  const hasKey = value.trim().length > 0
  const isValidShape =
    isOllama ||
    value.startsWith('sk-or-') ||
    value.startsWith('sk-') ||
    value.length >= 20

  return (
    <section
      id="api-key"
      className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5"
    >
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
              Configure
            </div>
            <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">
              Wire up your colony.
              <br />
              <span className="text-zinc-500">Keys stay yours.</span>
            </h2>
          </div>
          <p className="text-zinc-400 max-w-md">
            ANT AI routes through the LLM provider you choose. Pick a tab,
            paste your key locally, and the Queen handles the rest — nothing is
            ever sent to a remote server except your provider of choice.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="grid grid-cols-1 lg:grid-cols-12 gap-6"
        >
          {/* Tab list */}
          <div className="lg:col-span-4 space-y-3">
            {providers.map((p) => {
              const isActive = active === p.id
              return (
                <button
                  key={p.id}
                  onClick={() => {
                    setActive(p.id)
                    setValue('')
                    setShow(false)
                  }}
                  className={`group relative w-full overflow-hidden rounded-2xl border p-5 text-left transition-all ${
                    isActive
                      ? 'border-amber-500/40 bg-gradient-to-br from-amber-500/10 to-orange-500/5'
                      : 'border-white/5 bg-white/[0.02] hover:border-white/15 hover:bg-white/[0.04]'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="api-tab-bg"
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
                      {p.icon}
                    </div>
                    <div className="flex-1">
                      <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        {p.sub}
                      </div>
                      <div
                        className={`mt-0.5 text-lg font-semibold ${
                          isActive ? 'text-white' : 'text-zinc-300'
                        }`}
                      >
                        {p.label}
                      </div>
                    </div>
                    <div
                      className={`flex h-5 w-5 items-center justify-center rounded-full border transition-all ${
                        isActive
                          ? 'border-amber-500 bg-amber-500'
                          : 'border-zinc-700'
                      }`}
                    >
                      {isActive && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="h-1.5 w-1.5 rounded-full bg-black"
                        />
                      )}
                    </div>
                  </div>
                </button>
              )
            })}

            {/* Security card */}
            <div className="mt-4 rounded-2xl border border-white/5 bg-white/[0.015] p-5">
              <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-zinc-500">
                <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
                Security
              </div>
              <ul className="mt-3 space-y-2 text-xs text-zinc-400">
                <li className="flex gap-2">
                  <span className="text-amber-500">·</span>
                  <span>Keys are read from <span className="font-mono text-zinc-200">.env</span> at runtime, never committed.</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-amber-500">·</span>
                  <span>Browser-only — nothing leaves this tab.</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-amber-500">·</span>
                  <span>Clear it any time with the trash button.</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Panel */}
          <div className="lg:col-span-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={active}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.25 }}
                className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-sm gradient-border"
              >
                {/* Header */}
                <div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-5 py-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400">
                      <KeyRound className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        {current.sub}
                      </div>
                      <div className="text-sm font-semibold text-white">
                        {current.label} configuration
                      </div>
                    </div>
                  </div>
                  <a
                    href={current.docs}
                    target="_blank"
                    rel="noreferrer"
                    className="hidden sm:inline-flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-widest text-zinc-400 transition-colors hover:text-amber-300"
                  >
                    <span>get a key</span>
                    <span>↗</span>
                  </a>
                </div>

                {/* Body */}
                <div className="px-6 py-7 sm:px-8 sm:py-9 space-y-7">
                  {/* Hint */}
                  <div className="flex items-start gap-3 rounded-xl border border-white/5 bg-white/[0.015] p-4">
                    <Sparkles className="h-4 w-4 mt-0.5 text-amber-400 shrink-0" />
                    <p className="text-xs text-zinc-400 leading-relaxed">
                      {current.hint}
                    </p>
                  </div>

                  {/* Input */}
                  <div>
                    <label className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        {isOllama ? 'Endpoint URL' : 'API Key'}
                      </span>
                      <span className="text-[10px] font-mono text-zinc-600">
                        {current.prefix}
                      </span>
                    </label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 flex items-center pl-4 text-zinc-500 group-focus-within:text-amber-400 transition-colors">
                        {isOllama ? <Server className="h-4 w-4" /> : <Lock className="h-4 w-4" />}
                      </div>
                      <input
                        type={isOllama ? 'text' : show ? 'text' : 'password'}
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                        placeholder={current.placeholder}
                        spellCheck={false}
                        autoComplete="off"
                        className="w-full rounded-xl border border-white/10 bg-black/40 py-3.5 pl-11 pr-28 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none focus:ring-2 focus:ring-amber-500/20 transition-all"
                      />
                      <div className="absolute inset-y-0 right-2 flex items-center gap-1">
                        {!isOllama && value && (
                          <button
                            type="button"
                            onClick={() => setShow((s) => !s)}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-white transition-colors"
                            aria-label={show ? 'Hide key' : 'Show key'}
                          >
                            {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                          </button>
                        )}
                        {value && (
                          <button
                            type="button"
                            onClick={() => setValue('')}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-rose-300 transition-colors"
                            aria-label="Clear key"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    </div>

                    {/* Status row */}
                    <div className="mt-3 flex items-center justify-between text-[10px] font-mono uppercase tracking-widest">
                      <div className="flex items-center gap-2">
                        {hasKey ? (
                          isValidShape ? (
                            <>
                              <span className="relative flex h-1.5 w-1.5">
                                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500" />
                              </span>
                              <span className="text-emerald-400">valid format</span>
                            </>
                          ) : (
                            <>
                              <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                              <span className="text-amber-400">unrecognized format</span>
                            </>
                          )
                        ) : (
                          <>
                            <span className="h-1.5 w-1.5 rounded-full bg-zinc-700" />
                            <span className="text-zinc-500">awaiting input</span>
                          </>
                        )}
                      </div>
                      <span className="text-zinc-600">
                        {value.length > 0 ? `${value.length} chars` : '—'}
                      </span>
                    </div>

                    {/* Strength bar (only for keys) */}
                    {!isOllama && value && (
                      <div className="mt-3 h-1 rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{
                            width: `${Math.min(100, (value.length / 40) * 100)}%`,
                          }}
                          transition={{ duration: 0.3 }}
                          className={`h-full ${
                            isValidShape
                              ? 'bg-gradient-to-r from-emerald-500 to-emerald-400'
                              : 'bg-gradient-to-r from-amber-500 to-orange-500'
                          }`}
                        />
                      </div>
                    )}
                  </div>

                  {/* Snippet */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        Generated <span className="text-zinc-300">.env</span> snippet
                      </span>
                      <button
                        onClick={() => onCopy('snippet', codeSnippet)}
                        className="inline-flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-mono uppercase tracking-widest text-zinc-300 transition-all hover:bg-white/10 hover:text-white"
                      >
                        {copied === 'snippet' ? (
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
                    <pre className="overflow-x-auto rounded-xl border border-white/10 bg-black/60 p-4 font-mono text-xs leading-relaxed">
                      <code>
                        <span className="text-zinc-500"># drop this into your </span>
                        <span className="text-zinc-300">.env</span>
                        <span className="text-zinc-500"> file</span>
                        {'\n'}
                        <span className="text-amber-400">{current.prefix}</span>
                        <span className="text-zinc-500">=</span>
                        <span className="text-emerald-400">
                          {isOllama
                            ? 'http://localhost:11434'
                            : show && value
                              ? value
                              : value
                                ? maskKey(value)
                                : '<your-key>'}
                        </span>
                        {'\n\n'}
                        <span className="text-amber-400">ANT_DEFAULT_MODEL</span>
                        <span className="text-zinc-500">=</span>
                        <span className="text-emerald-400">
                          {active === 'openrouter' ? 'anthropic/claude-3.5-sonnet' : 'llama3.1:70b'}
                        </span>
                        {'\n'}
                        <span className="text-amber-400">ANT_AUDIT</span>
                        <span className="text-zinc-500">=</span>
                        <span className="text-emerald-400">
                          {active === 'openrouter' ? 'blockchain' : 'local'}
                        </span>
                      </code>
                    </pre>
                  </div>

                  {/* Action row */}
                  <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
                    <button
                      onClick={() => onCopy('command', `export ${envSnippet}`)}
                      className="group inline-flex flex-1 items-center justify-center gap-2 rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-black transition-all hover:bg-amber-400 hover:shadow-[0_0_30px_-5px_rgba(245,158,11,0.5)]"
                    >
                      {copied === 'command' ? (
                        <>
                          <Check className="h-4 w-4" />
                          <span>Copied to clipboard</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-4 w-4" />
                          <span>Copy export command</span>
                        </>
                      )}
                    </button>
                    <a
                      href={current.docs}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center justify-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-5 py-3 text-sm font-medium text-white transition-all hover:bg-white/[0.08] hover:border-white/20"
                    >
                      <span>Open docs</span>
                      <span className="text-amber-400">↗</span>
                    </a>
                  </div>
                </div>

                {/* Corner glow */}
                <div className="absolute -top-1 -right-1 h-24 w-24 rounded-full bg-amber-500/10 blur-2xl pointer-events-none" />
              </motion.div>
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </section>
  )
}