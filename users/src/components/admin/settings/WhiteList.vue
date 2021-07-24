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
            v-loading = 'loading'
            class="main_table"
            :data="tableData"
            stripe
            style="width: 1200px"
            :default-sort = "{prop: 'id', order: 'descending'}">
            <el-table-column
              prop="id"
              label="ID"
              type="index"
              sortable>
            </el-table-column>
            <el-table-column
              prop="name"
              label="姓名"
              width="120"
              align="center">
            </el-table-column>
            <el-table-column
              prop="phone_number"
              label="手机号"
              width="140"
              align="center">
            </el-table-column>
            <el-table-column
              prop="face_info"
              label="人脸信息"
              width="120"
              align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" inline @click="handleFace">查看和更新</el-button>
              </template>
            </el-table-column>
            <el-table-column
              label="权限信息"
              prop="level"
              width="120"
              align="center">
            </el-table-column>
            <el-table-column
              label="最早进入"
              prop="time_start"
              width="140"
              align="center">
            </el-table-column>
            <el-table-column
              label="最晚离开"
              prop="time_end"
              width="140"
              align="center">
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
          <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
                         :current-page="currentPage"
                         :page-sizes="[10,20,50,100]"
                         :page-size="pageSize"
                         layout="total, sizes, prev, pager, next, jumper"
                         :total="tableData.length">
          </el-pagination>
        </el-main>
      </el-container>
      <el-dialog title="编辑"
                 :visible.sync="editFormVisible"
                 :close-on-click-modal="false"
                 class="edit-form"
                 :before-close="handleClose">
        <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="phone_number">
            <el-input v-model="editForm.phone_number" auto-complete="off" disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="权限">
            <el-select v-model="editForm.level" placeholder="权限">
              <el-option label="高(3)" value="3"></el-option>
              <el-option label="中(2)" value="2"></el-option>
              <el-option label="低(1)" value="1"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="准入时间">
            <el-time-picker
              is-range
              v-model="editForm.timespan"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              placeholder="选择时间范围"
              value-format="HH:mm:ss">
            </el-time-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="handleCancel('editForm')">取消</el-button>
          <el-button type="primary" @click.native="handleUpdate('editForm')">更新</el-button>
        </div>
      </el-dialog>
      <el-dialog title="人脸照片更新"
                 :visible.sync="editFormVisible_face"
                 :close-on-click-modal="false"
                 class="edit-face"
                 :before-close="handleClose_face">
        <el-form>
          <el-form-item label="手机号" prop="phone_number">
            <el-input v-model="editPhone" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <el-upload
          class="avatar-uploader"
          :limit="1"
          :action="faceURL"
          :headers="headers"
          :on-remove="removeChange"
          :on-error="uploadError"
          :on-change="fileChange"
          :before-upload="beforeAvatarUpload"
          :auto-upload="false"
          align="center">
          <img v-if="licenseImageUrl" :src="licenseImageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="handleCancel_face('editForm')">取消</el-button>
          <el-button type="primary" @click.native="handleUpdate_face('editForm')">更新</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'WhiteList',
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  mounted () {
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': header}).then(response => {
      this.tableData = response.data
      this.loading = false
    })
  },
  data () {
    return {
      editForm: {},
      editURL: this.localAPI + 'admin/whitelist/edit',
      editFormVisible: false, // 默认不显示编辑弹层
      delURL: this.localAPI + 'admin/whitelist/del',
      editFormVisible_face: false,
      licenseImageUrl: '',
      editPhone: '',
      loading: true,
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      activeIndex: this.$route.path,
      imgSrc: require('../../../assets/img3.jpg'),
      search: '',
      tableData: []
    }
  },
  methods: {
    // 点击编辑
    handleEdit (index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row) // 这句是关键！！！
      this.editForm.timespan = []
      this.editForm.timespan.push(row.time_start)
      this.editForm.timespan.push(row.time_end)
      console.log(this.editForm.timespan)
    },
    handleFace (index, row) {
      this.editFormVisible_face = true
      this.editPhone = row.phone_number
      console.log(this.editPhone)
    },
    // 点击关闭dialog
    handleClose (done) {
      /* done();
      location.reload(); */
      this.editFormVisible = false
    },
    // 点击取消
    handleCancel (formName) {
      this.editFormVisible = false
    },
    // 点击更新
    handleUpdate (forName) {
      // 更新的时候就把弹出来的表单中的数据写到要修改的表格中
      // var postData = {
      //   name: this.editForm.name;
      // }
      // 这里再向后台发个post请求重新渲染表格数据
      let formData = new FormData()
      formData.append('name', this.editForm.name)
      formData.append('phone_number', this.editForm.phone_number)
      formData.append('time_span', this.editForm.timespan)
      formData.append('level', this.editForm.level)
      axios.post(this.editURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '编辑成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': this.headers}).then(response => {
            this.tableData = response.data
            this.loading = false
          })
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
        }
      })
      this.editFormVisible = false
    },
    handleDelete (index, row) {
      let formData = new FormData()
      formData.append('phone_number', row.phone_number)
      console.log(row.phone_number)
      axios.post(this.delURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': this.headers}).then(response => {
            this.tableData = response.data
            this.loading = false
          })
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
        }
      })
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
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
      formData.append('face', this.form.file.raw)
      console.log(formData.get('face'))
      console.log(formData.get('phone'))
      axios.post(this.uploadURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('上传成功')
        this.licenseImageUrl = this.localMedia + res.data
        console.log(this.licenseImageUrl)
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
