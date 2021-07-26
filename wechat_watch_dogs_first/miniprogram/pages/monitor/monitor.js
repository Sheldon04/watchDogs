// pages/monitor/monitor.js
Page({
  data: {
    showIOSDialog: false,
    src: '/image/jiankong.png',
  },

  close: function() {
    this.setData({
        showIOSDialog: false,
    });
    },
    openIOS: function () {
      this.setData({
          showIOSDialog: true
      });
  },

})