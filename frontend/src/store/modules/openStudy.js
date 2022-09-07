import router from '@/router'
import { createStudy, deleteFiles, createImgset, deleteImgsets } from '@/api'
import store from '@/store'
import { tools } from '@/store/modules/tools'

// import cornerstoneTools from 'cornerstone-tools'

const state = {
  title: String,
  password: String,
  description: String,
  design: Object,
  images: Array,
  imageSets: Array,
  instructions: String,
  user_study_progress: Array,
  imgsetDisplayed: undefined
}

const getters = {
  // meta data
  studyTitle (state) {
    return state.title
  },
  studyPassword (state) {
    return state.password
  },
  studyDescription (state) {
    return state.description
  },
  // images
  images (state) {
    return state.images
  },
  // imgsets
  imgsets (state) {
    return state.imageSets
  },
  imgsetDisplayed (state) {
    return state.imgsetDisplayed
  },
  // design data
  design (state) {
    return state.design
  },
  viewerNumb (state) {
    return Number(state.design.numb_img)
  },
  viewerLayoutCols (state) {
    return Number(state.design.img_per_row)
  },
  viewerLayoutRows (state) {
    return Number(state.design.layout_img_rows)
  },
  refviewerNumb (state) {
    return Number(state.design.numb_refimg)
  },
  buttonLabels (state) {
    return state.design.button_labels
  },
  backgroundColor (state) {
    return state.design.background_color
  },
  textColor (state) {
    return state.design.text_color
  },
  viewerHeight (state) {
    return Number(state.design.img_height)
  },
  viewerHeightAuto (state) {
    return state.design.img_height_auto
  },
  roiNumb (state) {
    return Number(state.design.numb_rois)
  },
  viewerMetainfo (state) {
    return state.design.show_viewport_info
  },
  transitionTime (state) {
    return Number(state.design.transition_time)
  },
  order (state) {
    return state.design.randomize_order
  },
  instructions (state) {
    return state.design.instructions
  },
  // scales
  scales (state) {
    return state.design.scales
  },
  scaleText: (state) => (index) => {
    return state.design.scales[index].text
  },
  scaleMin: (state) => (index) => {
    return state.design.scales[index].min
  },
  scaleMax: (state) => (index) => {
    return state.design.scales[index].max
  },
  scaleLabels: (state) => (index) => {
    return state.design.scales[index].labels
  },
  // tools with settings (saved in db)
  tools (state) {
    return state.design.tools
  },
  // complete list of tools (user interface study design)
  annToolsMousekeysSettings (state) {
    var toolsAnnotation = tools.toolsMousekeys.annotation
    // match toolsAvailable with tools with saved settings
    return matchTools(toolsAnnotation, state.design.tools)
  },
  viewerToolsMousekeysSettings (state) {
    var toolsViewerSetting = tools.toolsMousekeys.viewerSetting
    return matchTools(toolsViewerSetting, state.design.tools)
  },
  segToolsMousekeysSettings (state) {
    var toolsSegmentation = tools.toolsMousekeys.segmentation
    return matchTools(toolsSegmentation, state.design.tools)
  },
  viewerToolsMousewheelSettings (state) {
    var toolsViewerSetting = tools.toolsMousewheel.viewerSetting
    return matchTools(toolsViewerSetting, state.design.tools)
  },
  // list of tools (user interface study participation)
  annToolsMousekeysParticipant (state) {
    var toolsAnnotation = tools.toolsMousekeys.annotation
    return filterTools(toolsAnnotation, state.design.tools)
  },
  viewerToolsMousekeysParticipant (state) {
    var toolsViewerSetting = tools.toolsMousekeys.viewerSetting
    return filterTools(toolsViewerSetting, state.design.tools)
  },
  segToolsMousekeysParticipant (state) {
    var toolsSegmentation = tools.toolsMousekeys.segmentation
    return filterTools(toolsSegmentation, state.design.tools)
  },
  viewerToolsMousewheelParticipant (state) {
    var toolsViewerSetting = tools.toolsMousewheel.viewerSetting
    return filterTools(toolsViewerSetting, state.design.tools)
  },
  // stacks
  stacks (state) {
    return state.stacks
  },
  // results
  userStudyProgress (state) {
    return state.user_study_progress
  }
}

