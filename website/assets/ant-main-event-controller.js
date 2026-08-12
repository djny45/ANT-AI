/*
 * ANT Web Main Event Controller
 * Connects user actions with sphere states.
 */

(function(){

function setState(state){
    if(window.ANTState && ANTState.set){
        ANTState.set(state);
    }

    if(window.ANTVisual){
        if(state === 'thinking' && ANTVisual.thinking) ANTVisual.thinking();
        if(state === 'response' && ANTVisual.response) ANTVisual.response();
        if(state === 'idle' && ANTVisual.idle) ANTVisual.idle();
    }
}

window.ANTMainController = {
    startListening(){
        setState('listening');
        if(window.ANTSphere) ANTSphere.activate();
    },

    startThinking(){
        setState('thinking');
    },

    finishResponse(){
        setState('response');
        setTimeout(()=>setState('idle'), 2500);
    }
};

document.addEventListener('DOMContentLoaded',()=>{
    const input=document.querySelector('#command-input');
    const button=document.querySelector('#send-btn');

    if(input){
        input.addEventListener('focus',()=>{
            ANTMainController.startListening();
        });
    }

    if(button){
        button.addEventListener('click',()=>{
            ANTMainController.startThinking();
        });
    }
});

})();
