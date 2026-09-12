import { useEffect, useState } from 'react'
import { saveApiKey, getApiKey, clearApiKey, saveModel, getModel } from '../lib/storage'
import { motion } from 'framer-motion'
import { Check, Cloud, Eye, EyeOff, KeyRound, Lock, ShieldCheck, Sparkles, Trash2 } from 'lucide-react'

const FREE_MODEL = 'nvidia/nemotron-3-ultra-550b-a55b:free'

export default function ApiKey() {
  const [show, setShow] = useState(false)
  const [value, setValue] = useState(() => getApiKey())
  const [model, setModel] = useState(() => getModel(FREE_MODEL))
  const [modelTier, setModelTier] = useState<'free' | 'paid'>(() =>
    getModel(FREE_MODEL).endsWith(':free') ? 'free' : 'paid',
  )
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (value.trim()) saveApiKey(value.trim())
    else clearApiKey()
  }, [value])

  useEffect(() => {
    if (model.trim()) saveModel(model.trim())
  }, [model])

  const hasKey = value.trim().length > 0
  const isValidShape = value.startsWith('sk-or-') || value.startsWith('sk-') || value.length >= 20
  const codeSnippet = `OPENROUTER_API_KEY=${value || '<your-key>'}\nOPENROUTER_MODEL=${model || '<openrouter-model-id>'}\nANT_MODEL_PROVIDER=openrouter\nANT_AUDIT=blockchain`
  const copySnippet = async () => { await navigator.clipboard.writeText(codeSnippet); setCopied(true); setTimeout(() => setCopied(false), 1600) }

  const chooseTier = (tier: 'free' | 'paid') => {
    setModelTier(tier)
    if (tier === 'free') setModel(FREE_MODEL)
    else if (model === FREE_MODEL) setModel('')
  }

  return <section id="api-key" className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5">
    <div className="mx-auto max-w-7xl px-6">
      <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-6">
        <div className="max-w-2xl"><div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400"><span className="h-px w-6 bg-amber-500" /> Configure</div><h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">Connect ANT AI.<br /><span className="text-zinc-500">You choose the model.</span></h2></div>
        <p className="text-zinc-400 max-w-md">ANT AI uses OpenRouter as its hosted runtime. Choose a free or paid OpenRouter model yourself; ANT will use exactly the model ID you select.</p>
      </motion.div>
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4 space-y-3"><div className="rounded-2xl border border-amber-500/40 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-5"><div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/20 text-amber-400"><Cloud className="h-4 w-4" /></div><div><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Hosted runtime</div><div className="mt-0.5 text-lg font-semibold text-white">OpenRouter</div></div></div></div><div className="rounded-2xl border border-white/5 bg-white/[0.015] p-5"><div className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-zinc-500"><ShieldCheck className="h-3.5 w-3.5 text-emerald-400" /> Security</div><ul className="mt-3 space-y-2 text-xs text-zinc-400"><li>• Key is stored locally in the browser.</li><li>• No local-model runtime is required.</li><li>• Your model choice is stored locally too.</li></ul></div></div>
        <div className="lg:col-span-8 relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-sm"><div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-5 py-3"><div className="flex items-center gap-3"><div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400"><KeyRound className="h-4 w-4" /></div><div><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Model runtime</div><div className="text-sm font-semibold text-white">OpenRouter model selection</div></div></div><a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer" className="hidden sm:inline-flex text-[10px] font-mono uppercase tracking-widest text-zinc-400 hover:text-amber-300">Get a key ↗</a></div>
          <div className="px-6 py-7 sm:px-8 sm:py-9 space-y-7"><div className="flex items-start gap-3 rounded-xl border border-white/5 bg-white/[0.015] p-4"><Sparkles className="h-4 w-4 mt-0.5 text-amber-400 shrink-0" /><p className="text-xs text-zinc-400 leading-relaxed">No automatic model routing: the selected model is sent with every ANT request. For paid models, enter the exact OpenRouter model ID you want to use.</p></div>
            <div><label className="flex items-center justify-between mb-2"><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Model tier</span><span className="text-[10px] font-mono text-zinc-600">USER SELECTED</span></label><div className="grid grid-cols-2 gap-2"><button type="button" onClick={() => chooseTier('free')} className={`rounded-xl border px-4 py-3 text-left transition-all ${modelTier === 'free' ? 'border-emerald-500/50 bg-emerald-500/10' : 'border-white/10 bg-white/[0.02] hover:bg-white/5'}`}><div className="text-sm font-semibold text-white">Free</div><div className="mt-1 text-[10px] font-mono text-zinc-500">No paid model routing</div></button><button type="button" onClick={() => chooseTier('paid')} className={`rounded-xl border px-4 py-3 text-left transition-all ${modelTier === 'paid' ? 'border-amber-500/50 bg-amber-500/10' : 'border-white/10 bg-white/[0.02] hover:bg-white/5'}`}><div className="text-sm font-semibold text-white">Paid</div><div className="mt-1 text-[10px] font-mono text-zinc-500">Use your chosen model ID</div></button></div></div>
            <div><label className="flex items-center justify-between mb-2"><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">OpenRouter model ID</span><span className="text-[10px] font-mono text-zinc-600">EXACT MODEL</span></label><input value={model} onChange={e => { setModel(e.target.value); setModelTier(e.target.value.endsWith(':free') ? 'free' : 'paid') }} placeholder={modelTier === 'free' ? FREE_MODEL : 'provider/model-name'} spellCheck={false} autoComplete="off" className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none focus:ring-2 focus:ring-amber-500/20" /><div className="mt-2 text-[10px] text-zinc-600">Browse available model IDs on OpenRouter and paste the exact ID here.</div></div>
            <div><label className="flex items-center justify-between mb-2"><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">API Key</span><span className="text-[10px] font-mono text-zinc-600">OPENROUTER_API_KEY</span></label><div className="relative group"><Lock className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500 group-focus-within:text-amber-400" /><input type={show ? 'text' : 'password'} value={value} onChange={e => setValue(e.target.value)} placeholder="sk-or-v1-••••••••••••••••" spellCheck={false} autoComplete="off" className="w-full rounded-xl border border-white/10 bg-black/40 py-3.5 pl-11 pr-24 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none focus:ring-2 focus:ring-amber-500/20" /><div className="absolute inset-y-0 right-2 flex items-center gap-1">{value && <button type="button" onClick={() => setShow(s => !s)} className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-white" aria-label={show ? 'Hide key' : 'Show key'}>{show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</button>}{value && <button type="button" onClick={() => setValue('')} className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-rose-300" aria-label="Clear key"><Trash2 className="h-4 w-4" /></button>}</div></div><div className="mt-3 flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest">{hasKey && isValidShape ? <><Check className="h-3.5 w-3.5 text-emerald-400" /><span className="text-emerald-400">valid format</span></> : <span className="text-zinc-500">awaiting key</span>}</div></div>
            <div><div className="flex items-center justify-between mb-2"><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Generated <span className="text-zinc-300">.env</span> snippet</span><button onClick={copySnippet} className="inline-flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-mono uppercase tracking-widest text-zinc-300 hover:bg-white/10">{copied ? 'Copied' : 'Copy'}</button></div><pre className="overflow-x-auto rounded-xl border border-white/5 bg-black/50 p-4 text-xs leading-6 text-zinc-400"><code>{codeSnippet}</code></pre></div>
          </div></div>
      </motion.div>
    </div>
  </section>
}
