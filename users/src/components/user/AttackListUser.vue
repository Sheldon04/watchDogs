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
                  v-model="date"
                  align="right"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions">
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
                  placeholder="选择时间范围">
                </el-time-picker>
              </td>
            </tr>
          </table>
          <br>
          <br>
          <el-table
            :data="tableData"
            style="width: 100%"
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

<style scoped>
.main .el-table .warning-row {
  background-color: oldlace;
}

.main .el-table .success-row {
  background-color: #f0f9eb;
}

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

<script>
export default {
  name: 'Monitor',
  data () {
    return {
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      activeIndex: this.$route.path,
      imgSrc: require('../../assets/img3.jpg'),
      options: [],
      date: '',
      timespan: '',
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
  },
  methods: {
    tableRowClassName ({row, rowIndex}) {
      if (row.level === '严重') {
        return 'warning-row'
      } else if (row.level === '一般') {
        return 'success-row'
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
      console.log(row)
      console.log(row.class)
    }
  }
}
</script>
