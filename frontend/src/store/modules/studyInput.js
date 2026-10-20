import store from '@/store'
import { saveResultDb } from '@/api'

const getDefaultState = () => {
  return {
    studyId: null,
    userId: null,
    scaleInputs: [],
    textInputs: [],
    studyResultsUser: []
  }
}

const state = getDefaultState()

class ScaleInput {
  constructor (scaleName, scaleValue, scaleMin, scaleMax, uuidAnnotation = null) {
    this.name = scaleName
    this.value = scaleValue
    this.min = scaleMin
    this.max = scaleMax
    this.uuid = uuidAnnotation
  }
}

class TextInput {
  constructor (name, value = null) {
    this.name = name
    this.value = value
  }
}

const getters = {
  scaleInput: (state) => (index) => {
    return state.scaleInputs[index]
  },
  scaleInputs (state) {
    return state.scaleInputs
  },
  textInputs (state) {
    return state.textInputs
  },
  textInput: (state) => (index) => {
    return state.textInputs[index]
  },
  resultsCurrentUser (state) {
    return state.studyResultsUser
  }
}

const mutations = {
  openStudyInput (state, studyInput) {
    state.studyId = studyInput.studyId
    state.userId = studyInput.userId
    state.studyResultsUser = studyInput.studyResultsUser || []
    state.scaleInputs = []
    state.textInputs = []
  },
  reset (state) {
    Object.assign(state, getDefaultState())
  },
  scaleInput (state, { index, scaleName, scaleValue, scaleMin, scaleMax }) {
    const scale = new ScaleInput(scaleName, scaleValue, scaleMin, scaleMax)
    state.scaleInputs[index] = scale
  },
  updScaleInput (state, { index, scaleValue }) {
    state.scaleInputs[index].value = scaleValue
  },
  resetscaleInputs (state) {
    state.scaleInputs.forEach((scale) => {
      scale.value = null
      scale.uuid = null
    })
    state.textInputs.forEach((input) => {
      if (input) input.value = null
    })
  },
  addTextInput (state, { index, name, value }) {
    state.textInputs[index] = new TextInput(name, value)
  },
  updTextInput (state, { index, value }) {
    state.textInputs[index].value = value
  },
  addResultCurrentUser (state, result) {
    state.studyResultsUser.push(result)
  },
  removeResultsCurrentUser (state) {
    state.studyResultsUser = []
  }
}

const actions = {
  reset ({ commit }) {
    commit('reset')
  },    
  saveResult ({ commit, state }, payload) {
    store.commit('loadingState/startLoading', { title: 'Saving Results' })
    saveResultDb(state.studyId, payload)
      .then((response) => {
        debugger
        const result = response.data.result
        const usp = response.data.study_progress
        store.commit('currentStudy/userStudyProgress', usp)
        commit('addResultCurrentUser', result)
        // progress of all users lives in the currentStudy module (admin view)
        commit('resetscaleInputs')
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        console.log('Error saving result: ', response)  
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}