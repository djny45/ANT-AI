(function(){
  const SPHERE_SELECTOR = '#ant-sphere';
  const INPUT_SELECTOR = '#command-input';
  const SEND_BTN_SELECTOR = '#send-btn';

  const style=document.createElement('style');
  style.textContent=`
  ${SPHERE_SELECTOR}{transition:filter .6s ease;will-change:transform,filter;}
  ${SPHERE_SELECTOR}.ant-active{
    animation:ant-bounce 3.2s ease-in-out infinite,ant-glow 2.4s ease-in-out infinite;
  }
  @keyframes ant-bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
  @keyframes ant-glow{0%,100%{filter:drop-shadow(0 0 12px rgba(255,140,0,.35)) brightness(1)}50%{filter:drop-shadow(0 0 46px rgba(255,140,0,.85)) brightness(1.25)}}
  `;
  document.head.appendChild(style);

  function sphere(){return document.querySelector(SPHERE_SELECTOR)};

  window.ANTSphere={
    activate:function(){const el=sphere();if(el)el.classList.add('ant-active')},
    deactivate:function(){const el=sphere();if(el)el.classList.remove('ant-active')}
  };

  document.addEventListener('DOMContentLoaded',()=>{
    const input=document.querySelector(INPUT_SELECTOR);
    const button=document.querySelector(SEND_BTN_SELECTOR);
    const trigger=()=>{
      ANTSphere.activate();
      clearTimeout(window.antTimer);
      window.antTimer=setTimeout(()=>ANTSphere.deactivate(),4000);
    };
    if(button)button.onclick=trigger;
    if(input)input.addEventListener('keydown',e=>{if(e.key==='Enter')trigger()});
  });
})();
