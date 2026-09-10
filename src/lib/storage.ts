export const API_KEY_STORAGE = "ANT_API_KEY";

export function saveApiKey(key: string) {
  localStorage.setItem(API_KEY_STORAGE, key);
}

export function getApiKey() {
  return localStorage.getItem(API_KEY_STORAGE) || "";
}

export function clearApiKey() {
  localStorage.removeItem(API_KEY_STORAGE);
}
