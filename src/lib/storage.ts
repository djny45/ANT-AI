export const API_KEY_STORAGE = "ANT_API_KEY";
export const MODEL_STORAGE = "ANT_MODEL";

export function saveApiKey(key: string) {
  localStorage.setItem(API_KEY_STORAGE, key);
}

export function getApiKey() {
  return localStorage.getItem(API_KEY_STORAGE) || "";
}

export function clearApiKey() {
  localStorage.removeItem(API_KEY_STORAGE);
}

export function saveModel(model: string) {
  localStorage.setItem(MODEL_STORAGE, model);
}

export function getModel(defaultModel = "nvidia/nemotron-3-ultra-550b-a55b:free") {
  return localStorage.getItem(MODEL_STORAGE) || defaultModel;
}

export function clearModel() {
  localStorage.removeItem(MODEL_STORAGE);
}
