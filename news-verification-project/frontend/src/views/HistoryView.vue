<template>
  <div class="history-container">
    <div class="page-header">
      <h2 class="page-title">验证历史</h2>
      <p class="page-subtitle">查看所有新闻验证记录</p>
    </div>

    <div class="history-content" v-loading="loading">
      <transition-group name="list" tag="div" class="history-list">
        <div v-for="result in verificationResults" 
             :key="result.id" 
             class="history-item"
             @click="viewDetail(result)">
          <div class="item-header">
            <el-tag :type="result.isReal ? 'success' : 'danger'" class="status-tag">
              {{ result.isReal ? '真实新闻' : '虚假新闻' }}
            </el-tag>
            <span class="timestamp">{{ formatDate(result.timestamp) }}</span>
          </div>
          
          <div class="item-content">
            <div class="content-type">
              <el-icon v-if="result.hasText"><document /></el-icon>
              <el-icon v-if="result.hasImage"><picture /></el-icon>
              <el-icon v-if="result.hasVideo"><video-camera /></el-icon>
            </div>
            <div class="confidence-bar">
              <span class="label">可信度</span>
              <el-progress 
                :percentage="result.confidence * 100" 
                :status="result.isReal ? 'success' : 'exception'"
                :stroke-width="8"
              />
            </div>
          </div>
          
          <div class="item-footer">
            <span class="reason">{{ result.reason }}</span>
            <el-button type="primary" text>查看详情</el-button>
          </div>
        </div>
      </transition-group>

      <div v-if="!loading && verificationResults.length === 0" class="empty-state">
        <el-empty description="暂无验证记录" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Document, Picture, VideoCamera } from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()
const loading = ref(false)

const verificationResults = computed(() => store.state.verificationResults)

onMounted(async () => {
  loading.value = true
  try {
    await store.dispatch('fetchVerificationHistory')
  } finally {
    loading.value = false
  }
})

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

const viewDetail = (result) => {
  router.push(`/result/${result.id}`)
}
</script>

<style scoped>
.history-container {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.6s ease-out;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 8px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.history-content {
  max-width: 800px;
  margin: 0 auto;
}

.history-list {
  display: grid;
  gap: 20px;
}

.history-item {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  animation: slideIn 0.5s ease-out;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.status-tag {
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
}

.timestamp {
  color: #909399;
  font-size: 14px;
}

.item-content {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.content-type {
  display: flex;
  gap: 8px;
  color: #909399;
}

.confidence-bar {
  flex: 1;
}

.label {
  font-size: 14px;
  color: #666;
  margin-right: 8px;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reason {
  color: #666;
  font-size: 14px;
  flex: 1;
  margin-right: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 动画 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-item {
    padding: 16px;
  }
  
  .item-content {
    flex-direction: column;
    gap: 12px;
  }
}
</style> 