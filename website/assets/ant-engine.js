const sphere=document.getElementById('antSphere');
const input=document.getElementById('antInput');
const send=document.getElementById('send');
function setState(state){sphere.dataset.state=state;}
input.addEventListener('focus',()=>setState('listening'));
input.addEventListener('input',()=>setState('thinking'));
send.addEventListener('click',()=>{setState('response');setTimeout(()=>setState('idle'),1500);});
