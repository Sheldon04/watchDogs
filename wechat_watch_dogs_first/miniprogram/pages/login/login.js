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
    request:'',
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
  give: function(e){		//与服务器进行交互
    console.log("执行give服务器这里了！！"),
    wx.request({
      url: 'http://127.0.0.1:8000/api/user/login',	//获取服务器地址，此处为本地地址
      method: "POST",
      header:{
        "content-type": "application/x-www-form-urlencoded"		//使用POST方法要带上这个header
      },
      data: {		//向服务器发送的信息
        username:this.data.userName,
        password:this.data.userPwd,
        is_superuser:this.data.is_superuser,
      },
      success: res => {
        console.log(res)
        if (res.statusCode == 200) {
          console.log(res)
          this.setData({
            result: res.data	//服务器返回的结果 
          })
        }
        if(res.data.result){
          getApp().globalData.token = res.data.detail.token
          wx.navigateTo({
            url: '/pages/loginSuccess/loginSuccess',
          })
        }else{
          wx.navigateTo({
            url: '/pages/loginFail/loginFail',
          })
        }
      },
    })
  }

})