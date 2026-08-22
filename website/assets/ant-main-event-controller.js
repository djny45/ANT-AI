/* ANT Web Main Event Controller */
(function(){

function setState(state){
    if(window.ANTState && ANTState.set) ANTState.set(state);
    if(window.ANTVisual){
        if(state === 'thinking' && ANTVisual.thinking) ANTVisual.thinking();
        if(state === 'response' && ANTVisual.response) ANTVisual.response();
        if(state === 'idle' && ANTVisual.idle) ANTVisual.idle();
        if(state === 'error' && ANTVisual.error) ANTVisual.error();
    }
}

function showResponse(text){
    const target = document.querySelector('#ant-response');
    if(target) target.textContent = text || '';
}

async function executeCommand(){
    const input = document.querySelector('#command-input');
    const button = document.querySelector('#send-btn');
    if(!input || !window.ANTConnector) return;

    const message = input.value.trim();
    if(!message) return;

    setState('thinking');
    if(button) button.disabled = true;
    showResponse('ANT is processing...');

    try {
        const data = await window.ANTConnector.send(message);
        showResponse(data.response || 'ANT completed the request without a response.');
        setState('response');
    } catch(error) {
        showResponse(error.message || 'ANT execution failed.');
        setState('error');
    } finally {
        if(button) button.disabled = false;
    }
}

window.ANTMainController = {
    startListening(){ setState('listening'); if(window.ANTSphere) ANTSphere.activate(); },
    startThinking(){ setState('thinking'); },
    finishResponse(){ setState('response'); setTimeout(()=>setState('idle'), 2500); },
    executeCommand
};

document.addEventListener('DOMContentLoaded',()=>{
    const input=document.querySelector('#command-input');
    const button=document.querySelector('#send-btn');
    if(input){
        input.addEventListener('focus',()=>ANTMainController.startListening());
        input.addEventListener('keydown',(event)=>{
            if(event.key === 'Enter') executeCommand();
        });
    }
    if(button) button.addEventListener('click', executeCommand);
});

})();
