// pages/playback/playback.js
import Toast from '@vant/weapp/toast/toast';

Page({
  data: {
    date: '',
    show: false,
    src: '/image/jiankong.png',
    camera_id: ["摄像头1", "摄像头2", "摄像头3","摄像头4"],
    camera_id_index: 0,
    minDate: new Date().setMonth(new Date().getMonth()-3),
    maxDate: new Date().getTime(),
    invasion_time: []
  },
  onDisplay() {
    this.setData({ show: true });
  },
  onClose() {
    this.setData({ show: false });
  },
  formatDate(date) {
    date = new Date(date);
    let month = date.getMonth()
    if (month < 9) {
      month += 1
      month = '0' + month
      return `${date.getFullYear()}-`+month+`-${date.getDate()}`;
    }
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
  },
  onConfirm(event) {
    this.setData({
      show: false,
      date: this.formatDate(event.detail)
    });
  },
  onChange(event) {
    const { picker, value, index } = event.detail;
    Toast(`当前值：${value}, 当前索引：${index}`);
  },  
  bindCountryChange: function(e){
    console.log('picker country code 发生选择改变，携带值为', e.detail.value);
    this.setData({
      camera_id_index: e.detail.value
    })
  },
  onButtonConfirm: function(e) {
    let auth = "Token " + getApp().globalData.token
    console.log(auth)
    wx.request({
      url: 'http://127.0.0.1:8000/api/attacklistuser/invasiontime',	//获取服务器地址，此处为本地地址
      method: "POST",
      header:{
        "content-type": "application/x-www-form-urlencoded",		//使用POST方法要带上这个header
        "Authorization": auth
      },
      data: {		//向服务器发送的信息
        date:this.data.date
      },
      success: res => {
        console.log(res.data)
        if (res.data.length === 0) {
          wx.showModal({
            title: "提示", // 提示的标题
            content: "当天无入侵信息", // 提示的内容
            showCancel: false, // 是否显示取消按钮，默认true
            confirmText: "确定", // 确认按钮的文字，最多4个字符
            confirmColor: "#576B95", // 确认按钮的文字颜色，必须是 16 进制格式的颜色字符串
          })
          return
        }
        this.setData({
          invasion_time: res.data
        })
      },
    })
  },
  playback: function(item) {
    // console.log(item.currentTarget.dataset.time)
    if (this.data.date === '') {
      wx.showModal({
        title: "提示", // 提示的标题
        content: "请选择日期", // 提示的内容
        showCancel: false, // 是否显示取消按钮，默认true
        confirmText: "确定", // 确认按钮的文字，最多4个字符
        confirmColor: "#576B95", // 确认按钮的文字颜色，必须是 16 进制格式的颜色字符串
      })
      return
    }
    wx.navigateTo({
      url: '/pages/playback_detail/playback_detail?date=' + this.data.date + '&&time=' + item.currentTarget.dataset.time.time,
    })
  }
})