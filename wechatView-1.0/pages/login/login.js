// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    is_superuser: 0,
    userName:'',
    userPwd:'',
    src: '/image/watchDogs.png',
  },

  //获取用户输入的用户名
  userNameInput:function(e)
  {
    this.setData({
      userName: e.detail.value
    })
  },
  //获取用户输入的密码
  passWdInput:function(e)
  {
    this.setData({
      userPwd: e.detail.value
    })
  },

  jumpPage: function (e) {
    wx.navigateTo({
      url: '/pages/registerFirst/registerFirst',
    })
  },
  jumpRegisterPhone: function (e) {
    wx.navigateTo({
      url: '/pages/loginPhone/loginPhone',
    })
  },
  login:function(e){
    wx.switchTab({
      url: '/pages/monitor/monitor',
    })
  },
  give: function(e){		//与服务器进行交互
    console.log("执行give服务器这里了！！"),
    wx.request({
      url: 'http://127.0.0.1:8000/wx/wx_login/',	//获取服务器地址，此处为本地地址
      method: "POST",
      header:{
        "content-type": "application/x-www-form-urlencoded"		//使用POST方法要带上这个header
      },
      data: {		//向服务器发送的信息
        is_superuser:this.data.is_superuser,
        userName:this.data.userName,
        password:this.data.userPwd,
      },
      success: res => {
        console.log(this.mname)
        if (res.statusCode == 200) {
          console.log(res)
          this.setData({
            result: res.data	//服务器返回的结果 
          })    
        }    
      },
    })
  }

})