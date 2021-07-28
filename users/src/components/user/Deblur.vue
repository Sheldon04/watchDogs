<template>
  <div>
    <div>
      <el-container>
        <el-header class="header">
          <banner></banner>
        </el-header>
        <el-aside width="200px" class="side">
          <my-dropdown></my-dropdown>
          <my-sidnav-user></my-sidnav-user>
        </el-aside>
        <el-main class="main">
          <el-tabs type="border-card" class="border-card1">
            <el-tab-pane>
              <span slot="label"><i class="el-icon-date"></i>提交工单</span>
              <el-upload
                class="avatar-uploader"
                :limit="1"
                :headers="headers"
                :on-remove="removeChange"
                :on-error="uploadError"
                :on-change="fileChange"
                :before-upload="beforeAvatarUpload"
                :auto-upload="false"
                align="center">
                <img v-if="licenseImageUrl" :src="licenseImageUrl" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                <div class="el-upload__tip" slot="tip">在此处上传需要处理的图片</div>
              </el-upload>
              <br>
              <el-input
                class="textarea"
                type="textarea"
                :rows="10"
                placeholder="在此处输入描述信息"
                v-model="textarea">
              </el-input>
              <br>
            </el-tab-pane>
            <el-button type="primary" @click="submit" class="submit-button">提交</el-button>
          </el-tabs>
          <el-table
            v-loading = 'loading'
            class="border-card2"
            :data="tableData"
            stripe
            :default-sort = "{prop: 'id', order: 'ascending'}">
            <el-table-column
              prop="id"
              label="ID"
              type="index"
              width="80"
              sortable>
            </el-table-column>
            <el-table-column
              prop="date"
              label="创建时间"
              width="160"
              sortable
              align="center">
            </el-table-column>
            <el-table-column
              label="状态"
              prop="status"
              width="160"
              align="center">
            </el-table-column>
            <el-table-column
              align="center"
              label="操作"
              width="160">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleSee(scope.$index, scope.row)">查看</el-button>
                <el-button
                  size="mini"
                  @click="handleDownload(scope.$index, scope.row)">下载</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../public/Dropdown'
import MySidnavUser from '../public/SideNavUser'
import Banner from '../public/Banner'
import axios from 'axios'
export default {
  name: 'Deblur',
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  components: {Banner, MySidnavUser, MyDropdown},
  data () {
    return {
      submitURL: this.localAPI + 'deblur/submit',
      licenseImageUrl: '',
      textarea: '',
      tableData: [],
      loading: false
    }
  },
  methods: {
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
    submit () {
      let formData = new FormData()
      formData.append('name', this.form.username)
      formData.append('phone_number', this.form.phone)
      formData.append('time_span', this.form.timespan)
      formData.append('level', this.form.level)
      console.log(formData.get('time_span'))
      console.log(formData.get('phone'))
      axios.post(this.regURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true && this.hasFace === true) {
          this.$message({
            showClose: true,
            message: '注册成功',
            type: 'success'
          })
        } else {
          let msg = errorInfo
          if (this.hasFace === false) {
            msg = '未上传人脸照片'
          }
          this.$message({
            showClose: true,
            message: msg,
            type: 'error'
          })
          console.log(formData.get('name'))
          console.log(formData.get('phone_number'))
          console.log(formData.get('time_span'))
        }
      })
    },
    handleSee () {
    },
    handleDownload () {
    }
  }
}
</script>

<style scoped>
.el-menu {
  width: 200px;
  height: 800px;
}

.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}
.side {
  top: 100px;
}
.main {
  left: 300px;
  top: 130px;
  width: 1000px;
  height: 680px;
  position: absolute;
}

.border-card1 {
  width: 400px;
  height: 620px;
  left: 10px;
  top: 20px;
  position: absolute;
}

.border-card2 {
  width: 600px;
  height: 600px;
  left: 500px;
  top: 20px;
  position: absolute;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
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
