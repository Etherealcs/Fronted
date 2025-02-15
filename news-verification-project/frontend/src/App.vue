<template>
  <div class="app-container">
    <div class="animated-background">
      <div class="gradient-sphere"></div>
      <div class="gradient-sphere"></div>
      <div class="gradient-sphere"></div>
    </div>

    <header class="app-header" v-if="$route.name !== 'login'">
      <div class="header-left">
        <router-link to="/" class="logo">新闻真假检测系统</router-link>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item" active-class="active">
            <el-icon><home-filled /></el-icon>
            首页
          </router-link>
          <router-link to="/history" class="nav-item" active-class="active">
            <el-icon><histogram /></el-icon>
            历史记录
          </router-link>
        </nav>
      </div>
      <div class="header-right">
        <el-button type="primary" class="premium-btn" v-if="isAuthenticated">
          <el-icon><star-filled /></el-icon>
          获取无限AI智能
        </el-button>
        <template v-if="isAuthenticated">
          <el-dropdown @command="handleCommand">
            <el-avatar class="user-avatar" :size="32">
              {{ userInfo.username ? userInfo.username.charAt(0).toUpperCase() : 'U' }}
            </el-avatar>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="settings">设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-button type="primary">登录</el-button>
          </router-link>
        </template>
      </div>
    </header>
    
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { HomeFilled, Histogram, StarFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.getters['user/isAuthenticated'])
const userInfo = computed(() => store.getters['user/userInfo'])

const handleCommand = async (command) => {
  switch (command) {
    case 'logout':
      try {
        await store.dispatch('user/logout')
        ElMessage.success('退出登录成功')
        router.push('/login')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
      break
    case 'profile':
      // 处理个人信息
      break
    case 'settings':
      // 处理设置
      break
  }
}
</script>

<style>
:root {
  --primary-color: #646cff;
  --background-color: #f5f7fa;
  --text-color: #333;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  overflow-x: hidden;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.animated-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: -1;
}

.gradient-sphere {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 20s infinite ease-in-out;
}

.gradient-sphere:nth-child(1) {
  width: 400px;
  height: 400px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  top: -100px;
  left: -100px;
  animation-delay: -5s;
}

.gradient-sphere:nth-child(2) {
  width: 300px;
  height: 300px;
  background: linear-gradient(45deg, #ff6b6b, #ffd93d);
  bottom: -50px;
  right: -50px;
  animation-delay: -10s;
}

.gradient-sphere:nth-child(3) {
  width: 250px;
  height: 250px;
  background: linear-gradient(45deg, #4facfe, #00f2fe);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -15s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0);
  }
  25% {
    transform: translate(50px, 50px);
  }
  50% {
    transform: translate(0, 100px);
  }
  75% {
    transform: translate(-50px, 50px);
  }
}

.app-header {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo {
  font-size: 20px;
  font-weight: 600;
  color: var(--primary-color);
  text-decoration: none;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.nav-menu {
  display: flex;
  gap: 24px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(100, 108, 255, 0.1);
  color: var(--primary-color);
}

.nav-item.active {
  background: rgba(100, 108, 255, 0.1);
  color: var(--primary-color);
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.premium-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  border: none;
  transition: all 0.3s ease;
}

.premium-btn:hover {
  background: linear-gradient(45deg, #535bf2, #7c85ff);
  border: none;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(100, 108, 255, 0.3);
}

.user-avatar {
  background: linear-gradient(45deg, #646cff, #8f96ff);
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.1);
}

.app-main {
  flex: 1;
  padding: 84px 24px 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Element Plus 样式覆盖 */
.el-button--primary {
  --el-button-bg-color: var(--primary-color);
  --el-button-border-color: var(--primary-color);
  --el-button-hover-bg-color: #535bf2;
  --el-button-hover-border-color: #535bf2;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-left {
    gap: 16px;
  }
  
  .nav-menu {
    display: none;
  }
  
  .premium-btn span {
    display: none;
  }
}
</style> 