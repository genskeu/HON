import router from '@/router'
import {
  createStudy, updateStudy, fetchStudy, updateStudyDesign, deleteFiles,
  createImgset, updateImgset, deleteImgset,
  createImgsets, updateImgsets, deleteImgsets,
  saveResultDb, deleteResultUserDb,
  studyLoginParticipant
} from '@/api'
import store from '@/store'
import { tools } from '@/components/dicomViewer/tools'
import cornerstone from 'cornerstone-core'

// import cornerstoneTools from 'cornerstone-tools'

const getDefaultState = () => {
  return {
    id: Number,
    title: String,
    password: String,
    description: String,
    design: Object,
    images: [],
    stacks: [],
    imageSets: [],
    instructions: String,
    usersStudyProgress: [],
    imgsetDisplayed: null,
    resultsCurrentUser: [],
    scalesInput: []
  }
}

const state = getDefaultState()

// class Design {
//   constructor () {
//     this.element = null
//   }
// }

// class ScaleDesign {
//   constructor () {
//     this.element = null
//   }
// }

// class Tool {
//   constructor () {
//     this.element = null
//   }
// }

class ScaleInput {
  constructor (scaleName, scaleValue, scaleMin, scaleMax, uuidAnnoation = null) {
    this.name = scaleName
    this.value = scaleValue
    this.min = scaleMin
    this.max = scaleMax
    this.uuid = uuidAnnoation
  }
}

const getters = {
  // meta data
  id (state) {
    return state.id
  },
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
  scaleInput: (state) => (index) => {
    return state.scalesInput[index]
  },
  scalesInput (state) {
    return state.scalesInput
  },
  scalesInputDB (state) {
    // format for database
    // old: multiple values for one scaleInput possible (FROC, LROC)
    // new: each scaleInput has only one value and uuid
    var scalesInputDB = {}
    state.scalesInput.forEach((scale, index) => {
      // scale name + index = unique entry
      var scaleName = index + 1 + ' ' + scale.name
      scalesInputDB[scaleName] = {}
      scalesInputDB[scaleName].values = [scale.value]
      scalesInputDB[scaleName].uuids = [scale.uuid]
    })
    return scalesInputDB
  },
  // tools with settings (saved in db)
  tools (state) {
    return state.design.tools
  },
  toolSettings: (state) => (toolName) => {
    var tool = state.design.tools.find(tool => tool.cs_name === toolName)
    if (tool) {
      return tool.settings
    } else {
      return undefined
    }
  },
  synchronizeScroll (state) {
    var synched = false
    state.design.tools.forEach((tool) => {
      if (tool.cs_name.includes("Scroll")) {
        if (tool.settings) {
          synched = tool.settings.synched
        }
      }
    })
    return synched
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
  toolsMousekeysParticipant (state) {
    var toolsMousekeys = tools.toolsMousekeys
    return filterTools(toolsMousekeys, state.design.tools)
  },
  toolsMousewheelParticipant (state) {
    var toolsMousewheel = tools.toolsMousewheel
    return filterTools(toolsMousewheel, state.design.tools)
  },
  // stacks
  stacks (state) {
    return state.stacks
  },
  // results
  usersStudyProgress (state) {
    return state.usersStudyProgress
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
    var label = toolsAll[toolCsname].name
    if (!toolSetting) {
      toolsSettings[label] = { cs_name: toolCsname, key_binding: null, settings: {} }
    } else {
      toolsSettings[label] = toolSetting
    }
  })
  return toolsSettings
}

