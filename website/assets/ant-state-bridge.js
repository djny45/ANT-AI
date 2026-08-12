/*
 * ANT State Bridge
 * Connects AI states with sphere visual behavior.
 */

(function(){

  window.ANTBridge = {

    idle(){
      if(window.ANTSphere){
        ANTSphere.deactivate();
      }
    },

    listening(){
      if(window.ANTSphere){
        ANTSphere.activate();
      }
    },

    thinking(){
      if(window.ANTSphere){
        ANTSphere.activate();
      }
    },

    response(){
      if(window.ANTSphere){
        ANTSphere.activate();
      }

      setTimeout(()=>{
        if(window.ANTSphere){
          ANTSphere.deactivate();
        }
      },2500);
    }

  };

})();
