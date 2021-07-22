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
          <el-calendar :first-day-of-week=7>
            <template
              slot="dateCell"
              slot-scope="{date, data}">
              <p>
                {{ data.day.split('-').slice(1).join('-') }}
<!--                v-if="data.day==='2021-07-22'||data.day=='2021-07-23'"-->
                <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[data.day.split('-')[2]] > 0 && month_invasion_data[data.day.split('-')[2]] <= 5" type="warning">
                  {{month_invasion_data[data.day.split('-')[2]]}}
                </el-tag>
                <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[data.day.split('-')[2]] > 5" type="danger">
                  {{month_invasion_data[data.day.split('-')[2]]}}
                </el-tag>
              </p>
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
  name: 'Monitor',
  data () {
    return {
      activeIndex: this.$route.path,
      imgSrc: require('../../assets/img3.jpg'),
      options: [],
      value: '',
      cur_month: 0,
      month_invasion_data: {
        '12': 2,
        '23': 5,
        '24': 7,
        '27': 9
      },
      testdata: 5
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
    }
  },
  mounted () {
    this.$nextTick(() => {
      // 点击前一个月
      let prevBtn = document.querySelector(
        '.el-calendar__button-group .el-button-group>button:nth-child(1)')
      prevBtn.addEventListener('click', () => {
        console.log(this.cur_month)
      })
    })
    this.$nextTick(() => {
      // 点击后一个月
      let prevBtn = document.querySelector(
        '.el-calendar__button-group .el-button-group>button:last-child')
      prevBtn.addEventListener('click', () => {
        console.log(this.cur_month)
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

</style>
