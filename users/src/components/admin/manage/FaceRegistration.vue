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
          <el-form ref="form" :model="form" label-width="130px" class="form">
            <el-form-item label="注册人姓名">
              <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="手机">
              <el-input v-model="form.phone"></el-input>
            </el-form-item>
            <el-form-item label="准入区域">
              <el-select v-model="form.region" placeholder="请选择准入区域">
                <el-option label="区域一" value="shanghai"></el-option>
                <el-option label="区域二" value="beijing"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="准入时间">
              <el-col :span="11">
                <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
              </el-col>
              <el-col class="line" :span="2">-</el-col>
              <el-col :span="11">
                <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
              </el-col>
            </el-form-item>
            <el-form-item label="是否超级管理员">
              <el-switch v-model="form.is_superuser"></el-switch>
            </el-form-item>
            <el-form-item label="上传头像">
              <el-upload
                class="upload-demo"
                drag
                :limit="1"
                :action="uploadURL"
                :headers="headers"
                :on-remove="removeChange"
                :on-success="handleAvatarSuccess"
                :on-error="uploadError"
                :on-change="fileChange"
                :before-upload="beforeAvatarUpload"
                :auto-upload="false">
                <i class="el-icon-upload"></i>
                <img v-if="licenseImageUrl" :src="licenseImageUrl" width="" height="">
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              </el-upload>
              <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">立即注册</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FaceRegistration',
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  data () {
    return {
      activeIndex: this.$route.path,
      uploadURL: this.localAPI + 'admin/uploadface',
      imgSrc: require('../../../assets/img3.jpg'),
      licenseImageUrl: '',
      form: {
        username: '',
        phone: '',
        region: '',
        date1: '',
        date2: '',
        is_superuser: false,
        file: ''
      }
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    },
    handleAvatarSuccess (res, file) {
      let _this = this
      _this.licenseImageUrl = res.url
    },
    fileChange (file) {
      this.form.file = file
    },
    beforeAvatarUpload (file) {
      // eslint-disable-next-line no-redeclare
      const isJPG = file.type === 'image/jpeg'
      const isLt10M = file.size / 1024 / 1024 < 10
      if (this.form.phone === '') {
        this.$message.error('请先输入手机号')
        return false
      }
      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt10M) {
        this.$message.error('上传头像图片大小不能超过 10MB!')
      }
      return isJPG && isLt10M
    },
    // eslint-disable-next-line handle-callback-err
    uploadError (err, file, filelist) {
      this.$message.error('上传失败')
    },
    removeChange (file, fileList) {
      console.log('你要移除的文件为', file.name)
    },
    // eslint-disable-next-line handle-callback-err
    submitUpload () {
      let formData = new FormData()
      formData.append('phone', this.form.phone)
      formData.append('face', this.form.file)
      console.log(formData.get('face'))
      console.log(formData.get('phone'))
      axios.post(this.uploadURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('上传失败')
        // eslint-disable-next-line handle-callback-err
      }).catch(err => {
        this.$message.error('上传失败')
      })
    }
  }
}
</script>

<style scoped>
.submenu-title {
  font-size: 18px !important;
}
.form {
  top: 15%;
  left: 30%;
  position: absolute;
}

.user-menu {
  left: 50px;
  top: 5px;
}

</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9 !important;
  border-radius: 6px !important;
  cursor: pointer !important;
  position: relative !important;
  overflow: hidden !important;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF !important;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
