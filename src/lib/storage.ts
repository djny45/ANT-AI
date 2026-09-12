export type ModelApiProfile = {
  id: string
  name: string
  provider: string
  model: string
  apiKey: string
  baseUrl: string
}

export const PROFILES_STORAGE = "ANT_MODEL_API_PROFILES"
export const ACTIVE_PROFILE_STORAGE = "ANT_ACTIVE_MODEL_API_PROFILE"

const DEFAULT_PROFILE: ModelApiProfile = {
  id: "custom",
  name: "Custom model API",
  provider: "custom",
  model: "",
  apiKey: "",
  baseUrl: "",
}

export function getProfiles(): ModelApiProfile[] {
  try {
    const raw = localStorage.getItem(PROFILES_STORAGE)
    const parsed = raw ? JSON.parse(raw) : []
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function saveProfiles(profiles: ModelApiProfile[]) {
  localStorage.setItem(PROFILES_STORAGE, JSON.stringify(profiles))
}

export function getActiveProfileId() {
  return localStorage.getItem(ACTIVE_PROFILE_STORAGE) || "custom"
}

export function setActiveProfileId(id: string) {
  localStorage.setItem(ACTIVE_PROFILE_STORAGE, id)
}

export function getActiveProfile(): ModelApiProfile {
  const profiles = getProfiles()
  const activeId = getActiveProfileId()
  return profiles.find((profile) => profile.id === activeId) || profiles[0] || DEFAULT_PROFILE
}

export function upsertProfile(profile: ModelApiProfile) {
  const profiles = getProfiles().filter((item) => item.id !== profile.id)
  saveProfiles([...profiles, profile])
  setActiveProfileId(profile.id)
}

export function removeProfile(id: string) {
  const profiles = getProfiles().filter((profile) => profile.id !== id)
  saveProfiles(profiles)
  if (getActiveProfileId() === id) {
    setActiveProfileId(profiles[0]?.id || "custom")
  }
}

// Backward-compatible helpers for callers that only need the active key/model.
export function saveApiKey(key: string) {
  const profile = getActiveProfile()
  upsertProfile({ ...profile, apiKey: key })
}

export function getApiKey() {
  return getActiveProfile().apiKey
}

export function clearApiKey() {
  const profile = getActiveProfile()
  upsertProfile({ ...profile, apiKey: "" })
}

export function saveModel(model: string) {
  const profile = getActiveProfile()
  upsertProfile({ ...profile, model })
}

export function getModel(defaultModel = "") {
  return getActiveProfile().model || defaultModel
}

export function clearModel() {
  const profile = getActiveProfile()
  upsertProfile({ ...profile, model: "" })
}
