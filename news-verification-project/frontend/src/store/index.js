import { createStore } from 'vuex'
import axios from 'axios'
import user from './modules/user'

const store = createStore({
  modules: {
    user
  },
  
  state: {
    verificationResults: [],
    currentResult: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_VERIFICATION_RESULTS(state, results) {
      state.verificationResults = results
    },
    ADD_VERIFICATION_RESULT(state, result) {
      state.verificationResults.unshift(result)
    },
    SET_CURRENT_RESULT(state, result) {
      state.currentResult = result
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async verifyContent({ commit }, payload) {
      commit('SET_LOADING', true)
      try {
        const formData = new FormData()
        
        // 添加文本内容
        if (payload.text) {
          formData.append('text', payload.text)
        }
        
        // 添加图片文件
        if (payload.images) {
          payload.images.forEach(image => {
            formData.append('images', image)
          })
        }
        
        // 添加视频文件
        if (payload.videos) {
          payload.videos.forEach(video => {
            formData.append('videos', video)
          })
        }
        
        const response = await axios.post('/api/verify/mixed', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        console.log(response.data,'response.data');
        
        const result = {
          ...response.data,
          id: Date.now(),
          timestamp: new Date().toISOString()
        }
        
        commit('ADD_VERIFICATION_RESULT', result)
        commit('SET_CURRENT_RESULT', result)
        return result
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchVerificationHistory({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/api/verify/history')
        commit('SET_VERIFICATION_RESULTS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    getResultById: (state) => (id) => {
      return state.verificationResults.find(result => result.id === id)
    },
    getLatestResults: (state) => {
      return state.verificationResults.slice(0, 10)
    }
  }
})

export default store 