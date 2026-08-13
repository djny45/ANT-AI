/*
 * ANT Release Loader Optimizer
 * Lightweight startup layer for ANT website.
 * Keeps InfinityFree compatibility.
 */
(function(){
  window.ANTLoader = {
    ready:false,
    start:function(){
      this.ready=true;
      document.documentElement.setAttribute('data-ant-ready','true');
    }
  };

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded',()=>ANTLoader.start());
  } else {
    ANTLoader.start();
  }
})();
