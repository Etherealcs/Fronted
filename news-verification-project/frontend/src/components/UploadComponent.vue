<template>
  <div class="upload-container">
    <div class="upload-content" v-if="activeTab === 'text'">
      <el-input
        v-model="textContent"
        type="textarea"
        :rows="6"
        placeholder="请输入需要验证的新闻文本"
        class="text-input"
      />
    </div>

    <div class="upload-content" v-else-if="activeTab === 'image'">
      <el-upload
        class="upload-area"
        drag
        action="#"
        :auto-upload="false"
        :http-request="handleImageUpload"
        :on-change="handleImageChange"
      >
        <el-icon class="upload-icon"><upload-filled /></el-icon>
        <div class="upload-text">
          <h3>点击或拖拽文件到此处上传</h3>
          <p>支持 jpg、png、gif 格式的图片文件</p>
        </div>
      </el-upload>
    </div>

    <div class="upload-content" v-else-if="activeTab === 'video'">
      <el-upload
        class="upload-area"
        drag
        action="#"
        :auto-upload="false"
        :http-request="handleVideoUpload"
        :on-change="handleVideoChange"
      >
        <el-icon class="upload-icon"><video-camera /></el-icon>
        <div class="upload-text">
          <h3>点击或拖拽文件到此处上传</h3>
          <p>支持 mp4、avi、mov 格式的视频文件</p>
        </div>
      </el-upload>
    </div>

    <div class="action-buttons">
      <el-button 
        type="primary" 
        @click="handleVerify" 
        :loading="loading"
        :disabled="!canVerify"
        class="verify-button"
      >
        开始验证
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, VideoCamera } from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  activeTab: {
    type: String,
    required: true
  }
})

const textContent = ref('')
const loading = ref(false)
const currentFile = ref(null)

const canVerify = computed(() => {
  if (props.activeTab === 'text') {
    return textContent.value.trim().length > 0
  } else if (props.activeTab === 'image' || props.activeTab === 'video') {
    return currentFile.value !== null
  }
  return false
})

const handleImageChange = (file) => {
  if (!file) return
  const isImage = file.raw.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('请上传图片文件')
    return
  }
  currentFile.value = file.raw
}

const handleVideoChange = (file) => {
  if (!file) return
  const isVideo = file.raw.type.startsWith('video/')
  if (!isVideo) {
    ElMessage.error('请上传视频文件')
    return
  }
  currentFile.value = file.raw
}

const handleImageUpload = async (options) => {
  // 这个函数现在只在验证时被调用
  const formData = new FormData()
  formData.append('file', options.file)
  return formData
}

const handleVideoUpload = async (options) => {
  // 这个函数现在只在验证时被调用
  const formData = new FormData()
  formData.append('file', options.file)
  return formData
}

const handleVerify = async () => {
  if (!canVerify.value) {
    ElMessage.warning(props.activeTab === 'text' ? '请输入需要验证的文本' : '请先上传文件')
    return
  }

  loading.value = true
  try {
    let response
    if (props.activeTab === 'text') {
      response = await axios.post('/api/verify/text', {
        content: textContent.value
      })
    } else {
      const formData = new FormData()
      formData.append('file', currentFile.value)
      response = await axios.post(`/api/verify/${props.activeTab}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    emit('verification-complete', response.data)
    ElMessage.success('验证完成')
  } catch (error) {
    ElMessage.error('验证失败：' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const emit = defineEmits(['verification-complete'])
</script>

<style scoped>
.upload-container {
  width: 100%;
}

.upload-content {
  margin-bottom: 24px;
}

.text-input {
  width: 100%;
  background: #fff;
  border-radius: 8px;
}

.text-input :deep(.el-textarea__inner) {
  padding: 16px;
  font-size: 16px;
  border-radius: 8px;
  border-color: #e4e7ed;
  transition: all 0.3s ease;
}

.text-input :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(100, 108, 255, 0.1);
}

.upload-area {
  width: 100%;
  background: #fff;
  border: 2px dashed #e4e7ed;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: var(--primary-color);
}

.upload-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 16px;
}

.upload-text h3 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0 0 8px;
}

.upload-text p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.verify-button {
  min-width: 120px;
  height: 40px;
  font-size: 16px;
}

.verify-button:not(:disabled) {
  background: linear-gradient(45deg, #646cff, #8f96ff);
  border: none;
}

.verify-button:not(:disabled):hover {
  background: linear-gradient(45deg, #535bf2, #7c85ff);
  border: none;
  transform: translateY(-1px);
}
</style> 