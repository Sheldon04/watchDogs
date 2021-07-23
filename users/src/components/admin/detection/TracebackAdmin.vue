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
          <el-calendar :first-day-of-week=7 @pick="pick" @date-change="dateChange">
            <template
              slot="dateCell"
              slot-scope="{date, data}">
              <div v-if="data.isSelected">{{handle_click(data.day.split('-'))}}</div>
              <p class="date_cell">{{ data.day.split('-').slice(1).join('-') }}</p>
              <el-popover
                placement="right"
                width="200"
                trigger="click">
                <el-table :data="detail_invasion_data">
                  <el-table-column width="100" property="time" label="时间"></el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button size="mini" type="text" @click="handleSee(scope.$index, scope.row)">查看</el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <div slot="reference" class="date_cell">
                  <el-badge v-if="parseInt(data.day.split('-')[1]) === cur_month" :value="month_invasion_data[data.day.split('-')[2]]" class="item">
                    <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[data.day.split('-')[2]] > 0 && month_invasion_data[data.day.split('-')[2]] <= 5" type="warning">
                      有入侵
                    </el-tag>
                    <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[data.day.split('-')[2]] > 5" type="danger">
                      有入侵
                    </el-tag>
                  </el-badge>
                </div>
              </el-popover>
              <!--标记-->
              <!--              <div v-if="data.day==='2021-07-22'||data.day=='2021-07-23'" class="red budge">5</div>-->
              <!--              <div v-if="data.day==='2021-07-12'||data.day=='2021-07-13'" class="green budge"></div>-->
              <!--              <div v-if="data.day==='2021-07-02'||data.day=='2021-07-03'" class="orange budge"></div>-->
            </template>
          </el-calendar>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TracebackAdmin',
  data () {
    return {
      activeIndex: this.$route.path,
      imgSrc: require('../../../assets/img3.jpg'),
      options: [],
      value: '',
      cur_month: 9,
      month_invasion_data: {
        '12': 2,
        '23': 5,
        '24': 7,
        '27': 9
      },
      detail_invasion_data: [{
        'time': '10:12:56'
      },
      {
        'time': '10:12:56'
      },
      {
        'time': '10:12:56'
      }]
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
      console.log(nowDate)
    },
    handle_click (date) {
      if (parseInt(date[1]) !== this.cur_month) {
        this.cur_month = parseInt(date[1])
        console.log('update month: ', this.cur_month)
        this.month_invasion_data = {
          '08': 1,
          '09': 10,
          '24': 2
        }
        //  TODO 更新当前月入侵记录
      }
      if (this.month_invasion_data[date[2]] > 0) {
        console.log('show invasion')
        //  TODO 显示当天入侵详细记录
      }
    },
    handleSee (index, row) {
      console.log(index, ' ', row.time)
    }
  },
  mounted () {
    this.$nextTick(() => {
      // 点击上个月
      let prevBtn1 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(1)')
      prevBtn1.addEventListener('click', () => {
        console.log('上个月')
        this.cur_month = (this.cur_month + 11) % 12
      })
      // 点击今天
      let prevBtn2 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(2)')
      prevBtn2.addEventListener('click', () => {
        console.log('今天')
      })
      // 点击下个月
      let prevBtn3 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(3)')
      prevBtn3.addEventListener('click', () => {
        console.log('下个月')
        this.cur_month = this.cur_month % 12 + 1
      })
    })
    this.set_cur_month()
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

</style>
