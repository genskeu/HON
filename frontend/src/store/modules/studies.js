/*  */
import { fetchStudies, delStudy } from '@/api'

const state = {
  studies: []
}

const getters = {
}

const actions = {
  initStudies ({ commit }) {
    if (state.studies.length === 0) {
      fetchStudies()
        .then((response) => {
          const studies = response.data.studies
          commit('initStudies', studies)
        })
    }
  },
  deleteStudy ({ commit }, payload) {
    delStudy(payload.studyId, payload.loadingComp)
      .then(() => {
        if (!payload.loadingComp.$data.error) {
          commit('deleteStudy', payload.studyId)
        }
      })
  }
}

const mutations = {
  initStudies (state, studies) {
    state.studies = studies
  },
  deleteStudy (state, studyId) {
    const index = state.studies.findIndex(study => study.id === studyId)
    state.studies.splice(index, 1)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
