<template>
 <div>
   <div>
     <el-container>
       <el-header>
         <img :src="imgSrc" width="100%" height="100%" alt="" />
       </el-header>
       <el-aside>
         <el-menu
           default-active="2"
           class="el-menu-vertical-demo"
           @open="handleOpen"
           @close="handleClose"
           @select="handleSelect">
           <el-submenu index="1">
             <template slot="title">
               <i class="el-icon-view"></i>
               <span>入侵检测</span>
             </template>
             <el-menu-item index="/admin/monitor">
               <i class="el-icon-camera"></i>
               <span slot="title">实时监控</span>
             </el-menu-item>
             <el-menu-item index="/admin/traceback">
               <i class="el-icon-refresh"></i>
               <span slot="title">入侵回放</span>
             </el-menu-item>
             <el-menu-item index="/admin/attacklist">
               <i class="el-icon-document"></i>
               <span slot="title">查看记录</span>
             </el-menu-item>
             <el-menu-item index="/admin/attackinfo">
               <i class="el-icon-setting"></i>
               <span slot="title">入侵统计</span>
             </el-menu-item>
           </el-submenu>
           <el-submenu index="2">
             <template slot="title">
               <i class="el-icon-user"></i>
               <span>用户管理</span>
             </template>
             <el-menu-item index="/admin/monitor">
               <i class="el-icon-camera"></i>
               <span slot="title">人脸识别注册</span>
             </el-menu-item>
             <el-menu-item index="/admin/monitor">
               <i class="el-icon-document"></i>
               <span slot="title">用户信息管理</span>
             </el-menu-item>
           </el-submenu>
           <el-submenu index="3">
             <template slot="title">
               <i class="el-icon-setting"></i>
               <span>监控设置</span>
             </template>
             <el-menu-item index="/admin/monitor">
               <i class="el-icon-document-checked"></i>
               <span slot="title">可信名单管理</span>
             </el-menu-item>
             <el-menu-item index="/admin/monitor">
               <i class="el-icon-crop"></i>
               <span slot="title">监控区域划分</span>
             </el-menu-item>
           </el-submenu>
         </el-menu>
       </el-aside>
       <el-main class="main">
         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://100.58.198.227:8081/video" width="1080" height="720">
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
