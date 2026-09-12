export async function sendToANT(message: string, apiKey: string) {
  // Default to the same-origin FastAPI route so the frontend does not fail
  // merely because VITE_ANT_API_URL is absent. Set it only for a separate API.
  const configuredBaseUrl = import.meta.env.VITE_ANT_API_URL?.trim()
  const baseUrl = (configuredBaseUrl || '/api').replace(/\/$/, '')

  let response: Response
  try {
    response = await fetch(`${baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
      },
      body: JSON.stringify({ message }),
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
