/*  */
import { fetchStudies, delStudy } from '@/api'
import store from '@/store'

const state = {
  studies: []
}

const getters = {
  loadingState (state) {
    return state.loadingState
  }
}

const actions = {
  initStudies ({ commit }) {
    // if (state.studies.length === 0) {
    store.commit('loadingState/startLoading', { title: 'Loading Study Overview' })
    fetchStudies()
      .then((response) => {
        const studies = response.data.studies
        commit('initStudies', studies)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
    // }
  },
  deleteStudy ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Deleting Study' })
    delStudy(payload.studyId, payload.loadingComp)
      .then(() => {
        commit('deleteStudy', payload.studyId)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  }
}

const mutations = {
  initStudies (state, studies) {
    state.studies = studies
  },
  addStudy (state, study) {
    state.studies.push(study)
  },
  deleteStudy (state, studyId) {
    const index = state.studies.findIndex(study => study.id === studyId)
    state.studies.splice(index, 1)
  },
  // loading state
  startLoading (state, { title }) {
    state.loadingState.isLoading = true
    state.loadingState.title = title
    state.loadingState.errorOccured = false
    state.loadingState.errorMsg = ''
  },
  // loading state
  finishLoading (state, { errorOccured, errorMsg }) {
    state.loadingState.isLoading = false
    state.loadingState.errorOccured = errorOccured
    state.loadingState.errorMsg = errorMsg
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
