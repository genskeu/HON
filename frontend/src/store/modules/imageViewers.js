// import cornerstone from 'cornerstone-core'
import cornerstone from 'cornerstone-core'
import cornerstoneTools from 'cornerstone-tools'
import { tools } from '@/store/modules/tools'

const state = {
  refViewers: [],
  viewers: [],
  // workaround to get rid of warnings
  toolsInitialized: false
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
  },
  // tools
  toolsInitialized (state) {
    return state.toolsInitialized
  },
  // tools avaiblable
  viewerSettingToolsMousekeys (state) {
    return tools.toolsMousekeys.viewerSetting
  },
  annotationToolsMousekeys (state) {
    return tools.toolsMousekeys.annotation
  },
  segmentationToolsMousekeys (state) {
    return tools.toolsMousekeys.segmentation
  },
  viewerSettingToolsMousewheel (state) {
    return tools.toolsMousewheel.viewerSetting
  },
  // viewer tool state
  EllipticalRois: (state) => (index) => {
    if (state.viewers[index].toolState.annotations.EllipticalRoi) {
      return state.viewers[index].toolState.annotations.EllipticalRoi
    } else {
      return {}
    }
  },
  RectangleRois: (state) => (index) => {
    if (state.viewers[index].toolState.annotations.RectangleRoi) {
      return state.viewers[index].toolState.annotations.RectangleRoi
    } else {
      return {}
    }
  },
  CircleRois: (state) => (index) => {
    if (state.viewers[index].toolState.annotations.CircleRoi) {
      return state.viewers[index].toolState.annotations.CircleRoi
    } else {
      return {}
    }
  },
  EllipticalRoi: (state) => (index, uuid) => {
    return state.viewers[index].toolState.annotations.EllipticalRoi[uuid]
  },
  // imgsets
  getImgset (state) {
    var imgset = {
      position: Number,
      imageStacks: []
    }
    state.viewers.forEach((viewer, index) => {
      const element = viewer.element
      const viewport = cornerstone.getViewport(element)

      if (viewport) {
        var stack = {
          divId: index,
          csStack: viewer.stackDisplayed,
          name: '',
          segData: '',
          toolState: viewer.stackDisplayed.imageIds.map((id) => cornerstoneTools.globalImageIdSpecificToolStateManager.saveImageIdToolState(id)),
          viewport: viewport
        }
        imgset.imageStacks.push(stack)
      }
    })
    return imgset
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
  // viewport settings
  cornerstoneViewerWindowWidth: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowWidth = Number(payload.windowWidth).toFixed(2)
  },
  cornerstoneViewerWindowCenter: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.windowCenter = Number(payload.windowCenter).toFixed(2)
  },
  cornerstoneViewerScale: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.scale = Number(payload.scale).toFixed(2)
  },
  cornerstoneViewerPosX: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.posX = Number(payload.posX).toFixed(2)
  },
  cornerstoneViewerPosY: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.PosY = Number(payload.PosY).toFixed(2)
  },
  cornerstoneViewerRotation: (state, payload) => {
    var viewer = state.viewers[payload.viewer]
    viewer.viewportSettings.rotation = Number(payload.rotation).toFixed(2)
  },
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
  },
  // tools
  toolsInitialized (state, value) {
    state.toolsInitialized = value
  },
  // viewer tool state
  addAnnotation (state, payload) {
    var viewer = state.viewers[payload.index]
    if (!viewer.toolState.annotations[payload.type]) {
      viewer.toolState.annotations[payload.type] = {}
    }
    viewer.toolState.annotations[payload.type][payload.uuid] = payload.annotation
  },
  updateAnnotation (state, payload) {
    var viewer = state.viewers[payload.index]
    if (!viewer.toolState.annotations[payload.type]) {
      viewer.toolState.annotations[payload.type] = {}
    }
    viewer.toolState.annotations[payload.type][payload.uuid] = payload.annotation
  },
  removeAnnotation (state, payload) {
    var viewer = state.viewers[payload.index]
    // debugger // eslint-disable-line
    delete viewer.toolState.annotations[payload.type][payload.uuid]
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
