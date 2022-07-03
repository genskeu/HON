// import cornerstone from 'cornerstone-core'

const state = {
  viewers: []
}

// function to check if viewport and vieport props exist
// could be removed if viewport control shown only if viewport exists
// function voiCheck (viewer) {
//   return viewer.viewport !== undefined && viewer.viewport.voi !== undefined
// }

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
    return state.viewers[index].element
  },
  imageDisplayed: (state) => (index) => {
    const viewer = state.viewers[index]
    if (viewer) {
      return viewer.imageDisplayed
    } else {
      return undefined
    }
  },
  cornerstoneViewerWindowWidth: (state) => (index) => {
    return state.viewers[index].viewportSettings.windowWidth
  },
  cornerstoneViewerWindowCenter: (state) => (index) => {
    return state.viewers[index].viewportSettings.windowCenter
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
  imageDisplayed (state, payload) {
    var viewer = state.viewers[payload.index]
    viewer.imageDisplayed = payload.imageDisplayed
  },
  cornerstoneViewerWindowWidth: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowWidth = Number(payload.windowWidth)
  },
  cornerstoneViewerWindowCenter: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowCenter = Number(payload.windowCenter)
  },
  // viewport
  cornerstoneViewportAdd (state, viewport) {
    state.viewports.push(viewport)
  },
  cornerstoneViewportUpdate (state, payload) {
    var viewportSettings = state.viewers[payload.index].viewportSettings
    viewportSettings.windowWidth = payload.viewport.voi.windowWidth
    viewportSettings.windowCenter = payload.viewport.voi.windowCenter
    viewportSettings.Scale = payload.viewport.scale
    viewportSettings.PosX = payload.viewport.translation.x
    viewportSettings.PosY = payload.viewport.translation.y
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
