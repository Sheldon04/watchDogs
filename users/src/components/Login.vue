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
              <!--              <el-link href="https://element.eleme.io" target="_blank" style="width: 300px" >没有账号？注册</el-link>-->
              <el-button style="width: 300px" @click="register" type="text">没有账号？注册</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
    <div class="background">
      <img :src="imgSrc" width="100%" height="100%" alt="" />
    </div>
    <el-dialog title="注册新用户" :visible.sync="dialogRegisterVisible" width="600px">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username">
          <el-input type="text" v-model="ruleForm.username" suffix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="ruleForm.pass"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="ruleForm.checkPass"></el-input>
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input type="text" v-model="ruleForm.email" suffix-icon="el-icon-message" style="width: 350px"></el-input>
          <el-button @click="sendCode">验证码</el-button>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input type="text" v-model="ruleForm.code" style="width: 100px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitRegisterForm('ruleForm')">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  // 单页面中不支持前面的data:{}方式
  data () {
    let validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    let validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    // let validateEmail = (rule, value, callback) => {
    //   let regEmail = /^[A-Za-zd]+([-_.][A-Za-zd]+)*@([A-Za-zd]+[-.])+[A-Za-zd]{2,5}$/
    //   if (value === '') {
    //     callback(new Error('邮箱不能为空'))
    //   } else if (!regEmail.test(value)) {
    //     callback(new Error('邮箱格式不正确!'))
    //   } else {
    //     callback()
    //   }
    // }
    let validateCode = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('验证码不能为空'))
      } else {
        callback()
      }
    }
    const rolesOptions = ['用户', '管理员']
    // 相当于以前的function data(){},这是es5之前的写法，新版本可以省略掉function
    return {
      dialogRegisterVisible: false,
      user: {
        is_superuser: 0, // or 'admin'
        username: '',
        password: ''
        // 为了登录方便，可以直接在这里写好用户名和密码的值
      },
      imgSrc: require('../assets/img1.png'),
      checkedRoles: [],
      roles: rolesOptions,
      ruleForm: {
        username: '',
        email: '',
        pass: '',
        checkPass: '',
        code: '',
        validCode: ''
      },
      rules: {
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ],
        email: [
        ],
        code: [
          {validator: validateCode, trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    async submitForm () {
      if (this.checkedRoles.length !== 0 && this.checkedRoles[0] === '用户') {
        this.user.is_superuser = '0'
        console.log('????????????!!!!!!!!!!')
      } else {
        this.user.is_superuser = '1'
        console.log('----------------------')
      }
      axios.post('http://127.0.0.1:8000/api/user/login', this.user).then(response => {
        const {result, detail, errorInfo} = response.data
        if (result === true) {
          // 登录成功
          // 设置token
          localStorage.setItem('token', detail.token)
          // 跳转页面
          if (this.user.is_superuser === '1') {
            this.$router.push('/admin/monitor')
          } else {
            this.$router.push('/user/monitor')
          }
          localStorage.setItem('username', this.user.username)
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
          console.log('?????????failed???????')
        }
      })
    },
    submitRegisterForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid && this.ruleForm.validCode === this.ruleForm.code) {
          let formData = new FormData()
          formData.append('username', this.ruleForm.username) // 2021-7-10
          formData.append('password', this.ruleForm.pass) // 2021-7-10
          formData.append('phone_number', this.ruleForm.phone_number) // 2021-7-10
          formData.append('email', this.ruleForm.email) // 2021-7-10
          const auth = 'Token ' + localStorage.getItem('token')
          const header = {'Authorization': auth}
          axios.post('http://127.0.0.1:8000/api/adduser', formData, {'headers': header}).then(response => {
            console.log(response.data)
            if (response.data.result) {
              this.$message({
                message: '注册成功',
                type: 'success'
              })
              this.dialogRegisterVisible = false
            } else {
              this.$message.error(response.data.errorInfo)
            }
          })
        } else {
          if (this.ruleForm.validCode !== this.ruleForm.code) {
            this.$message({
              message: '验证码错误',
              type: 'warning'
            })
          } else {
            this.$message({
              message: '输入不合法，请检查您的输入',
              type: 'warning'
            })
          }
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    register () {
      console.log('tt')
      this.dialogRegisterVisible = true
    },
    sendCode () {
      let code = ''
      for (let i = 0; i < 6; i++) {
        code += Math.floor(Math.random() * 10)
      }
      this.ruleForm.validCode = code
      let formData = new FormData()
      formData.append('code', code)
      formData.append('email', this.ruleForm.email)
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/sendemail', formData, {'headers': header}).then(response => {
        console.log(response.data)
        if (response.data.result) {
          this.$message({
            message: '发送成功',
            type: 'success'
          })
        } else {
          this.$message.error(response.data.errorInfo)
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
