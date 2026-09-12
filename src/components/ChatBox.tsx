import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Bot, User, Sparkles, Cpu, Trash2 } from 'lucide-react'
import { sendToANT } from '../lib/api'
import { getActiveProfile, type ModelApiProfile } from '../lib/storage'

type Role = 'user' | 'ant' | 'system'

interface Message { id: string; role: Role; text: string; meta?: string }

const seedMessages: Message[] = [
  { id: 'm0', role: 'system', text: 'Queen initialized · 4 nano-capabilities online', meta: 'system' },
  { id: 'm1', role: 'ant', text: 'Colony online. Configure a model API and state a goal.', meta: 'Queen · t=0ms' },
]

const suggestions = ['Refactor auth to OAuth2', 'Audit the last 5 commits', 'Diagnose failing test suite', 'Suggest perf optimizations']

function MessageBubble({ m }: { m: Message }) {
  const isUser = m.role === 'user'
  const isSystem = m.role === 'system'
  if (isSystem) return <div className="flex justify-center"><div className="rounded-full border border-white/5 bg-white/[0.02] px-3 py-1 font-mono text-[10px] uppercase tracking-widest text-zinc-500">{m.text}</div></div>
  return <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }} className={`flex gap-2.5 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}><div className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${isUser ? 'bg-white/10 text-zinc-200' : 'bg-amber-500/15 text-amber-400'}`}>{isUser ? <User className="h-3.5 w-3.5" /> : <Bot className="h-3.5 w-3.5" />}</div><div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}><div className={`rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${isUser ? 'bg-white/[0.06] text-white border border-white/10 rounded-tr-sm' : 'bg-gradient-to-br from-amber-500/10 to-orange-500/5 text-zinc-100 border border-amber-500/20 rounded-tl-sm'}`}>{m.text}</div>{m.meta && <div className="font-mono text-[9px] uppercase tracking-widest text-zinc-600 px-1">{m.meta}</div>}</div></motion.div>
}

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>(seedMessages)
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)
  const [profile, setProfile] = useState<ModelApiProfile>(() => getActiveProfile())
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' }) }, [messages, thinking])
  useEffect(() => {
    const sync = () => setProfile(getActiveProfile())
    window.addEventListener('storage', sync)
    window.addEventListener('focus', sync)
    return () => { window.removeEventListener('storage', sync); window.removeEventListener('focus', sync) }
  }, [])

  const send = async (text?: string) => {
    const value = (text ?? input).trim()
    if (!value || thinking) return
    const selected = getActiveProfile()
    if (!selected.apiKey.trim() || !selected.model.trim()) {
      setMessages((m) => [...m, { id: `e-${Date.now()}`, role: 'system', text: 'Configure a model, endpoint, and API key in the API Configuration panel first.', meta: 'configuration' }])
      return
    }
    setMessages((m) => [...m, { id: `u-${Date.now()}`, role: 'user', text: value }])
    setInput('')
    setThinking(true)
    try {
      const result = await sendToANT(value, selected)
      const responseText = result?.response ?? result?.message ?? result?.text ?? 'ANT returned no response.'
      setMessages((m) => [...m, { id: `a-${Date.now()}`, role: 'ant', text: String(responseText), meta: `ANT API · ${selected.provider} · ${selected.model}` }])
    } catch (error) {
      setMessages((m) => [...m, { id: `e-${Date.now()}`, role: 'system', text: error instanceof Error ? error.message : 'ANT API request failed.', meta: 'error' }])
    } finally { setThinking(false); setProfile(getActiveProfile()) }
  }

  const clear = () => { setMessages(seedMessages); setInput('') }

  return <section id="chat" className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5"><div className="mx-auto max-w-7xl px-6">
    <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-6"><div className="max-w-2xl"><div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400"><span className="h-px w-6 bg-amber-500" /> Talk to the Queen</div><h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">Try the swarm.<br /><span className="text-zinc-500">Right here, right now.</span></h2></div><p className="text-zinc-400 max-w-md">Choose any configured model API in the panel, then send a goal. ANT never silently switches models.</p></motion.div>
    <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.1 }} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div className="lg:col-span-3 space-y-2"><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 px-1">Nano capabilities</div>{[{ label: 'Development', state: 'ready' }, { label: 'Repair', state: 'ready' }, { label: 'Analysis', state: 'ready' }, { label: 'Research', state: 'standby' }, { label: 'Audit', state: 'ready' }].map((c, i) => <motion.div key={c.label} initial={{ opacity: 0, x: -8 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 + i * 0.05 }} className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-white/[0.015] px-3 py-2.5"><div className="flex items-center gap-2"><Cpu className="h-3.5 w-3.5 text-zinc-500" /><span className="text-xs text-zinc-200">{c.label}</span></div><div className="flex items-center gap-1.5"><span className={`h-1.5 w-1.5 rounded-full ${c.state === 'ready' ? 'bg-emerald-400 pulse-dot' : 'bg-zinc-600'}`} /><span className="font-mono text-[9px] uppercase tracking-widest text-zinc-500">{c.state}</span></div></motion.div>)}<div className="mt-4 rounded-2xl border border-amber-500/20 bg-amber-500/[0.03] p-4"><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Selected API</div><div className="mt-2 truncate font-mono text-xs text-amber-300" title={`${profile.provider} · ${profile.model}`}>{profile.provider || 'custom'} · {profile.model || 'not configured'}</div></div><div className="rounded-2xl border border-white/5 bg-white/[0.015] p-4"><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Session</div><div className="mt-2 grid grid-cols-2 gap-2 text-xs"><div><div className="text-zinc-500">Messages</div><div className="font-mono text-white">{messages.length}</div></div><div><div className="text-zinc-500">Latency</div><div className="font-mono text-white">API</div></div></div></div></div>
      <div className="lg:col-span-9"><div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-sm gradient-border"><div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-5 py-3"><div className="flex items-center gap-3"><div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400"><Bot className="h-4 w-4" /><span className="absolute -bottom-0.5 -right-0.5 h-2 w-2 rounded-full bg-emerald-400 ring-2 ring-[#0a0a0a]" /></div><div><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">colony session</div><div className="text-sm font-semibold text-white">Queen · live</div></div></div><button onClick={clear} className="flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-mono uppercase tracking-widest text-zinc-400 transition-all hover:bg-white/10 hover:text-white"><Trash2 className="h-3 w-3" /><span>reset</span></button></div><div ref={scrollRef} className="h-[360px] overflow-y-auto px-5 py-5 sm:px-7 sm:py-7 space-y-3"><AnimatePresence initial={false}>{messages.map((m) => <MessageBubble key={m.id} m={m} />)}</AnimatePresence>{thinking && <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="flex gap-2.5"><div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400"><Bot className="h-3.5 w-3.5" /></div><div className="flex items-center gap-1.5 rounded-2xl rounded-tl-sm border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-orange-500/5 px-4 py-3"><span className="h-1.5 w-1.5 rounded-full bg-amber-400 pulse-dot" /><span className="h-1.5 w-1.5 rounded-full bg-amber-400 pulse-dot" style={{ animationDelay: '0.2s' }} /><span className="h-1.5 w-1.5 rounded-full bg-amber-400 pulse-dot" style={{ animationDelay: '0.4s' }} /></div></motion.div>}</div><div className="border-t border-white/5 bg-white/[0.01] px-5 py-3 sm:px-7"><div className="flex items-center gap-2 mb-2"><Sparkles className="h-3 w-3 text-amber-400" /><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Try a goal</span></div><div className="flex flex-wrap gap-2">{suggestions.map((s) => <button key={s} onClick={() => void send(s)} disabled={thinking} className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs text-zinc-300 transition-all hover:border-amber-500/40 hover:bg-amber-500/10 hover:text-amber-200 disabled:opacity-50 disabled:cursor-not-allowed">{s}</button>)}</div></div><form onSubmit={(e) => { e.preventDefault(); void send() }} className="border-t border-white/5 bg-white/[0.02] px-5 py-3 sm:px-7 sm:py-4"><div className="relative"><input value={input} onChange={(e) => setInput(e.target.value)} placeholder="State a goal for the swarm…" disabled={thinking} className="w-full rounded-xl border border-white/10 bg-black/40 py-3.5 pl-4 pr-14 text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none focus:ring-2 focus:ring-amber-500/20 transition-all disabled:opacity-50" /><button type="submit" disabled={!input.trim() || thinking} aria-label="Send" className="absolute right-2 top-1/2 -translate-y-1/2 flex h-9 w-9 items-center justify-center rounded-lg bg-amber-500 text-black transition-all hover:bg-amber-400 disabled:opacity-40 disabled:cursor-not-allowed"><Send className="h-3.5 w-3.5" /></button></div></form></div></div>
    </motion.div>
  </div></section>
}
