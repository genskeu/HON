// import cornerstone from 'cornerstone-core'

const state = {
  viewers: []
}

const getters = {
  // viewer
  cornerstoneViewers (state) {
    return state.viewers
  },
  cornerstoneViewer: (state) => (index) => {
    return state.viewers[index].element
  },
  stackDisplayed: (state) => (index) => {
    const viewer = state.viewers[index]
    if (viewer) {
      return viewer.stackDisplayed
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
    return state.viewers[index].viewportSettings.scale
  },
  cornerstoneViewerPosX: (state) => (index) => {
    return state.viewers[index].viewportSettings.posX
  },
  cornerstoneViewerPosY: (state) => (index) => {
    return state.viewers[index].viewportSettings.posY
  },
  cornerstoneViewerRotation: (state) => (index) => {
    return state.viewers[index].viewportSettings.rotation
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
  stackDisplayed (state, payload) {
    var viewer = state.viewers[payload.index]
    viewer.stackDisplayed = payload.stackDisplayed
  },
  cornerstoneViewerWindowWidth: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowWidth = Number(payload.windowWidth)
  },
  cornerstoneViewerWindowCenter: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowCenter = Number(payload.windowCenter)
  },
  cornerstoneViewerScale: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.scale = Number(payload.scale)
  },
  cornerstoneViewerPosX: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.posX = Number(payload.posX)
  },
  cornerstoneViewerPosY: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.PosY = Number(payload.PosY)
  },
  cornerstoneViewerRotation: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.rotation = Number(payload.rotation)
  },
  // viewport
  cornerstoneViewportAdd (state, viewport) {
    state.viewports.push(viewport)
  },
  cornerstoneViewportUpdate (state, payload) {
    var viewportSettings = state.viewers[payload.index].viewportSettings
    viewportSettings.windowWidth = payload.viewport.voi.windowWidth
    viewportSettings.windowCenter = payload.viewport.voi.windowCenter
    viewportSettings.scale = payload.viewport.scale
    viewportSettings.posX = payload.viewport.translation.x
    viewportSettings.posY = payload.viewport.translation.y
    viewportSettings.rotation = payload.viewport.rotation
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
