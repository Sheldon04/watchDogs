<template>
 <div>
   <div>
     <el-container>
       <el-header>
         <img :src="imgSrc" width="100%" height="100%" alt="" />
       </el-header>
       <el-aside>
         <el-menu
           :default-active=activeIndex
           class="el-menu-vertical-demo"
           @select="handleSelect">
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
       <el-main class="main">
         <el-button @click="dosomething()" type="primary">主要按钮</el-button>
         <img ref="img" style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://127.0.0.1:8000/api/video" type="video/mp4" width="1080" height="720">
       </el-main>
     </el-container>
   </div>
 </div>
</template>

<script>
// import axios from 'axios'

import axios from 'axios'

export default {
  name: 'Monitor',
  mounted () {
    let token = sessionStorage.getItem('token')
    let img = this.$refs.img
    let request = new XMLHttpRequest()
    request.responseType = 'blob'
    request.open('get', this.authSrc, true)
    request.setRequestHeader('Token ', token)
    request.onreadystatechange = e => {
      if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
        img.src = URL.createObjectURL(request.response)
        img.onload = () => {
          URL.revokeObjectURL(img.src)
        }
      }
    }
    request.send(null)
  },
  data () {
    return {
      activeIndex: this.$route.path,
      imgSrc: require('../../assets/img3.jpg')
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    },
    dosomething () {
      // console.log('test')
      const url = 'http://127.0.0.1:8000/api/tokentest'
      // // 从localStorage获取到登录时保持的token
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.get(url, {'headers': header}).then(response => {
        console.log(response.data.result)
      })
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

.main {
  left: 200px;
  top: 80px;
  position: absolute;
}

</style>
