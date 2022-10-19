// import cornerstone from 'cornerstone-core'
import cornerstone from 'cornerstone-core'
import cornerstoneTools from 'cornerstone-tools'
import { tools } from '@/store/modules/currentStudy/tools'

const state = {
  refviewers: [],
  viewers: [],
  // workaround to get rid of warnings
  toolsInitialized: false
}

// interface class to hold data from cornerstone image viewers and tools
class Viewer {
  constructor () {
    this.element = undefined
    this.stackDisplayed = {
      csStack: {
        imageIds: [],
        currentImageIdIndex: Number
      },
      name: String,
      savedSegmentation: undefined,
      savedToolstate: undefined,
      savedViewport: undefined
    }
    this.viewportSettings = {
      windowWidth: Number,
      windowCenter: Number,
      scale: Number,
      rotation: Number,
      posX: Number,
      posY: Number
    }
    this.toolState = {
      annotations: {
        CircleRoi: {},
        RectangleRoi: {},
        EllipticalRoi: {},
        FreehandRoi: {},
        LengthMeasurement: {}
      }
    }
  }
}

const getters = {
  // viewer
  viewers (state) {
    return state.viewers
  },
  refviewers (state) {
    return state.refviewers
  },
  viewer: (state) => (index, viewertype) => {
    return state[viewertype][index]
  },
  stackDisplayed: (state) => (index, viewertype) => {
    const viewer = state[viewertype][index]
    if (viewer && viewer.stackDisplayed) {
      return viewer.stackDisplayed
    } else {
      return undefined
    }
  },
  element: (state) => (index, viewertype) => {
    return state[viewertype][index].element
  },
  cornerstoneViewerWindowWidth: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.windowWidth
  },
  cornerstoneViewerWindowCenter: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.windowCenter
  },
  cornerstoneViewerScale: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.scale
  },
  cornerstoneViewerPosX: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.posX
  },
  cornerstoneViewerPosY: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.posY
  },
  cornerstoneViewerRotation: (state) => (index, viewertype) => {
    return state[viewertype][index].viewportSettings.rotation
  },
  // tools
  toolsInitialized (state) {
    return state.toolsInitialized
  },
  // tools avaiblable
  viewerSettingToolsMousekeys () {
    return tools.toolsMousekeys.viewerSetting
  },
  annotationToolsMousekeys () {
    return tools.toolsMousekeys.annotation
  },
  segmentationToolsMousekeys () {
    return tools.toolsMousekeys.segmentation
  },
  viewerSettingToolsMousewheel () {
    return tools.toolsMousewheel.viewerSetting
  },
  // viewer tool state
  EllipticalRois: (state) => (index, viewertype) => {
    if (state[viewertype][index].toolState.annotations.EllipticalRoi) {
      return state[viewertype][index].toolState.annotations.EllipticalRoi
    } else {
      return {}
    }
  },
  RectangleRois: (state) => (index, viewertype) => {
    if (state[viewertype][index].toolState.annotations.RectangleRoi) {
      return state[viewertype][index].toolState.annotations.RectangleRoi
    } else {
      return {}
    }
  },
  CircleRois: (state) => (index, viewertype) => {
    if (state[viewertype][index].toolState.annotations.CircleRoi) {
      return state[viewertype][index].toolState.annotations.CircleRoi
    } else {
      return {}
    }
  },
  Roi: (state) => (index, viewertype, uuid, roiType) => {
    return state[viewertype][index].toolState.annotations[roiType][uuid]
  },
  // imgsets
  getImgset (state) {
    var imgset = {
      position: Number,
      stacks: []
    }
    const viewersAll = state.refviewers.concat(state.viewers)
    viewersAll.forEach((viewer, index) => {
      const element = viewer.element
      const viewport = cornerstone.getViewport(element)
      if (viewport) {
        const imageIds = viewer.stackDisplayed.csStack.imageIds
        var stack = {
          div_id: 'dicom_img_' + index,
          image_names: imageIds.map((id) => id.split('/').pop()),
          base_url: imageIds[0].substring(0, imageIds[0].lastIndexOf('/')).replace('wadouri:', '') + '/',
          name: viewer.stackDisplayed.name,
          segmentation_data: '',
          tool_state: imageIds.map((id) => cornerstoneTools.globalImageIdSpecificToolStateManager.saveImageIdToolState(id)),
          viewport: viewport
        }
        imgset.stacks.push(stack)
      }
    })
    return imgset
  }
}

const mutations = {
  // viewer
  initViewer (state, payload) {
    const viewer = new Viewer()
    state[payload.viewertype].push(viewer)
  },
  updateViewerElement (state, payload) {
    var viewer = state[payload.viewertype][payload.index]
    viewer.element = payload.element
  },
  removeCornerstoneViewer (state, viewer) {
    state.viewers = state.viewers.filter(v => v.element !== viewer)
    state.refviewers = state.refviewers.filter(v => v.element !== viewer)
  },
  stackDisplayed (state, payload) {
    var viewer = state[payload.viewertype][payload.index]
    if (viewer) {
      viewer.stackDisplayed =
      {
        name: payload.name,
        csStack: {
          currentImageIdIndex: payload.stackDisplayed.currentImageIdIndex,
          imageIds: payload.stackDisplayed.imageIds
        },
        savedViewport: payload.savedViewport,
        savedToolstate: payload.savedToolstate,
        savedSegmentation: payload.savedSegmentation
      }
    }
  },
  // viewport settings
  cornerstoneViewerWindowWidth: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.windowWidth = Number(payload.windowWidth)
  },
  cornerstoneViewerWindowCenter: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.windowCenter = Number(payload.windowCenter).toFixed(2)
  },
  cornerstoneViewerScale: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.scale = Number(payload.scale).toFixed(2)
  },
  cornerstoneViewerPosX: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.posX = Number(payload.posX).toFixed(2)
  },
  cornerstoneViewerPosY: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.posY = Number(payload.posY).toFixed(2)
  },
  cornerstoneViewerRotation: (state, payload) => {
    var viewer = state[payload.viewertype][payload.viewer]
    viewer.viewportSettings.rotation = Number(payload.rotation).toFixed(2)
  },
  cornerstoneViewportAdd (state, viewport) {
    state.viewports.push(viewport)
  },
  cornerstoneViewportUpdate (state, payload) {
    var viewportSettings = state[payload.viewertype][payload.index].viewportSettings
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
    var viewer = state[payload.viewertype][payload.index]
    if (!viewer.toolState.annotations[payload.type]) {
      viewer.toolState.annotations[payload.type] = {}
    }
    var annotations = viewer.toolState.annotations[payload.type]
    annotations[payload.uuid] = payload.annotation
  },
  updateAnnotation (state, payload) {
    var viewer = state[payload.viewertype][payload.index]
    var annotations = viewer.toolState.annotations[payload.type]
    annotations[payload.uuid] = payload.annotation
  },
  removeAnnotation (state, payload) {
    var viewer = state[payload.viewertype][payload.index]
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
