import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 配置axios
import axios from 'axios'
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

app.use(ElementPlus)
app.use(router)
app.use(store)

app.mount('#app') 