function filterTools (toolsAll, toolsSaved) {
  var toolsFiltered = {}
  Object.keys(toolsAll).forEach(toolType => {
    Object.keys(toolsAll[toolType]).forEach(toolCsname => {
      var toolSaved = toolsSaved.find(tool => tool.cs_name === toolCsname)
      if (toolSaved) {
        if (toolType in toolsFiltered) {
          toolsFiltered[toolType][toolCsname] = toolsAll[toolType][toolCsname]
        } else {
          toolsFiltered[toolType] = {}
          toolsFiltered[toolType][toolCsname] = toolsAll[toolType][toolCsname]
        }
      toolsFiltered[toolType][toolCsname]['settings'] = toolSaved.settings
      }
    })
  })
  return toolsFiltered
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
    state.usersStudyProgress = study.user_study_progress
    state.imgsetDisplayed = null
    state.resultsCurrentUser = study.results_current_user
    state.scalesInput = []    
  },
  closeStudy (state) {
    Object.assign(state, getDefaultState())
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
  addScale (state, payload) {
    state.design.scales.push(payload)
  },
  delScale (state, payload) {
    state.design.scales.splice(payload.index)
  },
  scaleInput (state, { index, scaleName, scaleValue, scaleMin, scaleMax}) {
    const scale = new ScaleInput(scaleName, scaleValue, scaleMin, scaleMax)
    state.scalesInput[index] = scale
  },
  updScaleInput (state, { index, scaleValue }) {
    state.scalesInput[index].value = scaleValue
    console.log(state.scalesInput[index])
  },
  resetScales (state) {
    var scalesDefault = []
    state.design.scales.forEach((scale) => {
      if (!scale.isRepeated) {
        scalesDefault.push(scale)
      }
    })
    Object.assign(state.design.scales, scalesDefault)
  },
  resetScalesInput (state) {
    state.scalesInput.forEach((scale) => {
      scale.value = null
      scale.uuid = null
    })
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
  updImgset (state, imgset) {
    state.imageSets[imgset.position] = imgset
  },
  delImgset (state, imgset) {
    state.imageSets.splice(imgset.position, 1)
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
  removeResultsCurrentUser (state) {
    state.resultsCurrentUser = []
  },
  userStudyProgress (state, userStudyProgressNew) {
    var userStudyProgressIndex = state.usersStudyProgress.findIndex(usp => usp.user_id === userStudyProgressNew.user_id)
    if (userStudyProgressIndex > -1) {
      state.usersStudyProgress[userStudyProgressIndex] = userStudyProgressNew
    } else {
      state.usersStudyProgress.push(userStudyProgressNew)
    }
  },
  usersStudyProgress (state, usersStudyProgress) {
    state.usersStudyProgress = usersStudyProgress
  },
}

const actions = {
  openStudy (context, {id, preLoadImages}) {
    store.commit('loadingState/startLoading', { title: 'Opening Study' })
    fetchStudy(id)
      .then((response) => {
        const data = response.data
        context.commit('openStudy', data.study)
        const viewerNumber = context.getters.viewerNumb
        const refviewerNumber = context.getters.refviewerNumb
        for (let i = 0; i < viewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'viewers' })
        }
        for (let i = 0; i < refviewerNumber; i++) {
          store.commit('imageViewers/initViewer', { viewertype: 'refviewers' })
        }
        if (preLoadImages) {
          loadAndCacheVolumes(data.study.stacks, 0)
            .then(() => {
              store.commit('loadingState/finishLoading')
            })
        } else {
          store.commit('loadingState/finishLoading')
        }
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  closeStudy (context) {
    // store.commit('loadingState/startLoading', { title: 'Close Study' })
    // store.commit('loadingState/finishLoading')
    router.push('/study-management/study-overview').then(() => {
      context.commit('closeStudy')
      store.commit('imageViewers/reset')
    })
  },
  logoutStudy (context) {
    context.commit('closeStudy')
    store.commit('imageViewers/reset')
    router.push({ name: 'StudyLogin' }).then(() => {
    })
  },
  // update study design
  updateDesign ({ state }, studyId) {
    store.commit('loadingState/startLoading', { title: 'Saving Design' })
    const design = state.design
    updateStudyDesign(studyId, design)
      .then(() => {
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  studyLogin (context, payload) {
    studyLoginParticipant(payload)
      .then((response) => {
        localStorage.setItem('user', JSON.stringify(response.data))
        const studyId = response.data.study_loggedin
        context.dispatch('openStudy', { id:studyId, preLoadImages:true } ).then(() => router.push(studyId + '/participation'))
      })
  },
  createNewStudy ({ commit }) {
    store.commit('loadingState/startLoading', { title: 'Creating new study' })
    createStudy()
      .then(response => {
        const study = response.data.study
        commit('openStudy', study)
        store.commit('studies/addStudy', study)
        store.commit('loadingState/finishLoading')
        const route = '/study-management/' + study.id + '/metainfos'
        setTimeout(function () {
          router.push(route)
        }, 500)
      })
      .catch(response => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
      .finally(() => {})
  },
  deleteSelectedFiles ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Deleting Files' })
    return deleteFiles(payload.studyId, payload.files)
      .then(() => {
        commit('deleteStacks', payload.files)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  updateStudyMetainfos (_ ,{ studyId, data } ) {
    store.commit('loadingState/startLoading', { title: 'Saving updated Metainfos' })
    updateStudy(studyId, data)
      .then(() => {
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  /* eslint-enable */
  // imgsets
  addImgset ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Creating Imageset' })
    createImgset(payload.studyId, payload.imgset)
      .then(response => {
        commit('addImgset', response.data.imgset)
        commit('imgsetDisplayed', response.data.imgset)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  updImgset ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'updating Imageset' })
    updateImgset(payload.studyId, payload.imgset.position, payload.imgset)
      .then(response => {
        commit('updImgset', response.data.imgset)
        commit('imgsetDisplayed', response.data.imgset)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  delImgset ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Deleting Imageset' })
    deleteImgset(payload.studyId, payload.imgset.position)
      .then(() => {
        commit('delImgset', payload.imgset)
        if(state.imageSets.length > 1){
          commit('imgsetDisplayed', state.imageSets[payload.imgset.position-1])
        } else {
          commit('imgsetDisplayed', null)
        }
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  createImgsetsAuto ({ state, commit }, { studyId, viewport, order, type, posPattern, negPattern }) {
    store.commit('loadingState/startLoading', { title: 'Creating Image-Sets' })
    const viewerNumber = state.design.numb_img
    const imgsetStartPosition = state.imageSets.length
    var imageStacks = state.stacks
    if (order == "random") {
      imageStacks = imageStacks.sort(() => Math.random() - 0.5)
    } 
    var imgsets = []
    if (type == 'standard') {
      imgsets = createStandartImgsets(viewerNumber, imgsetStartPosition, imageStacks, viewport)
    } else if (type == 'afc') {
      imgsets = createAfcImgsets(viewerNumber, imgsetStartPosition, imageStacks, viewport, posPattern, negPattern)
    } else {
      console.log('Error: unknown type of imgset')
    }
    createImgsets(studyId, imgsets)
      .then(response => {
        response.data.imgsets.forEach(imgset => {
          commit('addImgset', imgset)
          commit('imgsetDisplayed', imgset)
        })
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  updateAllImgsets ({ commit }, { studyId, viewport }) {
    store.commit('loadingState/startLoading', { title: 'Updating Image-Sets' })
    updateImgsets(studyId, viewport)
      .then(response => {
        commit('deleteAllImgsets')
        response.data.imgsets.forEach(imgset => {
          commit('addImgset', imgset)
          commit('imgsetDisplayed', imgset)
        })
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  deleteAllImgsets ({ commit }, studyId) {
    store.commit('loadingState/startLoading', { title: 'Deleting all Image-Sets' })
    deleteImgsets(studyId)
      .then(() => {
        commit('deleteAllImgsets')
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  saveResult ({ commit }, payload) {
    store.commit('loadingState/startLoading', { title: 'Saving Results' })
    saveResultDb(state.id, payload)
      .then((response) => {
        const result = response.data.result
        const usp = response.data.study_progress
        commit('addResultCurrentUser', result)
        commit('userStudyProgress', usp)
        commit('resetScales')
        commit('resetScalesInput')
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  delResultsUser ({ commit }, userId) {
    store.commit('loadingState/startLoading', { title: 'Deleting Results' })
    deleteResultUserDb(state.id, userId)
      .then((response) => {
        const usersStudyProgress = response.data.user_study_progress
        commit('usersStudyProgress', usersStudyProgress)
        commit('removeResultsCurrentUser')
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
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

  // imgsets
 function createStandartImgsets (viewerNumber, imgsetStartPosition, imageStacks, viewport) {
    const numberImgsets = state.stacks.length / viewerNumber
    var imgsets = []
    for (var imgsetIndex = 0; imgsetIndex < numberImgsets; imgsetIndex++) {
      var imgset = {
        stacks: [],
        position: imgsetStartPosition + imgsetIndex
      }
      for (var i = 0; i < viewerNumber; i++) {
        var stackIndex = imgsetIndex * viewerNumber + i
        if (stackIndex >= imageStacks.length) {
          continue
        }
        const imageIds = imageStacks[stackIndex].cs_stack.imageIds
        var stack = {
          stack_id: imageStacks[stackIndex].stack_id,
          div_id: 'dicom_img_' + i,
          name: imageStacks[stackIndex].name,
          segmentation_data: '',
          tool_state: imageIds.map(() => null),
          viewport: viewport
        }
        imgset.stacks.push(stack)
      }
      imgsets.push(imgset)
    }
    return imgsets
  }

  function createAfcImgsets (viewerNumber, imgsetStartPosition, imageStacks, viewport, pos_pattern, neg_pattern) {
    var imgsets = []
    const imgaeStacksPos = imageStacks.filter(stack => stack.name.split('_')[1] == (pos_pattern))
    const imgaeStacksNeg = imageStacks.filter(stack => stack.name.split('_')[1] == (neg_pattern))
    imgaeStacksPos.forEach((stack, index) => {
      var group = stack.name.split('_')[2]
      var imgaeStacksNegGroup = imgaeStacksNeg.filter(stack => stack.name.split('_')[2] == group)
      var imgset = {
        stacks: [],
        position: imgsetStartPosition + index
      }
      // pick viewernumber - 1 random negative stacks, without repitition
      imgaeStacksNegGroup.sort(() => Math.random() - 0.5)
      var stacksRaw = imgaeStacksNegGroup.slice(0, viewerNumber - 1)
      // add positive stack at random position
      var posStackIndex = Math.floor(Math.random() * viewerNumber)
      stacksRaw.splice(posStackIndex, 0, stack)

      stacksRaw.forEach((stackRaw, i) => {
        const imageIds = stackRaw.cs_stack.imageIds
        var stack = {
          stack_id: stackRaw.stack_id,
          div_id: 'dicom_img_' + i,
          name: stackRaw.name,
          segmentation_data: '',
          tool_state: imageIds.map(() => null),
          viewport: viewport
        }
        imgset.stacks.push(stack)
      })
      imgsets.push(imgset)
    })
    return imgsets
  }

  cornerstone.imageCache.setMaximumSizeBytes(4000000000)
  function loadAndCacheVolume(imageIds) {
    //console.log('loading image ' + index)
    var promisis = []
    imageIds.forEach((imageId) => {
      var promis = cornerstone.loadAndCacheImage(imageId)
      promisis.push(promis)
    })
    return Promise.all(promisis)
  }

  function loadAndCacheVolumes(stacks, index) {
    return new Promise((resolve) => {
      resolve(loadAndCacheVolume(stacks[index].cs_stack.imageIds, 0))
    }).then(() => {
      var percLoaded = (index+1)/stacks.length
      store.commit('loadingState/updLoading', { title: 'Loading Images ' + (percLoaded*100).toFixed(2) + '%'})
      if (index < stacks.length-1) {
        return loadAndCacheVolumes(stacks, index + 1)
      } else {
        return index
      } 
    })
  }