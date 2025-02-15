<template>
  <div class="verification-container">
    <div class="page-header">
      <h2 class="page-title">使用 AI 创建</h2>
      <p class="page-subtitle">您希望如何开始？</p>
    </div>

    <div class="verification-options">
      <div class="option-card" @click="activeTab = 'text'">
        <div class="option-icon text-icon">
          <el-icon><document /></el-icon>
        </div>
        <div class="option-content">
          <h3>粘贴文本</h3>
          <p>根据笔记、大纲或现有内容创建</p>
          <span class="tag">文字检测</span>
        </div>
      </div>

      <div class="option-card" @click="activeTab = 'image'">
        <div class="option-icon image-icon">
          <el-icon><picture /></el-icon>
        </div>
        <div class="option-content">
          <h3>图片验证</h3>
          <p>在几秒钟内分析图片真实性</p>
          <span class="tag">图像检测</span>
        </div>
      </div>

      <div class="option-card" @click="activeTab = 'video'">
        <div class="option-icon video-icon">
          <el-icon><video-camera /></el-icon>
        </div>
        <div class="option-content">
          <h3>视频验证</h3>
          <p>增强现有视频、演示文稿或网页的功能</p>
          <span class="tag">视频检测</span>
        </div>
      </div>
    </div>

    <div class="verification-content" v-if="activeTab">
      <upload-component @verification-complete="handleVerificationComplete" :active-tab="activeTab" />
      <verification-result v-if="verificationResult" :result="verificationResult" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Document, Picture, VideoCamera } from '@element-plus/icons-vue'
import UploadComponent from '../components/UploadComponent.vue'
import VerificationResult from '../components/VerificationResult.vue'

const activeTab = ref('')
const verificationResult = ref(null)

const handleVerificationComplete = (result) => {
  verificationResult.value = result
}

// 添加 watch 监听 activeTab 变化
watch(activeTab, () => {
  verificationResult.value = null
})
</script>

<style scoped>
.verification-container {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--text-color);
}

.page-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.verification-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.option-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #eee;
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.option-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.option-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.text-icon {
  background: #e6f7ff;
  color: #1890ff;
}

.image-icon {
  background: #f6ffed;
  color: #52c41a;
}

.video-icon {
  background: #fff7e6;
  color: #fa8c16;
}

.option-content {
  flex: 1;
}

.option-content h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
}

.option-content p {
  margin: 0 0 12px;
  color: #666;
  font-size: 14px;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.verification-content {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style> 