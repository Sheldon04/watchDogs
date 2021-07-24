<template>
  <div>
    <div>
      <el-container>
        <el-header>
          <img :src="imgSrc" width="100%" height="100%" alt="" />
        </el-header>
        <el-aside>
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
          <el-calendar @pick="test" v-loading="loading" :first-day-of-week=7>
            <template
              slot="dateCell"
              slot-scope="{date, data}">
              <div @click="handle_click(data.day.split('-'))">
                <p class="date_cell">{{ data.day.split('-').slice(1).join('-') }}</p>
                <el-popover
                  placement="right"
                  width="200"
                  trigger="click">
                  <el-table v-loading="dia_loading" :data="detail_invasion_data">
                    <el-table-column width="100" property="time" label="时间"></el-table-column>
                    <el-table-column label="操作">
                      <template slot-scope="scope">
                        <el-button
                          size="mini" type="text"
                          @click="handleSee(scope.$index, scope.row, data.day)">查看</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <div slot="reference" class="date_cell">
                    <el-badge v-if="parseInt(data.day.split('-')[1]) === cur_month" :value="month_invasion_data[parseInt(data.day.split('-')[2])]" class="item">
                      <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[parseInt(data.day.split('-')[2])] > 0 && month_invasion_data[parseInt(data.day.split('-')[2])] <= 5" type="warning">
                        有入侵
                      </el-tag>
                      <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[parseInt(data.day.split('-')[2])] > 5" type="danger">
                        有入侵
                      </el-tag>
                    </el-badge>
                  </div>
                </el-popover>
              </div>
            </template>
          </el-calendar>
        </el-main>
      </el-container>
      <el-dialog width="720" height="360" :visible.sync="dialogMediaVisible">
        <img ref="img" style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" :src="video_url" type="video/mp4" width="720" height="360">
      </el-dialog>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import axios from 'axios'

export default {
  name: 'Monitor',
  data () {
    return {
      loading: true,
      dia_loading: false,
      video_url: '',
      dialogMediaVisible: false,
      activeIndex: this.$route.path,
      imgSrc: require('../../assets/img3.jpg'),
      options: [],
      value: '',
      cur_month: -1,
      cur_year: 0,
      cur_day: 0,
      month_invasion_data: {},
      detail_invasion_data: []
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    },
    set_cur_month () {
      let nowDate = new Date()
      this.cur_month = nowDate.getMonth() + 1
      this.cur_year = nowDate.getFullYear()
    },
    handle_click (date) {
      if (parseInt(date[1]) !== this.cur_month) {
        this.cur_year = parseInt(date[0])
        this.cur_month = parseInt(date[1])
      }
      if (this.month_invasion_data[parseInt(date[2])] > 0) {
        this.dia_loading = true
        console.log(date[0] + '-' + date[1] + '-' + date[2])
        let formData = new FormData()
        formData.append('date', date[0] + '-' + date[1] + '-' + date[2]) // 2021-7-10
        const auth = 'Token ' + localStorage.getItem('token')
        const header = {'Authorization': auth}
        axios.post('http://127.0.0.1:8000/api/attacklistuser/invasiontime', formData, {'headers': header}).then(response => {
          // console.log(response.data)
          this.detail_invasion_data = response.data
          this.dia_loading = false
        })
      }
    },
    handleSee (index, row, day) {
      // dialogTableVisible = true
      this.dialogMediaVisible = true
      this.video_url = 'http://127.0.0.1:8000/api/invationrecord/getvideo' + '?date=' +
        day + '&time=' + row.time
      // console.log(index, row.time)
      console.log(this.video_url)
    }
  },
  mounted () {
    this.$nextTick(() => {
      // 点击上个月
      let prevBtn1 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(1)')
      prevBtn1.addEventListener('click', () => {
        if (this.cur_month - 1 === 0) {
          this.cur_year -= 1
        }
        this.cur_month = (this.cur_month + 11) % 12
      })
      // 点击今天
      let prevBtn2 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(2)')
      prevBtn2.addEventListener('click', () => {
      })
      // 点击下个月
      let prevBtn3 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(3)')
      prevBtn3.addEventListener('click', () => {
        if (this.cur_month + 1 === 13) {
          this.cur_year += 1
        }
        this.cur_month = this.cur_month % 12 + 1
      })
    })
    this.set_cur_month()
  },
  watch: {
    // eslint-disable-next-line camelcase
    cur_month (new_month, old_month) {
      this.loading = true
      let formData = new FormData()
      formData.append('month', this.cur_year + '-' + this.cur_month) // 2021-7-10
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/invationrecord/getmonth', formData, {'headers': header}).then(response => {
        console.log(response.data)
        this.month_invasion_data = response.data
        this.loading = false
      })
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

.budge{
  width: 10px;
  height: 10px;
  border-radius: 5px;
  margin: 5px auto;
}

.red{
  background-color: #c9413f;
}
.green{
  background-color: #25b591;
}
.orange{
  background-color: #ee915c;
}

.date_cell {
  display: inline-block;
}

.user-menu {
  left: 50px;
  top: 5px;
}

</style>
