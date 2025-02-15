import axios from 'axios'

const state = {
  token: localStorage.getItem('token') || '',
  userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
  isAuthenticated: !!localStorage.getItem('token')
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    state.isAuthenticated = !!token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  },
  CLEAR_USER_STATE(state) {
    state.token = ''
    state.userInfo = {}
    state.isAuthenticated = false
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }
}

const actions = {
  async login({ commit }, { username, password, remember }) {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password,
        remember
      })
      const { token, user } = response.data
      commit('SET_TOKEN', token)
      commit('SET_USER_INFO', user)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  async register({ commit }, { username, password, email }) {
    try {
      const response = await axios.post('/api/auth/register', {
        username,
        password,
        email
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  async logout({ commit }) {
    try {
      await axios.post('/api/auth/logout')
    } finally {
      commit('CLEAR_USER_STATE')
    }
  },

  async getUserInfo({ commit }) {
    try {
      const response = await axios.get('/api/auth/user')
      commit('SET_USER_INFO', response.data)
      return response.data
    } catch (error) {
      commit('CLEAR_USER_STATE')
      throw error
    }
  }
}

const getters = {
  isAuthenticated: state => state.isAuthenticated,
  userInfo: state => state.userInfo,
  token: state => state.token
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 