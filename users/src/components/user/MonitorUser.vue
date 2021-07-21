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
         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://127.0.0.1:8000/api/video" type="video/mp4" width="1080" height="720">
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
      imgSrc: require('../../assets/img3.jpg')
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

.main {
  left: 200px;
  top: 80px;
  position: absolute;
}

</style>
