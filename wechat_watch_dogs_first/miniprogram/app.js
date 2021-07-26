//app.js
App({
  onLaunch: function () {

    wx.cloud.init({
      traceUser: true,
      env:"cloud1-4glvb4tta48f9654",
    })

    this.globalData = {
      token: '43a81b051e4249568b275659ca7a9de13002b183'
    }
  }
})
