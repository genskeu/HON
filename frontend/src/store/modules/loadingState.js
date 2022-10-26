const state = {
  isLoading: false,
  title: '',
  errorOccured: false,
  errorData: null
}

const getters = {
  state (state) {
    return state
  }
}

const mutations = {
  startLoading (state, { title }) {
    state.isLoading = true
    state.title = title
    state.errorOccured = false
    state.errorData = null
  },
  errorOccured (state, { errorData }) {
    state.isLoading = true
    state.errorOccured = true
    state.errorData = errorData
  },
  finishLoading (state) {
    state.isLoading = false
    state.errorOccured = false
    state.errorData = null
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations
}
