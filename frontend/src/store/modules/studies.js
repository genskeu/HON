/*  */
import { fetchStudies, delStudy } from '@/api'
import store from '@/store'

const getDefaultState = () => {
  return {
    studies: []
  }
}

const state = getDefaultState()

const getters = {
}

const actions = {
  initStudies ({ commit }) {
    // if (state.studies.length === 0) {
    store.commit('loadingState/startLoading', { title: 'Loading Study Overview' })
    fetchStudies()
      .then((response) => {
        const studies = response.data.studies
        commit('initStudies', studies)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
    // }
  },
  deleteStudy ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Deleting Study' })
    delStudy(payload.studyId, payload.loadingComp)
      .then(() => {
        commit('deleteStudy', payload.studyId)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  reset ({ commit }) {
    commit('reset')
  }
}

const mutations = {
  reset (state) {
    Object.assign(state, getDefaultState())
  },
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
