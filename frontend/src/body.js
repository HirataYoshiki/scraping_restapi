window.onload = function (){
      var app = new Vue({
            delimiters:['[[',']]'],
            el:"#app",
            data:{
                  message:"vue_app",
                  text:"this is text"
            }
      })

      var header = new Vue({
            delimiters:['[[',']]'],
            el:"#app2",
            data:{
                  message:"login",
                  text:"login text"
            }
      });
}