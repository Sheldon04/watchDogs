<template>
 <div>
   <div>
     <el-container>
       <el-header>
         <img :src="imgSrc" width="100%" height="100%" alt="" />
       </el-header>
       <el-aside>
         <el-menu
           default-active="/user/monitor"
           class="el-menu-vertical-demo">
           <el-menu-item index="/user/monitor">
             <i class="el-icon-camera"></i>
             <span slot="title">实时监控</span>
           </el-menu-item>
           <el-menu-item index="/user/traceback">
             <i class="el-icon-refresh"></i>
             <span slot="title">入侵回放</span>
           </el-menu-item>
           <el-menu-item index="/user/attacklist">
             <i class="el-icon-document"></i>
             <span slot="title">查看记录</span>
           </el-menu-item>
           <el-menu-item index="/user/attackinfo">
             <i class="el-icon-setting"></i>
             <span slot="title">入侵统计</span>
           </el-menu-item>
         </el-menu>
       </el-aside>
       <el-main>
         <video-player class="video-player vjs-custom-skin"
                        ref="videoPlayer"
                        :playsinline="true"
                        :options="playerOptions"
         ></video-player>
       </el-main>
     </el-container>
   </div>
 </div>
</template>

<script>
export default {
  name: 'Monitor',
  data () {
    return {
      activeIndex: this.$route.path,
      imgSrc: require('../assets/img3.jpg'),
      // 视频播放
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
        autoplay: false, // 如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 导致视频一结束就重新开始。
        preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        techOrder: ['html5'],
        html5: { hls: { withCredentials: false } },
        sources: [{ // 流配置，数组形式，会根据兼容顺序自动切换
          type: 'flv',
          src: 'http://admin:123456@100.58.198.227:8081/live.flv'
        }],
        // width: document.documentElement.clientWidth,
        notSupportedMessage: '此视频暂无法播放，请稍后再试',
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true
        }
      }
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    }
  }
}
</script>

<style scoped>
.el-menu {
  width: 200px;
  height: 800px;
}
.submenu-title {
  font-size: 18px !important;
}
</style>
