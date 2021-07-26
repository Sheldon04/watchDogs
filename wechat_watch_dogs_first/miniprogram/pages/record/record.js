Page({
  data: {
    model: false,
    date: '',
    calendarShow: false,
    startTimeShow:false,
    endTimeShow:false,
    minDate: new Date().setMonth(new Date().getMonth()-3),
    maxDate: new Date().getTime(),
    startTime: "00:01",
    endTime:"23:59",
    startMinTime:"00:01",
    startMaxTime:"23:59",
    endMinTime:"00:02",
    endMaxTime:"23:59",

    formData:new Date(),
    listData: []
  },

  calendarOnDisplay() {
    this.setData({ calendarShow: true });
  },
  calendarOnClose() {
    this.setData({ calendarShow: false });
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
  calendarOnConfirm(event) {
    this.setData({
      calendarShow: false,
      date: this.formatDate(event.detail),
    });
  },
  onStartConfirm(event) {
    this.setData({
      startTimeShow:false,
      startTime: event.detail,
    });
    console.log(this.data.startTime)
  },
  onEndConfirm(event){
    this.setData({
      endTimeShow:false,
      endTime: event.detail,
    });
    console.log(this.data.endTime)
  },
  showStartTimePopup(){
    this.setData({ startTimeShow: true });
  },
  showEndTimePopup(){
    this.setData({ endTimeShow: true });
  },
  startTimeOnClose(){
    this.setData({ startTimeShow: false });
  },
  endTimeOnClose(){
    this.setData({ endTimeShow: false });
  },

  onLoad(options) {
    this.seeAll()
  },

  search: function(e){		//与服务器进行交互
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
    let time_span = this.data.startTime + ':00,' + this.data.endTime + ':00'
    let auth = "Token " + getApp().globalData.token
    console.log(time_span)
    let qx_data = {
      "date": this.data.date,
      "time_span": time_span,
    }
    wx.request({
      url: 'http://127.0.0.1:8000/api/attacklistuser',	//获取服务器地址，此处为本地地址
      method: "POST",
      header:{
        "content-type": "application/x-www-form-urlencoded",		//使用POST方法要带上这个header
        "Authorization": auth
      },
      data: {		//向服务器发送的信息
        "date": this.data.date,
        "time_span": time_span,
      },
      success: res => {
        if (res.statusCode == 200) {
          this.setData({
            listData: res.data  //服务器返回的结果 
          })
        }
      },
    })
  },
  preventTouchMove() {},
  seeAll: function() {
    let auth = "Token " + getApp().globalData.token
    console.log(auth)
    wx.request( {
      url: "http://127.0.0.1:8000/api/attacklistuser/all",
      header:{
        "Authorization": auth
      },
      success: res => {
        console.log(res.data)
        this.setData({
          listData: res.data
        })
      }
    })
  }
});