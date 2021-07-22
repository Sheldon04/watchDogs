// pages/playback/playback.js
import Toast from '@vant/weapp/toast/toast';

Page({

  data: {
    date: '',
    show: false,
    src: '/image/jiankong.png',
    countries: ["摄像头1", "摄像头2", "摄像头3","摄像头4"],
    countryIndex: 0,
  },
  onDisplay() {
    this.setData({ show: true });
  },
  onClose() {
    this.setData({ show: false });
  },
  formatDate(date) {
    date = new Date(date);
    return `${date.getMonth() + 1}/${date.getDate()}`;
  },
  onConfirm(event) {
    this.setData({
      show: false,
      date: this.formatDate(event.detail),
    });
  },
  onChange(event) {
    const { picker, value, index } = event.detail;
    Toast(`当前值：${value}, 当前索引：${index}`);
  },  
  bindCountryCodeChange: function(e){
    console.log('picker country code 发生选择改变，携带值为', e.detail.value);

    this.setData({
        countryCodeIndex: e.detail.value
    })
},
bindCountryChange: function(e) {
    console.log('picker country 发生选择改变，携带值为', e.detail.value);

    this.setData({
        countryIndex: e.detail.value
    })
},
})
