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
          <table>
            <tr>
              <td>按日期选择</td>
              <td>
                <el-date-picker
                  v-model="value2"
                  align="right"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions">
                </el-date-picker>
              </td>
              <td>最近的侵入记录</td>
              <td>
                <el-select v-model="value" placeholder="请选择">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </td>
            </tr>
          </table>
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
      options: [],
      value: ''
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
