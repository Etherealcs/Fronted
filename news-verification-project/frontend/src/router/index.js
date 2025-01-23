import { createRouter, createWebHistory } from 'vue-router'
import VerificationView from '../views/VerificationView.vue'
import HistoryView from '../views/HistoryView.vue'
import ResultDetailView from '../views/ResultDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'verification',
    component: VerificationView
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView
  },
  {
    path: '/result/:id',
    name: 'result-detail',
    component: ResultDetailView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 