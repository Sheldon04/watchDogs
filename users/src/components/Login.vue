<template>
  <div>
    <!--flex弹性盒子模型，justify-content：主抽 -->
    <div style="display: flex;justify-content: center;margin-top: 150px" class="mycard">
      <el-card style="width: 380px">
        <div slot="header" class="clearfix">
          <span>登录</span>
        </div>
        <table>
          <tr>
            <td>用户名</td>
            <td>
              <el-input v-model="user.username" placeholder="请输入用户名"></el-input>
            </td>
          </tr>
          <br>
          <tr>
            <td>密码</td>
            <td>
              <el-input type="password" v-model="user.password" placeholder="请输入密码" @keydown.enter.native="submitForm"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <br>
          <tr>
            <td colspan="2">
              <el-checkbox-group
                v-model="checkedRoles"
                :min="0"
                :max="1">
                <el-checkbox v-for="role in roles" :label="role" :key="role">{{role}}</el-checkbox>
              </el-checkbox-group>
            </td>
          </tr>
          <tr>
            <!-- 占两行-->
            <td colspan="2">
              <!-- 点击事件的两种不同的写法v-on:click和 @click-->
              <!--<el-button style="width: 300px" type="primary" v-on:click="doLogin">登录</el-button>-->
              <el-button style="width: 300px" type="primary" @click="submitForm">登录</el-button>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <el-link href="https://element.eleme.io" target="_blank" style="width: 300px" >没有账号？注册</el-link>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
    <div class="background">
      <img :src="imgSrc" width="100%" height="100%" alt="" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  // 单页面中不支持前面的data:{}方式
  data () {
    const rolesOptions = ['用户', '管理员']
    // 相当于以前的function data(){},这是es5之前的写法，新版本可以省略掉function
    return {
      user: {
        issuperuser: '1', // or 'admin'
        username: '',
        password: ''
        // 为了登录方便，可以直接在这里写好用户名和密码的值
      },
      imgSrc: require('../assets/img1.png'),
      checkedRoles: [],
      roles: rolesOptions
    }
  },
  methods: {
    async submitForm () {
      axios.post('http://127.0.0.1:8000/api/user/login', this.user).then(response => {
        const {result, detail, errorInfo} = response.data
        if (result === true) {
          // 登录成功
          // 设置token
          localStorage.setItem('token', detail.token)
          // 跳转页面
          this.$router.push('/user/monitor')
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
          console.log('?????????failed???????')
        }
      })
    }
  }
}
</script>

<style scoped>
.background{
  width: 100%;
  height: 100%;  /**宽高100%是为了图片铺满屏幕 */
  left: 0;
  top: 0;
  z-index:-1;
  position: absolute;
}
.mycard{
  left: 70%;
  top: 10%;
  position: absolute;
}

</style>
