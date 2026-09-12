import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Eye, EyeOff, KeyRound, Lock, Plus, Save, Trash2, Cpu } from 'lucide-react'
import {
  type ModelApiProfile,
  getActiveProfile,
  getActiveProfileId,
  getProfiles,
  removeProfile,
  setActiveProfileId,
  upsertProfile,
} from '../lib/storage'

const PROVIDERS = [
  ['nova-core', 'NOVA Core (native)', ''],
  ['openai', 'OpenAI', 'https://api.openai.com/v1'],
  ['anthropic', 'Anthropic', 'https://api.anthropic.com/v1'],
  ['google', 'Google Gemini', 'https://generativelanguage.googleapis.com/v1beta'],
  ['groq', 'Groq', 'https://api.groq.com/openai/v1'],
  ['mistral', 'Mistral', 'https://api.mistral.ai/v1'],
  ['deepseek', 'DeepSeek', 'https://api.deepseek.com/v1'],
  ['together', 'Together AI', 'https://api.together.xyz/v1'],
  ['fireworks', 'Fireworks AI', 'https://api.fireworks.ai/inference/v1'],
  ['xai', 'xAI', 'https://api.x.ai/v1'],
  ['perplexity', 'Perplexity', 'https://api.perplexity.ai'],
  ['cerebras', 'Cerebras', 'https://api.cerebras.ai/v1'],
  ['custom', 'Custom / OpenAI-compatible', ''],
] as const

function blankProfile(id = `profile-${Date.now()}`): ModelApiProfile {
  return { id, name: 'New model API', provider: 'nova-core', model: 'nova-core', apiKey: '', baseUrl: '' }
}

