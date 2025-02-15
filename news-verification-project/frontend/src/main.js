import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 配置axios
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    const token = store.getters['user/token']
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 添加响应拦截器
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // token过期或无效
      store.commit('user/CLEAR_USER_STATE')
      router.push({
        name: 'login',
        query: { redirect: router.currentRoute.value.fullPath }
      })
    }
    return Promise.reject(error)
  }
)

app.use(ElementPlus)
app.use(router)
app.use(store)

app.mount('#app') 