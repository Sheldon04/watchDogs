// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    is_superuser: 0,
    userName:'',
    userPwd:"",
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
  },
})
