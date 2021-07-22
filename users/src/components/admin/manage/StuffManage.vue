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
              <el-dropdown-item>个人信息</el-dropdown-item>
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
          <el-table
            :data="tableData.filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
            stripe
            style="width: 1200px"
            :default-sort = "{prop: 'id', order: 'descending'}">
            <el-table-column
              prop="id"
              label="ID"
              width="100"
              type="index"
              sortable>
            </el-table-column>
            <el-table-column
              prop="username"
              label="姓名"
              width="200"
              sortable>
            </el-table-column>
            <el-table-column
              prop="email"
              label="邮箱"
              width="200">
            </el-table-column>
            <el-table-column
              prop="is_superuser"
              label="是否为管理员"
              width="200"
              :filters="[{ text: '是', value: '是' }, { text: '否', value: '否' }]"
              :filter-method="filterHandler">
            </el-table-column>
            <el-table-column
              prop="last_login"
              label="最近一次登录"
              width="200"
              sortable>
            </el-table-column>
            <el-table-column
              align="center"
              width="300">
              <template slot="header" slot-scope="scope">
                <div>
                  <div class="search">
                    <el-input
                      v-model="search"
                      size="mini"
                      prefix-icon="el-icon-search"
                      placeholder="输入关键字搜索"/>
                  </div>
                  <div class="search"><el-button icon="el-icon-search" size="mini" circle></el-button></div>
                </div>
              </template>
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Monitor',
  mounted () {
    const url = 'http://127.0.0.1:8000/api/user/getall'
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get(url, {'headers': header}).then(response => {
      console.log(response.data.result)
      this.tableData = response.data
    })
  },
  data () {
    return {
      search: '',
      activeIndex: this.$route.path,
      imgSrc: require('../../../assets/img3.jpg'),
      tableData: []
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    },
    filterHandler (value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    handleEdit (index, row) {
      console.log(index, row)
    },
    handleDelete (index, row) {
      console.log(index, row)
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

.search {
  display: inline-block;
}

</style>
