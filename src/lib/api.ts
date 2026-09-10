export async function sendToANT(message: string, apiKey: string) {
  const baseUrl = import.meta.env.VITE_ANT_API_URL;

  if (!baseUrl) {
    throw new Error('VITE_ANT_API_URL is not configured');
  }

  const response = await fetch(`${baseUrl}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error('ANT API request failed');
  }

  return response.json();
}
