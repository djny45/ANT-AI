/*
 * Legacy compatibility bridge.
 *
 * The current website uses #command-input, #send-btn and the ANTMainController.
 * This file used to bind handlers to obsolete IDs (#antInput, #send, #antSphere)
 * and dereference null elements during page load. Keep the legacy file harmless
 * while delegating to the canonical controller when it is available.
 */
(function () {
  const input = document.getElementById('command-input');
  const send = document.getElementById('send-btn');
  const sphere = document.getElementById('ant-sphere');

  function setState(state) {
    if (sphere) sphere.dataset.state = state;
    if (window.ANTState && typeof window.ANTState.set === 'function') {
      window.ANTState.set(state);
    }
  }

  if (!input || !send) return;

  input.addEventListener('input', () => setState('thinking'));

  if (!window.ANTMainController) {
    send.addEventListener('click', () => {
      setState('response');
      setTimeout(() => setState('idle'), 1500);
    });
  }
})();