function matchTools (toolsAll, toolsSaved) {
  var toolsSettings = {}
  Object.keys(toolsAll).forEach(toolCsname => {
    var toolSetting = toolsSaved.find(tool => tool.cs_name === toolCsname)
    var label = toolsAll[toolCsname]
    if (!toolSetting) {
      toolsSettings[label] = { cs_name: toolCsname, key_binding: null, settings: {} }
    } else {
      toolsSettings[label] = toolSetting
    }
  })
  return toolsSettings
}

function filterTools (toolsAll, toolsSaved) {
  var toolsSettings = {}
  Object.keys(toolsAll).forEach(toolCsname => {
    var toolSetting = toolsSaved.find(tool => tool.cs_name === toolCsname)
    var label = toolsAll[toolCsname]
    if (toolSetting) {
      toolsSettings[label] = toolSetting
    }
  })
  return toolsSettings
}

const mutations = {
  openStudy (state, study) {
    state.title = study.title
    state.password = ''
    state.description = study.description
    state.design = study.design
    state.images = study.images
    state.stacks = study.stacks
    state.imageSets = study.imgsets
    state.instructions = study.instructions
    state.user_study_progress = study.user_study_progress
  },
  closeStudy () {
    state.title = String
    state.password = String
    state.description = String
    state.design = Object
    state.images = Array
    state.stacks = Array
    state.imageSets = Array
    state.instructions = String
  },
  // meta data
  updateStudyTitle (state, studyTitle) {
    state.title = studyTitle
  },
  updateStudyPassword (state, studyPassword) {
    state.password = studyPassword
  },
  updateStudyDesc (state, studyDesc) {
    state.description = studyDesc
  },
  // design
  instructions (state, instructions) {
    state.design.instructions = instructions
  },
  buttonLabels (state, buttonLabel) {
    state.design.button_labels = buttonLabel
  },
  backgroundColor (state, backgroundColor) {
    state.design.background_color = backgroundColor
  },
  textColor (state, textColor) {
    state.design.text_color = textColor
  },
  viewerWidth (state, viewerWidth) {
    state.design.img_width = viewerWidth
  },
  viewerWidthAuto (state, bool) {
    state.design.img_width_auto = bool
  },
  viewerHeight (state, viewerHeight) {
    state.design.img_height = viewerHeight
  },
  viewerHeightAuto (state, bool) {
    state.design.img_height_auto = bool
  },
  roiNumb (state, roiNumb) {
    state.design.numb_rois = roiNumb
  },
  viewerMetainfo (state, viewerMetainfo) {
    state.design.show_viewport_info = viewerMetainfo
  },
  transitionTime (state, transitionTime) {
    state.design.transition_time = transitionTime
  },
  order (state, order) {
    state.design.randomize_order = order
  },
  // scales
  scales (state, scales) {
    state.design.scales = scales
  },
  scaleText (state, payload) {
    state.design.scales[payload.index].text = payload.text
  },
  scaleMin (state, payload) {
    state.design.scales[payload.index].min = payload.min
    var labels = []
    for (let i = state.design.scales[payload.index].min; i <= state.design.scales[payload.index].max; i++) {
      labels.push(i)
    }
    state.design.scales[payload.index].labels = labels
  },
  scaleMax (state, payload) {
    state.design.scales[payload.index].max = payload.max
    var labels = []
    for (let i = state.design.scales[payload.index].min; i <= state.design.scales[payload.index].max; i++) {
      labels.push(i)
    }
    state.design.scales[payload.index].labels = labels
  },
  scaleLabel (state, payload) {
    state.design.scales[payload.index].labels[[payload.labelIndex]] = payload.label
  },
  addScale (state, payload) {
    state.design.scales.push(payload)
  },
  delScale (state, payload) {
    state.design.scales.splice(payload.index)
  },
  // tools available and tool settings
  tools (state, tools) {
    state.design.tools = tools
  },
  toolSettings (state, payload) {
    var tool = state.design.tools.find(tool => tool.cs_name === payload.csName)
    if (!tool) {
      tool = { cs_name: payload.csName, key_binding: null, settings: {} }
      state.design.tools.push(tool)
    }
    tool.settings[payload.propName] = payload.value
    if (payload.propName === 'maxNumber') {
      tool.settings.labels = []
      for (let i = 1; i <= payload.value; i++) {
        tool.settings.labels.push(i)
      }
    }
  },
  toolLabel (state, payload) {
    var tool = state.design.tools.find(tool => tool.cs_name === payload.csName)
    tool.settings.labels[payload.labelIndex] = payload.value
  },
  viewerNumber (state, numbViewer) {
    state.design.numb_img = numbViewer
  },
  refviewerNumber (state, refnumbViewer) {
    state.design.numb_refimg = refnumbViewer
  },
  viewerLayoutCols (state, colNumb) {
    state.design.img_per_row = colNumb
  },
  // imgsets
  addImgset (state, imgset) {
    state.imageSets.splice(imgset.position, 0, imgset)
    state.imageSets.forEach((set, index) => {
      set.position = index
    })
  },
  imgsetDisplayed (state, imgset) {
    state.imgsetDisplayed = imgset
  },
  createImgsetsAuto (state, imgsetConfig) {
    const viewerNumber = state.design.numb_img
    const numberImgsets = Object.keys(state.stacks).length / viewerNumber
    const imgsetStartPosition = state.imageSets.length
    for (var imgsetIndex = 0; imgsetIndex < numberImgsets; imgsetIndex++) {
      var imgset = {
        imageStacks: [],
        position: imgsetStartPosition + imgsetIndex
      }
      for (var i = 0; i < viewerNumber; i++) {
        var stackIndex = imgsetIndex * viewerNumber + i
        var stack = {
          divId: i,
          csStack: state.stacks[stackIndex].cs_stack,
          name: '',
          segData: '',
          toolState: null,
          viewport: null
        }
        imgset.imageStacks.push(stack)
      }
      state.imageSets.push(imgset)
    }
  },
  deleteAllImgsets (state) {
    state.imageSets = []
    state.imgsetDisplayed = undefined
  },
  deleteStacks (state, stacks) {
    stacks.forEach((stackDeleted) => {
      const index = state.stacks.findIndex(stack => stack === stackDeleted)
      state.stacks.splice(index, 1)
    })
  },
  addStack (state, stack) {
    state.stacks.push(stack)
  }
}

const actions = {
  createNewStudy ({ commit }) {
    createStudy()
      .then(response => {
        const study = response.data.study
        commit('openStudy', study)
        store.commit('studies/addStudy', study)
        const route = '/study-management/' + study.id + '/metainfos'
        router.push(route)
      })
      .catch(error => {
        console.log(error)
      })
      .finally(() => {})
  },
  deleteSelectedFiles ({ commit }, payload) {
    deleteFiles(payload.studyId, payload.files).then(() => {
      commit('deleteStacks', payload.files)
    })
  },
  // imgsets
  addImgset ({ commit }, payload) {
    createImgset(payload.studyId, payload.imgset)
      .then(response => {
        commit('addImgset', response.data.imgset)
        commit('imgsetDisplayed', response.data.imgset)
      })
  },
  deleteAllImgsets ({ commit }, studyId) {
    deleteImgsets(studyId)
      .then(response => {
        commit('deleteAllImgsets')
      })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
