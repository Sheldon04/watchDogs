// pages/registerFirst/registerFirst.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  jumpPage:function(){
    wx.navigateTo({
      url: '/pages/register/register',
    })
  },
  sendEmail(){
    wx.cloud.callFunction({
      name:"sendEmail",
      success(res){
        console.log("发送成功",res)
      },
      fail(res){
        console.log("发送失败",res)
      }
    })
  },

})