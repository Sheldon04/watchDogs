<template>
 <div>
   <div>
     <el-container>
       <el-header>
         <img :src="imgSrc" width="100%" height="100%" alt="" />
       </el-header>
       <el-aside>
         <my-dropdown></my-dropdown>
         <my-sidnav-user></my-sidnav-user>
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
import MyDropdown from '../public/Dropdown'
import MySidnavUser from '../public/SideNavUser'
export default {
  name: 'Monitor',
  components: {MySidnavUser, MyDropdown},
  mounted () {
    let token = sessionStorage.getItem('token')
    let img = this.$refs.img
    let request = new XMLHttpRequest()
    request.responseType = 'blob'
    request.open('get', this.src, true)
    request.setRequestHeader('Authorization', 'Token ' + token)
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
      imgSrc: require('../../assets/img3.jpg')
    }
  },
  methods: {
    dosomething () {
      let formData = new FormData()
      formData.append('date', '2021-07-10')
      formData.append('time_span', '08:00:00,18:00:00')
      // console.log('test')
      // const url = 'http://127.0.0.1:8000/api/tokentest'
      // // // 从localStorage获取到登录时保持的token
      // const auth = 'Token ' + localStorage.getItem('token')
      // const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/user/attacklistuser', formData).then(response => {
        this.tableData = response.data
      })
      // axios.post('http://127.0.0.1:8000/api/user/attacklistuser', testdata).then(response => {
      //   console.log(response.data.result)
      // })
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

.user-menu {
  left: 50px;
  top: 5px;
}

</style>
