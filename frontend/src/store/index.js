import { createStore } from 'vuex'

export default createStore({
  state: {
    studies: [],
    open_study: undefined
  },
  mutations: {
    addStudy (state, study) {
      state.studies.push(study)
    },
    openStudy (state, id) {
      state.open_study = state.studies.find(study => study.id === id)
    },
    updateStudyTitle (state, studyTitle) {
      state.open_study.title = studyTitle
    },
    updateStudyDesc (state, studyDesc) {
      state.open_study.description = studyDesc
    },
    updateNumbViewer (state, numbViewer) {
      state.open_study.design.numb_img = numbViewer
    },
    closeStudy () {
      this.state.open_study = undefined
    }
  },
  actions: {
  },
  modules: {
  }
})
