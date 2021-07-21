<template>
  <div>
    <div>
      <el-container>
        <el-header>
          <img :src="imgSrc" width="100%" height="100%" alt="" />
        </el-header>
        <el-aside width="200px">
          <el-dropdown class="user-menu" placement="bottom-start">
           <span class="el-dropdown-link">
             <el-avatar shape="square" :size="80" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
           </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>修改密码</el-dropdown-item>
              <el-dropdown-item>注销</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-menu
            :default-active=activeIndex
            class="el-menu"
            @select="handleSelect">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-view"></i>
                <span>入侵检测</span>
              </template>
              <el-menu-item index="/admin/monitor">
                <i class="el-icon-camera"></i>
                实时监控
              </el-menu-item>
              <el-menu-item index="/admin/traceback">
                <i class="el-icon-refresh"></i>
                入侵回放
              </el-menu-item>
              <el-menu-item index="/admin/attacklist">
                <i class="el-icon-document"></i>
                查看记录
              </el-menu-item>
              <el-menu-item index="/admin/attackinfo">
                <i class="el-icon-setting"></i>
                入侵统计
              </el-menu-item>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-user"></i>
                <span>用户管理</span>
              </template>
              <el-menu-item index="/admin/facereg">
                <i class="el-icon-camera"></i>
                人脸识别注册
              </el-menu-item>
              <el-menu-item index="/admin/usermanage">
                <i class="el-icon-document"></i>
                用户信息管理
              </el-menu-item>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-setting"></i>
                <span>监控设置</span>
              </template>
              <el-menu-item index="/admin/whitelist">
                <i class="el-icon-document-checked"></i>
                可信名单管理
              </el-menu-item>
              <el-menu-item index="/admin/segmentation">
                <i class="el-icon-crop"></i>
                监控区域划分
              </el-menu-item>
            </el-submenu>
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
      imgSrc: require('../../../assets/img3.jpg'),
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
