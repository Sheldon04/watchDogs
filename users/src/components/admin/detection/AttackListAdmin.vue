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
          <table class="main-table">
            <tr>
              <td>按日期选择</td>
              <td>
                <el-date-picker
                  v-model="date"
                  align="right"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions"
                  format="yyyy 年 MM 月 dd 日"
                  value-format="yyyy-MM-dd">
                </el-date-picker>
              </td>
              <td>按时间范围选择</td>
              <td>
                <el-time-picker
                  is-range
                  v-model="timespan"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  placeholder="选择时间范围"
                  value-format="HH:mm:ss">
                </el-time-picker>
              </td>
              <td>
                <el-button @click="search">查找</el-button>
              </td>
            </tr>
          </table>
          <br>
          <br>
          <el-table
            :data="tableData"
            style="width: 1000px"
            :row-class-name="tableRowClassName">
            <el-table-column
              prop="date"
              label="时间"
              width="200">
            </el-table-column>
            <el-table-column
              prop="level"
              label="报警级别"
              width="150">
            </el-table-column>
            <el-table-column
              prop="camera"
              label="摄像头"
              width="150">
            </el-table-column>
            <el-table-column
              prop="area"
              label="报警区域"
              width="150">
            </el-table-column>
            <el-table-column
              prop="number"
              label="入侵数量"
              width="150">
            </el-table-column>
            <el-table-column
              fixed="right"
              label="操作"
              width="100">
              <template slot-scope="scope">
                <el-button @click="handleClick(scope.row)" type="text" size="small">查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
                         :current-page="currentPage"
                         :page-sizes="[10,20,50,100]"
                         :page-size="pageSize"
                         layout="total, sizes, prev, pager, next, jumper"
                         :total="tableData.length">
          </el-pagination>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<style>
.main .el-table .warning-row {
  background-color: oldlace;
}

.main .el-table .common-row {
  background-color: #f0f9eb;
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

<script>
import axios from 'axios'
export default {
  name: 'AttackListAdmin',
  mounted () {
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get('http://127.0.0.1:8000/api/attacklistuser/all', {'headers': header}).then(response => {
      this.tableData = response.data
    })
  },
  methods: {
    async search () {
      // let keywords = []
      // keywords.push(this.date)
      // if (this.timespan.length !== 0) {
      //   keywords = keywords.concat(this.timespan)
      // }
      let formData = new FormData()
      formData.append('date', this.date) // 2021-7-10
      formData.append('time_span', this.timespan) // 8:00:15,9:00:00
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/attacklistuser', formData, {'headers': header}).then(response => {
        this.tableData = response.data
      })
      console.log(formData.get('date'))
      console.log(formData.get('time_span'))
    },
    tableRowClassName ({row, rowIndex}) {
      if (row.level === '严重') {
        return 'warning-row'
      } else if (row.level === '中等') {
        return 'common-row'
      }
      return 'other'
    },
    handleSizeChange (val) {
      console.log(`每页 ${val} 条`)
      this.currentPage = 1
      this.pageSize = val
    },
    handleCurrentChange (val) {
      console.log(`当前页: ${val}`)
      this.currentPage = val
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    },
    handleClick (row) {
      console.log(this.timespan)
      console.log(this.date)
    }
  },
  data () {
    return {
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      activeIndex: this.$route.path,
      imgSrc: require('../../../assets/img3.jpg'),
      options: [],
      date: '2021-7-21',
      timespan: [],
      tableData: [{
        date: '2016-05-02',
        level: '严重',
        camera: '1',
        area: '仓库',
        number: '1'
      }, {
        date: '2016-05-02',
        level: '严重',
        camera: '1',
        area: '仓库',
        number: '1'
      }, {
        date: '2016-05-02',
        level: '严重',
        camera: '1',
        area: '仓库',
        number: '1'
      }, {
        date: '2016-05-02',
        level: '严重',
        camera: '1',
        area: '仓库',
        number: '1'
      }],
      pickerOptions: {
        disabledDate (time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: '今天',
          onClick (picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: '昨天',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: '一周前',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      }
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

.el-table.warning-row {
  background: oldlace;
}

.el-table.success-row {
  background: #f0f9eb;
}

.user-menu {
  left: 50px;
  top: 5px;
}

</style>
=======
>>>>>>> Stashed changes
