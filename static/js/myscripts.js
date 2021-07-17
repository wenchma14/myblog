window.onload=function(){
    var send_code=document.getElementById('send_code'),
      times=60,
      timer=null;
    send_code.onclick=function(){
     // 计时开始
     var that = this;
      this.disabled=true;
      timer = setInterval(function(){
        times --;
        that.value = times + "秒后重试";
        if(times <= 0){
          that.disabled =false;
          that.value = "发送验证码";
          clearInterval(timer);
          times = 60;
        }
        //console.log(times);
      },1000);
    }
}