export default function ApiKey() {
  const [profiles, setProfiles] = useState<ModelApiProfile[]>(() => getProfiles())
  const [activeId, setActiveId] = useState(() => getActiveProfileId())
  const [draft, setDraft] = useState<ModelApiProfile>(() => getActiveProfile())
  const [showKey, setShowKey] = useState(false)
  const [saved, setSaved] = useState(false)
  const nativeNova = draft.provider === 'nova-core'

  const providerName = useMemo(
    () => PROVIDERS.find(([id]) => id === draft.provider)?.[1] || draft.provider || 'Custom',
    [draft.provider],
  )

  useEffect(() => {
    const sync = () => {
      setProfiles(getProfiles())
      setActiveId(getActiveProfileId())
      setDraft(getActiveProfile())
    }
    window.addEventListener('storage', sync)
    window.addEventListener('focus', sync)
    return () => {
      window.removeEventListener('storage', sync)
      window.removeEventListener('focus', sync)
    }
  }, [])

  const selectProfile = (id: string) => {
    setActiveProfileId(id)
    setActiveId(id)
    setDraft(getProfiles().find((profile) => profile.id === id) || blankProfile(id))
    setSaved(false)
    setShowKey(false)
  }

  const chooseProvider = (provider: string) => {
    const preset = PROVIDERS.find(([id]) => id === provider)
    setDraft((current) => ({ ...current, provider, baseUrl: preset?.[2] || '', model: provider === 'nova-core' ? 'nova-core' : current.model }))
  }

  const save = () => {
    if (!draft.model.trim() || (!nativeNova && !draft.apiKey.trim())) return
    const normalized = { ...draft, name: draft.name.trim() || providerName, model: draft.model.trim(), apiKey: nativeNova ? '' : draft.apiKey.trim(), baseUrl: draft.baseUrl.trim() }
    upsertProfile(normalized)
    setProfiles(getProfiles())
    setActiveId(normalized.id)
    setDraft(normalized)
    setSaved(true)
    setTimeout(() => setSaved(false), 1600)
  }

  const addProfile = () => {
    const next = blankProfile()
    upsertProfile(next)
    setProfiles(getProfiles())
    setActiveId(next.id)
    setDraft(next)
    setShowKey(false)
    setSaved(false)
  }

  const deleteProfile = () => {
    removeProfile(draft.id)
    const nextProfiles = getProfiles()
    setProfiles(nextProfiles)
    const next = nextProfiles[0] || blankProfile('nova-core')
    setActiveProfileId(next.id)
    setActiveId(next.id)
    setDraft(next)
  }

  const hasKey = draft.apiKey.trim().length > 0

  return (
    <section id="api-key" className="relative w-full bg-[#0a0a0a] py-28 sm:py-36 border-t border-white/5">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <div className="max-w-2xl">
            <div className="mb-3 inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-amber-400"><span className="h-px w-6 bg-amber-500" /> API Configuration</div>
            <h2 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl">Choose your intelligence.<br /><span className="text-zinc-500">NOVA native or external API.</span></h2>
          </div>
          <p className="text-zinc-400 max-w-md">NOVA Core is the native runtime and requires no external API key. External providers remain optional profiles you can add and switch to explicitly.</p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-4 space-y-3">
            <div className="rounded-2xl border border-amber-500/30 bg-amber-500/[0.04] p-5">
              <div className="flex items-center justify-between mb-4"><div><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Saved intelligence profiles</div><div className="mt-1 text-lg font-semibold text-white">{profiles.length} configured</div></div><button type="button" onClick={addProfile} className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-zinc-300 hover:bg-white/10 hover:text-white" aria-label="Add model API"><Plus className="h-4 w-4" /></button></div>
              <div className="space-y-2">
                {profiles.map((profile) => <button type="button" key={profile.id} onClick={() => selectProfile(profile.id)} className={`w-full rounded-xl border px-3 py-3 text-left transition-all ${activeId === profile.id ? 'border-amber-500/40 bg-amber-500/10' : 'border-white/5 bg-white/[0.015] hover:bg-white/5'}`}><div className="flex items-center gap-2 truncate text-sm font-medium text-white">{profile.provider === 'nova-core' && <Cpu className="h-3.5 w-3.5 text-amber-400" />}{profile.name || profile.provider}</div><div className="mt-1 truncate text-[10px] font-mono uppercase tracking-widest text-zinc-500">{profile.provider} · {profile.model || 'model not set'}</div></button>)}
                {profiles.length === 0 && <div className="rounded-xl border border-dashed border-white/10 p-4 text-xs text-zinc-500">No profiles yet. NOVA Core is available by default; add an external profile when needed.</div>}
              </div>
            </div>
            <div className="rounded-2xl border border-white/5 bg-white/[0.015] p-5"><div className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-zinc-500"><Lock className="h-3.5 w-3.5 text-emerald-400" /> Credential handling</div><ul className="mt-3 space-y-2 text-xs text-zinc-400"><li>• NOVA Core native mode does not require an external key.</li><li>• External keys stay in browser local storage until you send a request.</li><li>• External keys are forwarded only for the current request.</li><li>• Provider and endpoint are selected explicitly; no hidden routing.</li></ul></div>
          </div>

          <div className="lg:col-span-8 relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-sm">
            <div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] px-5 py-3"><div className="flex items-center gap-3"><div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400"><KeyRound className="h-4 w-4" /></div><div><div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Active intelligence</div><div className="text-sm font-semibold text-white">{providerName}</div></div></div><button type="button" onClick={deleteProfile} className="inline-flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-mono uppercase tracking-widest text-zinc-400 hover:text-rose-300"><Trash2 className="h-3 w-3" /> Remove</button></div>
            <div className="px-6 py-7 sm:px-8 sm:py-9 space-y-6">
              {nativeNova && <div className="rounded-2xl border border-amber-500/20 bg-amber-500/[0.04] p-4 text-sm text-zinc-300"><div className="flex items-center gap-2 font-medium text-amber-300"><Cpu className="h-4 w-4" /> Native NOVA Core</div><div className="mt-2 text-xs leading-relaxed text-zinc-500">ANT will send this request to the configured NOVA-Core runtime. No OpenAI, Gemini, Anthropic, or other external API key is required.</div></div>}
              <div><label className="mb-2 block text-[10px] font-mono uppercase tracking-widest text-zinc-500">Profile name</label><input value={draft.name} onChange={(e) => setDraft({ ...draft, name: e.target.value })} placeholder="My production model" className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none" /></div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4"><div><label className="mb-2 block text-[10px] font-mono uppercase tracking-widest text-zinc-500">Provider</label><select value={draft.provider} onChange={(e) => chooseProvider(e.target.value)} className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 text-sm text-white focus:border-amber-500/50 focus:outline-none">{PROVIDERS.map(([id, name]) => <option key={id} value={id}>{name}</option>)}</select></div><div><label className="mb-2 block text-[10px] font-mono uppercase tracking-widest text-zinc-500">Model ID</label><input value={draft.model} onChange={(e) => setDraft({ ...draft, model: e.target.value })} placeholder={nativeNova ? 'nova-core' : 'provider/model-name'} spellCheck={false} autoComplete="off" className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none" /></div></div>
              {!nativeNova && <div><label className="mb-2 block text-[10px] font-mono uppercase tracking-widest text-zinc-500">API endpoint</label><input value={draft.baseUrl} onChange={(e) => setDraft({ ...draft, baseUrl: e.target.value })} placeholder="https://api.example.com/v1" spellCheck={false} autoComplete="off" className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none" /><div className="mt-2 text-[10px] text-zinc-600">For Custom, enter the provider's API base URL. OpenAI-compatible endpoints use <span className="font-mono">/chat/completions</span>.</div></div>}
              {!nativeNova && <div><label className="mb-2 flex items-center justify-between"><span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">API key</span><span className="text-[10px] font-mono text-zinc-600">USER SUPPLIED</span></label><div className="relative"><input type={showKey ? 'text' : 'password'} value={draft.apiKey} onChange={(e) => setDraft({ ...draft, apiKey: e.target.value })} placeholder="Paste your provider API key" spellCheck={false} autoComplete="off" className="w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3.5 pr-24 font-mono text-sm text-white placeholder:text-zinc-600 focus:border-amber-500/50 focus:outline-none" /><div className="absolute inset-y-0 right-2 flex items-center gap-1">{hasKey && <button type="button" onClick={() => setShowKey((value) => !value)} className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-white" aria-label={showKey ? 'Hide key' : 'Show key'}>{showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</button>}<button type="button" onClick={() => setDraft({ ...draft, apiKey: '' })} className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-400 hover:bg-white/5 hover:text-rose-300" aria-label="Clear key"><Trash2 className="h-4 w-4" /></button></div></div><div className="mt-3 flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest">{hasKey ? <><Check className="h-3.5 w-3.5 text-emerald-400" /><span className="text-emerald-400">key present</span></> : <span className="text-zinc-500">key required</span>}</div></div>}
              <button type="button" onClick={save} disabled={!draft.model.trim() || (!nativeNova && !draft.apiKey.trim())} className="inline-flex items-center gap-2 rounded-xl bg-amber-500 px-5 py-3 text-sm font-semibold text-black transition-all hover:bg-amber-400 disabled:cursor-not-allowed disabled:opacity-40"><Save className="h-4 w-4" /> {saved ? 'Saved' : nativeNova ? 'Use NOVA Core' : 'Save & use this API'}</button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
