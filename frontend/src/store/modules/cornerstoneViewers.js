import cornerstone from 'cornerstone-core'

const state = {
  viewers: []
}

// function to check if viewport and vieport props exist
// could be removed if viewport control shown only if viewport exists
function voiCheck (viewer) {
  return viewer.viewport !== undefined && viewer.viewport.voi !== undefined
}

function scaleCheck (viewer) {
  return viewer.viewport !== undefined && viewer.viewport.scale !== undefined
}

function translationCheck (viewer) {
  return viewer.viewport !== undefined && viewer.viewport.translation !== undefined
}
const getters = {
  // viewer
  cornerstoneViewers (state) {
    return state.viewers
  },
  cornerstoneViewer: (state) => (index) => {
    return state.viewers[index]
  },
  cornerstoneViewerVoi: (state) => (index) => {
    if (voiCheck(state.viewers[index])) {
      return state.viewers[index].viewport.voi
    } else {
      return NaN
    }
  },
  cornerstoneViewerScale: (state) => (index) => {
    if (scaleCheck(state.viewers[index])) {
      return state.viewers[index].viewport.scale
    } else {
      return NaN
    }
  },
  cornerstoneViewerTranslation: (state) => (index) => {
    if (translationCheck(state.viewers[index])) {
      return state.viewers[index].viewport.translation
    } else {
      return NaN
    }
  }
}

const mutations = {
  // viewer
  cornerstoneViewer (state, viewer) {
    state.viewers.push(viewer)
  },
  removeCornerstoneViewer (state, viewer) {
    state.viewers = state.viewers.filter(v => v.element !== viewer)
  },
  cornerstoneViewerWW: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    if (voiCheck(viewer)) {
      viewer.viewport.voi.windowWidth = payload.windowWidth
      cornerstone.updateImage(viewer.element)
    }
  },
  cornerstoneViewerWC: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    if (voiCheck(viewer)) {
      viewer.viewport.voi.windowCenter = payload.windowCenter
      cornerstone.updateImage(viewer.element)
    }
  },
  // viewport
  cornerstoneViewportAdd (state, viewport) {
    state.viewports.push(viewport)
  },
  cornerstoneViewportUpdate (state, payload) {
    state.viewers[payload.index].viewport = payload.viewport
  }
}

const actions = {
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
