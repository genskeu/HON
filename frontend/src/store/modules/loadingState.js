const state = {
  isLoading: false,
  title: '',
  errorOccured: false,
  errorMsg: ''
}

const getters = {
  state (state) {
    return state
  }
}

const mutations = {
  // loading state
  startLoading (state, { title }) {
    state.isLoading = true
    state.title = title
    state.errorOccured = false
    state.errorMsg = ''
  },
  // loading state
  finishLoading (state, { errorOccured, errorMsg }) {
    state.isLoading = false
    state.errorOccured = errorOccured
    state.errorMsg = errorMsg
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations
}
