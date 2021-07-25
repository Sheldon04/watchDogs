<template>
  <div>
    <div>
      <el-container>
        <el-header>
          <img :src="imgSrc" width="100%" height="100%" alt="" />
        </el-header>
        <el-aside width="200px">
          <my-dropdown></my-dropdown>
          <my-sidenav-admin></my-sidenav-admin>
        </el-aside>
        <el-main class="main">
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
export default {
  name: 'Segmentation',
  components: {MySidenavAdmin, MyDropdown},
  data () {
    return {
      imgSrc: require('../../../assets/img3.jpg')
    }
  },
  methods: {
  }
}
</script>

<style scoped>
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
