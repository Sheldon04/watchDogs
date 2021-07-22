Page({
  data: {
    src: '/image/lineChart.png'
  },
  imageError: function(e) {
    console.log('image3发生error事件，携带值为', e.detail.errMsg)
  }
})