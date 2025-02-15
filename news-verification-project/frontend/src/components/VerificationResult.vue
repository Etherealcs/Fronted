<template>
  <div class="result-container" v-if="result">
    <div class="result-header">
      <h3 class="result-title">验证结果</h3>
      <el-tag :type="result.isReal ? 'success' : 'danger'" class="result-tag">
        {{ result.isReal ? '真实新闻' : '虚假新闻' }}
      </el-tag>
    </div>

    <div class="result-content">
      <div class="confidence-section">
        <div class="confidence-header">
          <span class="confidence-label">可信度</span>
          <span class="confidence-value">{{ (result.confidence * 100).toFixed(2) }}%</span>
        </div>
        <el-progress 
          :percentage="result.confidence * 100" 
          :status="result.isReal ? 'success' : 'exception'"
          :stroke-width="10"
          class="confidence-progress"
        />
      </div>

      <div class="analysis-section">
        <h4 class="section-title">分析依据</h4>
        <p class="analysis-text">{{ result.reason }}</p>
      </div>

      <div class="chart-section">
        <h3>详细分析</h3>
        <div class="analysis-grid">
          <!-- 基础分析因素 -->
          <div class="analysis-group">
            <h4>基础分析</h4>
            <div class="analysis-items">
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

          <!-- 深度分析数据 -->
          <div class="analysis-group">
            <h4>深度分析</h4>
            <div class="analysis-items">
              <div class="analysis-item" v-for="(value, key) in result.analysisData" :key="key">
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

          <!-- 内容展示区域 -->
          <div class="content-display" v-if="result.type === 'text'">
            <h4>验证内容</h4>
            <div class="content-text">{{ result.content }}</div>
          </div>
          <div class="content-display" v-else-if="result.type === 'image'">
            <h4>图片内容</h4>
            <img :src="result.imageUrl" class="content-image" alt="验证图片" />
          </div>
          <div class="content-display" v-else-if="result.type === 'video'">
            <h4>视频内容</h4>
            <video :src="result.videoUrl" class="content-video" controls></video>
          </div>
        </div>
      </div>

      <div class="meta-section">
        <div class="meta-item">
          <el-icon><timer /></el-icon>
          <span>验证时间：{{ new Date(result.timestamp).toLocaleString() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { Timer } from '@element-plus/icons-vue'

const props = defineProps({
  result: {
    type: Object,
    required: true
  }
})

const getProgressColor = (value) => {
  if (value >= 0.8) return '#67C23A'  // 绿色
  if (value >= 0.6) return '#E6A23C'  // 黄色
  return '#F56C6C'  // 红色
}
</script>

<style scoped>
.result-container {
  margin-top: 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.result-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.result-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.result-tag {
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
}

.result-content {
  padding: 24px;
}

.confidence-section {
  margin-bottom: 24px;
}

.confidence-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.confidence-label {
  font-size: 16px;
  color: #666;
}

.confidence-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
}

.confidence-progress {
  margin-top: 8px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px;
}

.analysis-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.analysis-text {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.chart-section {
  margin-bottom: 24px;
}

.analysis-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  margin-top: 20px;
}

.analysis-group {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
}

.analysis-group h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.analysis-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.analysis-item {
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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

.content-display {
  grid-column: 1 / -1;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
}

.content-display h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.content-text {
  background: white;
  padding: 16px;
  border-radius: 8px;
  line-height: 1.6;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
}

.content-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}

.content-video {
  width: 100%;
  max-width: 800px;
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}

.meta-section {
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.meta-item .el-icon {
  font-size: 16px;
}

/* Element Plus 样式覆盖 */
:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

:deep(.el-progress-bar__inner) {
  border-radius: 4px;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }
}
</style> 