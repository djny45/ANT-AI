export async function sendToANT(message: string, apiKey: string, model?: string) {
  // Accept either an API base URL (/api) or a full chat endpoint (/api/chat).
  // Default to the same-origin FastAPI route when no URL is configured.
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
        ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
      },
      body: JSON.stringify({
        message,
        context: model?.trim() ? { openrouter_model: model.trim() } : {},
      }),
    })
  } catch {
    throw new Error(
      'Unable to reach ANT API. Check the API deployment or VITE_ANT_API_URL.',
    )
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
