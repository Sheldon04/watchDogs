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
          <canvas id="canvas" width="1280" height="720"></canvas>
          <img class="cam1" width="1280" height="720" id="cam1" :src="camSrc1">
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
  mounted () {
    // eslint-disable-next-line no-unused-vars,no-undef
    let canvas = new fabric.Canvas('canvas')
    let imgElement = document.getElementById('cam1')
    // eslint-disable-next-line no-undef
    let imgInstance = new fabric.Image(imgElement, {
      left: 0,
      top: 0,
      angle: 0,
      opacity: 0.85
    })
    imgInstance.set('selectable', false)
    canvas.add(imgInstance)
  },
  components: {MySidenavAdmin, MyDropdown},
  data () {
    return {
      context: {},
      imgSrc: require('../../../assets/img3.jpg'),
      camSrc1: require('../../../assets/camera1.jpg')
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.main {
  left: 200px;
  top: 80px;
  position: absolute;
}

canvas {
  border: 1px dashed black;
}

.cam1 {
  display: none;
}
</style>
