<template>
  <div class="detail-container">
    <div class="detail-content" v-if="result" v-loading="loading">
      <div class="detail-header">
        <el-button @click="goBack" class="back-button">
          <el-icon><arrow-left /></el-icon>
          返回
        </el-button>
        <div class="header-content">
          <h2 class="title">验证详情</h2>
          <el-tag :type="result.isReal ? 'success' : 'danger'" size="large">
            {{ result.isReal ? '真实新闻' : '虚假新闻' }}
          </el-tag>
        </div>
      </div>

      <div class="detail-body">
        <div class="section confidence-section">
          <div class="section-header">
            <h3>总体可信度</h3>
            <div class="confidence-value">{{ (result.confidence * 100).toFixed(2) }}%</div>
          </div>
          <el-progress 
            :percentage="result.confidence * 100" 
            :status="result.isReal ? 'success' : 'exception'"
            :stroke-width="12"
          />
        </div>

        <div class="section content-section">
          <h3>验证内容</h3>
          <div class="content-grid">
            <div v-if="result.text" class="content-item text-content">
              <div class="content-header">
                <el-icon><document /></el-icon>
                <span>文本内容</span>
              </div>
              <div class="text-preview">{{ result.text }}</div>
            </div>

            <div v-if="result.images && result.images.length" class="content-item image-content">
              <div class="content-header">
                <el-icon><picture /></el-icon>
                <span>图片内容</span>
              </div>
              <el-carousel :interval="4000" type="card" height="200px">
                <el-carousel-item v-for="(image, index) in result.images" :key="index">
                  <img :src="image" class="carousel-image" />
                </el-carousel-item>
              </el-carousel>
            </div>

            <div v-if="result.videos && result.videos.length" class="content-item video-content">
              <div class="content-header">
                <el-icon><video-camera /></el-icon>
                <span>视频内容</span>
              </div>
              <video 
                v-for="(video, index) in result.videos" 
                :key="index"
                controls 
                class="video-player"
              >
                <source :src="video" type="video/mp4">
              </video>
            </div>
          </div>
        </div>

        <div class="section analysis-section">
          <h3>分析结果</h3>
          <div class="analysis-grid">
            <div class="analysis-item" v-for="(value, key) in result.factors" :key="key">
              <div class="analysis-header">
                <span class="analysis-label">{{ key }}</span>
                <span class="analysis-value">{{ (value * 100).toFixed(2) }}%</span>
              </div>
              <el-progress 
                :percentage="value * 100" 
                :color="getProgressColor(value)"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>

        <div class="section reason-section">
          <h3>分析依据</h3>
          <div class="reason-content">{{ result.reason }}</div>
        </div>

        <div class="section chart-section">
          <h3>数据分析</h3>
          <div class="chart-container">
            <spark-analysis-chart :data="result.analysisData" />
          </div>
        </div>
      </div>

      <div class="detail-footer">
        <span class="timestamp">验证时间：{{ formatDate(result.timestamp) }}</span>
        <el-button type="primary" @click="shareResult">分享结果</el-button>
      </div>
    </div>

    <el-empty v-else description="未找到相关验证结果" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Document, Picture, VideoCamera } from '@element-plus/icons-vue'
import SparkAnalysisChart from '../components/SparkAnalysisChart.vue'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()
const route = useRoute()
const loading = ref(false)

const result = computed(() => {
  return store.getters.getResultById(Number(route.params.id))
})

onMounted(async () => {
  if (!result.value) {
    loading.value = true
    try {
      await store.dispatch('fetchVerificationHistory')
    } finally {
      loading.value = false
    }
  }
})

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

const getProgressColor = (value) => {
  if (value >= 0.8) return '#67C23A'
  if (value >= 0.6) return '#E6A23C'
  return '#F56C6C'
}

const goBack = () => {
  router.back()
}

const shareResult = () => {
  // 实现分享功能
  ElMessage.success('分享功能开发中')
}
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.detail-content {
  max-width: 1000px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: fadeIn 0.6s ease-out;
}

.detail-header {
  padding: 24px;
  border-bottom: 1px solid #eee;
  position: relative;
}

.back-button {
  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
}

.header-content {
  text-align: center;
  margin: 0 60px;
}

.title {
  margin: 0 0 12px;
  font-size: 24px;
  background: linear-gradient(45deg, #646cff, #8f96ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.detail-body {
  padding: 24px;
}

.section {
  margin-bottom: 32px;
  animation: slideUp 0.6s ease-out;
}

.section h3 {
  margin: 0 0 16px;
  font-size: 18px;
  color: #333;
}

.confidence-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.confidence-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
}

.content-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.content-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
}

.content-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #666;
}

.text-preview {
  max-height: 200px;
  overflow-y: auto;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.video-player {
  width: 100%;
  border-radius: 8px;
}

.analysis-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.analysis-item {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.analysis-label {
  color: #666;
  font-size: 14px;
}

.analysis-value {
  font-weight: 600;
  color: var(--primary-color);
}

.reason-content {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  line-height: 1.6;
}

.chart-container {
  height: 400px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.detail-footer {
  padding: 20px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timestamp {
  color: #909399;
  font-size: 14px;
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
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
  .detail-content {
    border-radius: 0;
  }
  
  .content-grid,
  .analysis-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    margin: 0 40px;
  }
}
</style> 