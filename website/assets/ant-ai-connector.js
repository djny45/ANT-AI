// ANT AI Connector — browser to FastAPI execution bridge.

async function sendANTMessage(message) {
  if (!message) return null;

  if (window.ANTState) ANTState.set(ANTState.states.THINKING);

  const apiBase = window.ANT_API_URL || '';
  const response = await fetch(`${apiBase}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      conversation_id: 'web-session'
    })
  });

  const data = await response.json();
  if (!response.ok) {
    if (window.ANTState) ANTState.set(ANTState.states.ERROR);
    throw new Error(data.detail || 'ANT execution failed');
  }

  if (window.ANTState) ANTState.set(ANTState.states.RESPONSE);
  return data;
}

window.ANTConnector = {
  send: sendANTMessage
};
