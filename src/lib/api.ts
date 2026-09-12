import type { ModelApiProfile } from './storage'

export async function sendToANT(message: string, profile: ModelApiProfile) {
  const configuredUrl = import.meta.env.VITE_ANT_API_URL?.trim().replace(/\/+$/, '')
  const apiUrl = configuredUrl
    ? /\/chat$/.test(configuredUrl)
      ? configuredUrl
      : `${configuredUrl}/chat`
    : '/api/chat'

  let response: Response
  try {
    response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(profile.apiKey ? { Authorization: `Bearer ${profile.apiKey}` } : {}),
      },
      body: JSON.stringify({
        message,
        context: {
          model_provider: profile.provider,
          model: profile.model,
          model_base_url: profile.baseUrl,
        },
      }),
    })
  } catch {
    throw new Error('Unable to reach ANT API. Check the API deployment or VITE_ANT_API_URL.')
  }

  if (!response.ok) {
    let detail = ''
    try {
      const body = await response.json()
      detail = typeof body?.detail === 'string' ? body.detail : ''
    } catch {
      // Keep the status error when the server did not return JSON.
    }
    const suffix = detail ? `: ${detail}` : ''
    throw new Error(`ANT API request failed (${response.status})${suffix}`)
  }

  return response.json()
}
