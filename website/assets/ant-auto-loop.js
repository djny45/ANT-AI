/*
 * ANT Web Auto Interaction Loop
 * Connects user activity with ANT sphere states.
 */
(function(){
  const setState = (state)=>{
    if(window.ANTState && typeof window.ANTState.set === 'function'){
      window.ANTState.set(state);
    }

    if(window.ANTBridge && typeof window.ANTBridge[state] === 'function'){
      window.ANTBridge[state]();
    }

    if(window.ANTSphere){
      if(state === 'idle' && ANTSphere.deactivate){
        ANTSphere.deactivate();
      }
      if(state !== 'idle' && ANTSphere.activate){
        ANTSphere.activate();
      }
    }
  };

  window.ANTAutoLoop = {
    start(){
      setState('thinking');
    },
    listening(){
      setState('listening');
    },
    finish(){
      setState('response');
      setTimeout(()=>setState('idle'),2000);
    }
  };

  document.addEventListener('DOMContentLoaded',()=>{
    const input=document.querySelector('#command-input');
    if(input){
      input.addEventListener('focus',()=>setState('listening'));
    }
  });
})();
