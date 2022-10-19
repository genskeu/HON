import router from '@/router'
import { createStudy, updateStudy, deleteFiles, createImgset, createImgsets, deleteImgsets, saveResultDb, getResultsCurrentUser, deleteResultUserDb, fetchStudy, studyLoginParticipant } from '@/api'
import store from '@/store'
import { tools } from '@/store/modules/currentStudy/tools'

// import cornerstoneTools from 'cornerstone-tools'

const state = {
  id: Number,
  title: String,
  password: String,
  description: String,
  design: Object,
  images: Array,
  stacks: Array,
  imageSets: [],
  instructions: String,
  userStudyProgress: Array,
  imgsetDisplayed: undefined,
  resultsCurrentUser: [],
  loadingState: {
    isLoading: false,
    title: '',
    errorOccured: false,
    errorMsg: ''
  }
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
  scalesInput (state) {
    var scalesInput = {}
    state.design.scales.forEach(scale => {
      console.log(scale)
      if (scalesInput[scale.text] === undefined) {
        scalesInput[scale.text] = {
          values: [],
          uuids: []
        }
      }
      scalesInput[scale.text].values.push(scale.input)
      scalesInput[scale.text].uuids.push(scale.uuid)
    })
    return scalesInput
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
  scaleInput: (state) => (index) => {
    return state.design.scales[index].input
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
    return state.userStudyProgress
  },
  resultsCurrentUser (state) {
    return state.resultsCurrentUser
  },
  loadingState (state) {
    return state.loadingState
  }
}

// helper functions for getters of tool states
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
    state.id = study.id
    state.title = study.title
    state.password = ''
    state.description = study.description
    state.design = study.design
    state.images = study.images
    state.stacks = study.stacks
    state.imageSets = study.imgsets
    state.instructions = study.instructions
    state.userStudyProgress = study.user_study_progress
    state.resultsCurrentUser = []
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
    state.design.scales[payload.index].labels[payload.labelIndex] = payload.label
  },
  scaleInput (state, payload) {
    state.design.scales[payload.index].input = payload.input
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
  },
  addResultCurrentUser (state, result) {
    state.resultsCurrentUser.push(result)
  },
  addResultsCurrentUser (state, results) {
    state.resultsCurrentUser = results
  },
  userStudyProgress (state, userStudyProgress) {
    state.userStudyProgress = userStudyProgress
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

const actions = {
  openStudy (context, id) {
    store.commit('loadingState/startLoading', { title: 'Opening Study' })
    fetchStudy(id)
      .then((response) => {
        const data = response.data
        context.commit('openStudy', data.study)
        context.dispatch('resultsCurrentUser')
        const viewerNumber = context.getters.viewerNumb
        const refviewerNumber = context.getters.refviewerNumb
        for (let i = 0; i < viewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'viewers' })
        }
        for (let i = 0; i < refviewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'refviewers' })
        }
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  closeStudy (context) {
    store.commit('loadingState/startLoading', { title: 'Close Study' })
    context.commit('closeStudy')
    store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
    router.push('/study-management/study-overview')
  },
  studyLogin (context, payload) {
    studyLoginParticipant(payload)
      .then((response) => {
        const study = response.data.study
        context.commit('openStudy', study)
        const results = response.data.results
        context.commit('addResultsCurrentUser', results)
        const viewerNumber = context.getters.viewerNumb
        const refviewerNumber = context.getters.refviewerNumb
        for (let i = 0; i < viewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'viewers' })
        }
        for (let i = 0; i < refviewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'refviewers' })
        }
      })
  },
  createNewStudy ({ commit }) {
    store.commit('loadingState/startLoading', { title: 'Creating new study' })
    createStudy()
      .then(response => {
        const study = response.data.study
        commit('openStudy', study)
        store.commit('studies/addStudy', study)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
        const route = '/study-management/' + study.id + '/metainfos'
        setTimeout(function () {
          router.push(route)
        }, 500)
      })
      .catch(error => {
        console.log(error)
      })
      .finally(() => {})
  },
  deleteSelectedFiles ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Deleting Files' })
    deleteFiles(payload.studyId, payload.files)
      .then(() => {
        commit('deleteStacks', payload.files)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  updateStudyMetainfos ({ commit }, { studyId, data }) {
    store.commit('loadingState/startLoading', { title: 'Saving updated Metainfos' })
    updateStudy(studyId, data)
      .then(() => {
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  // imgsets
  addImgset ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Creating Imageset' })
    createImgset(payload.studyId, payload.imgset)
      .then(response => {
        commit('addImgset', response.data.imgset)
        commit('imgsetDisplayed', response.data.imgset)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  // imgsets
  createImgsetsAuto ({ state, commit }, studyId) {
    store.commit('loadingState/startLoading', { title: 'Creating Imagesets' })
    var imgsets = []
    const viewerNumber = state.design.numb_img
    const numberImgsets = state.stacks.length / viewerNumber
    const imgsetStartPosition = state.imageSets.length
    for (var imgsetIndex = 0; imgsetIndex < numberImgsets; imgsetIndex++) {
      var imgset = {
        stacks: [],
        position: imgsetStartPosition + imgsetIndex
      }
      for (var i = 0; i < viewerNumber; i++) {
        var stackIndex = imgsetIndex * viewerNumber + i
        const imageIds = state.stacks[stackIndex].cs_stack.imageIds
        var stack = {
          div_id: 'dicom_img_' + i,
          image_names: imageIds.map((id) => id.split('/').pop()),
          base_url: imageIds[0].substring(0, imageIds[0].lastIndexOf('/')).replace('wadouri:', '') + '/',
          name: state.stacks[stackIndex].name,
          segmentation_data: '',
          tool_state: imageIds.map((id) => null),
          viewport: null
        }
        imgset.stacks.push(stack)
      }
      imgsets.push(imgset)
    }
    createImgsets(studyId, imgsets)
      .then(response => {
        response.data.imgsets.forEach(imgset => {
          commit('addImgset', imgset)
          commit('imgsetDisplayed', imgset)
          store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
        })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  deleteAllImgsets ({ commit }, studyId) {
    store.commit('loadingState/startLoading', { title: 'Deleting all Imagesets' })
    deleteImgsets(studyId)
      .then(response => {
        commit('deleteAllImgsets')
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  saveResult ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Saving Results' })
    saveResultDb(state.id, payload)
      .then((response) => {
        const result = response.data.result
        commit('addResultCurrentUser', result)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
      })
  },
  resultsCurrentUser ({ commit }) {
    getResultsCurrentUser(state.id).then((response) => {
      const results = response.data.results
      commit('addResultsCurrentUser', results)
    })
  },
  delResultsUser ({ commit }, userId) {
    store.commit('loadingState/startLoading', { title: 'Deleting Results' })
    deleteResultUserDb(state.id, userId)
      .then((response) => {
        const userStudyProgress = response.data.user_study_progress
        commit('userStudyProgress', userStudyProgress)
        store.commit('loadingState/finishLoading', { errorOccured: false, errorMsg: '' })
      })
      .catch((response) => {
        store.commit('loadingState/finishLoading', { errorOccured: true, errorMsg: response.data.error })
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
