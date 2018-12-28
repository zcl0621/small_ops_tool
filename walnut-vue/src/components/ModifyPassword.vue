<template>
  <div id="modifypassword">
    <el-row type="flex" class="row-bg" justify="center">
    <el-col>
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
    >
      <el-form-item label="用户名" prop="username">
          <el-input v-model="ruleForm.username" placeholder="请输入域账号"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
          <el-input type="password" v-model="ruleForm.password" placeholder="请输入新密码 6位以上 由大小写字母加数字加符号组成"></el-input>
      </el-form-item>
      <el-form-item label="短信验证码" prop="msmcode">
            <el-input v-model="ruleForm.msmcode" placeholder="请输入绑定域账号手机收到的6位短信验证码">
              <el-button slot="append" @click="actionsmscode()" :loading="(isLoading ? true : false)">{{ buttonName }}</el-button>
            </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
    </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'ModifyPassword',
  data () {
    return {
      isLoading: false,
      buttonName: '获取验证码',
      time: 60,
      ruleForm: {
        username: '',
        password: '',
        msmcode: ''
      },
      rules: {
        username: [
          { type: 'string', required: true, message: '请输入用户名', trigger: 'blur' },
          { type: 'string', required: true, message: '请输入正确的用户名', trigger: 'change', pattern: /^[^@]+$/ }, // eslint-disable-line
        ],
        password: [
          { type: 'string', required: true, message: '未输入密码', trigger: 'blur', whitespace: false },
          { type: 'string', required: true, message: '密码复杂度不够或未输入密码', trigger: 'change', whitespace: false } // eslint-disable-line
        ],
        msmcode: [
          { type: 'string', required: true, message: '请输入短信验证码', trigger: 'blur' },
          { type: 'string', required: true, message: '短信验证码为6位数字', trigger: 'change', len: 6, pattern: /[0-9]/ }
        ]
      }
    }
  },
  methods: {
    get_sms_code () {
      this.$http({
        method: 'GET',
        url: '/api/password/?username=' + this.ruleForm.username
      }).then(response => {
        localStorage.sms_code = response.data.code
        localStorage.cn_name = response.data.cn_name
      }, function (error) {
        alert(error.response.data.code)
      })
    },
    sms_code_count_down (me) {
      if (!localStorage.send_numb) {
        localStorage.send_numb = 1
      } else {
        ++localStorage.send_numb
      }
      me.time = 60 * localStorage.send_numb
      let interval = window.setInterval(function () {
        me.buttonName = '（' + me.time + '秒）后重新发送'
        --me.time
        if (me.time < 0) {
          me.buttonName = '重新发送'
          me.time = 60 * localStorage.send_numb
          me.isLoading = false
          window.clearInterval(interval)
        }
      }, 1000)
    },
    actionsmscode () {
      if (!this.ruleForm.username) {
        alert('用户名未输入')
      } else {
        this.isLoading = true
        this.sms_code_count_down(this)
        this.get_sms_code()
      }
    },
    postForm () {
      var data = {
        'username': this.ruleForm.username,
        'sms_code': this.ruleForm.msmcode,
        'cn_name': localStorage.cn_name,
        'password': this.ruleForm.password
      }
      console.log(data)
      this.$http({
        url: '/api/password/',
        method: 'POST',
        data: data
      }).then(response => {
        alert(response.data.data)
        location.reload()
      },
      function (error) {
        alert(error.response.data.data)
        return false
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.ruleForm.msmcode === localStorage.sms_code) {
            this.postForm()
          } else {
            alert('验证码错误')
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  },
  created () {
    if (localStorage.send_numb) {
      this.sms_code_count_down(this)
    }
  }
}
</script>
