import { createRouter, createWebHistory } from 'vue-router'
import VerificationView from '../views/VerificationView.vue'
import HistoryView from '../views/HistoryView.vue'
import ResultDetailView from '../views/ResultDetailView.vue'
import LoginView from '../views/LoginView.vue'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'verification',
    component: VerificationView,
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView,
    meta: { requiresAuth: true }
  },
  {
    path: '/result/:id',
    name: 'result-detail',
    component: ResultDetailView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = store.getters['user/isAuthenticated']
  const token = store.getters['user/token']
  
  // 如果有token但没有用户信息，尝试获取用户信息
  if (token && !store.getters['user/userInfo'].id) {
    try {
      await store.dispatch('user/getUserInfo')
    } catch (error) {
      // 如果获取用户信息失败，清除token
      store.commit('user/CLEAR_USER_STATE')
    }
  }
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果需要认证但未登录，重定向到登录页
    next({ 
      name: 'login', 
      query: { redirect: to.fullPath },
      replace: true 
    })
  } else if (to.name === 'login' && isAuthenticated) {
    // 如果已登录但访问登录页，重定向到首页
    next({ name: 'verification', replace: true })
  } else {
    next()
  }
})

export default router 