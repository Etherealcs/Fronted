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

      <div class="details-section">
        <h4 class="section-title">详细分析</h4>
        <div class="chart-wrapper" v-if="result.analysisData">
          <spark-analysis-chart :data="result.analysisData" />
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
import SparkAnalysisChart from './SparkAnalysisChart.vue'

const props = defineProps({
  result: {
    type: Object,
    required: true
  }
})
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

.details-section {
  margin-bottom: 24px;
}

.chart-wrapper {
  height: 300px;
  margin-top: 16px;
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
  border-radius: 6px;
}

:deep(.el-progress-bar__inner) {
  border-radius: 6px;
  transition: all 0.3s ease;
}
</style> 