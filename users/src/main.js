// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

import VideoPlayer from 'vue-video-player'
import 'videojs-flash'
// import 'videojs-contrib-hls'// 不确定是否需要了
require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
Vue.use(VideoPlayer)

Vue.use(ElementUI)
Vue.prototype.$http = axios

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

router.beforeEach((to, from, next) => {
  console.log('from: ', from.fullPath.split('/'))
  console.log('to: ', to.fullPath)
  if (from.fullPath === '/') {
    next(true)
  } else if (to.fullPath.split('/')[1] !== from.fullPath.split('/')[1]) {
    next(false)
  } else {
    next(true)
  }
})
