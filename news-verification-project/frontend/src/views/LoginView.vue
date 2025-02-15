<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-form" :class="{ 'form-login': !isRegister, 'form-register': isRegister }">
        <h2 class="title">{{ isRegister ? '注册账号' : '欢迎回来' }}</h2>
        <p class="subtitle">{{ isRegister ? '创建一个新账号以使用全部功能' : '登录您的账号以继续使用' }}</p>

        <el-form 
          ref="formRef" 
          :model="form" 
          :rules="rules" 
          class="form"
          label-position="top"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <template v-if="isRegister">
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="确认密码"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item prop="email">
              <el-input
                v-model="form.email"
                placeholder="电子邮箱"
                :prefix-icon="Message"
              />
            </el-form-item>
          </template>

          <div class="form-options" v-if="!isRegister">
            <el-checkbox v-model="form.remember">记住我</el-checkbox>
            <el-button link type="primary">忘记密码？</el-button>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              class="submit-btn"
              :loading="loading"
              @click="handleSubmit"
            >
              {{ isRegister ? '注册' : '登录' }}
            </el-button>
          </el-form-item>

          <div class="form-footer">
            <p>
              {{ isRegister ? '已有账号？' : '还没有账号？' }}
              <el-button link type="primary" @click="toggleForm">
                {{ isRegister ? '立即登录' : '立即注册' }}
              </el-button>
            </p>
          </div>
        </el-form>

        <div class="social-login">
          <div class="divider">
            <span>或使用以下方式</span>
          </div>
          <div class="social-buttons">
            <el-button circle class="social-btn wechat">
              <el-icon><svg-icon name="wechat" /></el-icon>
            </el-button>
            <el-button circle class="social-btn qq">
              <el-icon><svg-icon name="qq" /></el-icon>
            </el-button>
            <el-button circle class="social-btn weibo">
              <el-icon><svg-icon name="weibo" /></el-icon>
            </el-button>
          </div>
        </div>
      </div>

      <div class="login-banner">
        <div class="banner-content">
          <img src="@/assets/login-banner.svg" alt="登录插图" class="banner-image" />
          <h3>新闻真假检测系统</h3>
          <p>使用先进的AI技术，为您提供准确的新闻真实性分析</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()
const route = useRoute()
const formRef = ref(null)
const loading = ref(false)
const isRegister = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  remember: false
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (form.confirmPassword !== '') {
      formRef.value?.validateField('confirmPassword')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (isRegister.value) {
      await store.dispatch('user/register', {
        username: form.username,
        password: form.password,
        email: form.email
      })
      ElMessage.success('注册成功')
      isRegister.value = false
    } else {
      await store.dispatch('user/login', {
        username: form.username,
        password: form.password,
        remember: form.remember
      })
      ElMessage.success('登录成功')
      
      // 获取重定向路径
      const redirectPath = route.query.redirect || '/'
      router.push(redirectPath)
    }
  } catch (error) {
    console.error(error)
    ElMessage.error(error.response?.data?.error || error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const toggleForm = () => {
  isRegister.value = !isRegister.value
  formRef.value?.resetFields()
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-box {
  width: 1000px;
  height: 600px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  display: flex;
  overflow: hidden;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.login-form {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  transition: all 0.5s ease;
  opacity: 0;
  transform: translateX(-20px);
  animation: slideIn 0.5s ease forwards;
}

.form-login {
  animation-delay: 0.2s;
}

.form-register {
  animation-delay: 0.3s;
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 8px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: titleGlow 2s ease-in-out infinite;
}

@keyframes titleGlow {
  0%, 100% {
    filter: brightness(100%);
  }
  50% {
    filter: brightness(120%);
  }
}

.subtitle {
  color: #666;
  margin: 0 0 32px;
  font-size: 16px;
}

.form {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form :deep(.el-input__wrapper) {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 4px 16px rgba(100, 108, 255, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 8px 0;
}

.submit-btn {
  height: 44px;
  font-size: 16px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  border: none;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 108, 255, 0.3);
  background: linear-gradient(45deg, #535bf2, #7c85ff);
}

.form-footer {
  text-align: center;
  margin-top: 24px;
}

.social-login {
  margin-top: 32px;
}

.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: #999;
  font-size: 14px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, #eee, transparent);
  margin: 0 16px;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.social-btn {
  width: 44px;
  height: 44px;
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.social-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: currentColor;
  opacity: 0.1;
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
}

.social-btn:hover::before {
  opacity: 0.2;
}

.wechat {
  color: #07c160;
}

.qq {
  color: #12b7f5;
}

.weibo {
  color: #e6162d;
}

.login-banner {
  width: 500px;
  background: linear-gradient(135deg, #646cff 0%, #8f96ff 100%);
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.banner-content {
  position: relative;
  z-index: 1;
  max-width: 360px;
}

.banner-image {
  width: 100%;
  max-width: 300px;
  margin-bottom: 32px;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.banner-content h3 {
  font-size: 28px;
  margin: 0 0 16px;
  font-weight: 600;
}

.banner-content p {
  opacity: 0.9;
  line-height: 1.6;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .login-box {
    width: 100%;
    max-width: 500px;
    height: auto;
    flex-direction: column-reverse;
  }

  .login-banner {
    width: 100%;
    padding: 32px;
  }

  .banner-image {
    max-width: 200px;
  }

  .login-form {
    padding: 32px;
  }
}

@media (max-width: 480px) {
  .login-form {
    padding: 24px;
  }

  .title {
    font-size: 24px;
  }

  .subtitle {
    font-size: 14px;
  }

  .social-buttons {
    flex-wrap: wrap;
  }
}
</style> 