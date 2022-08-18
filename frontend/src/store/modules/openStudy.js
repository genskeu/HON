import axios from 'axios'
import router from '@/router'

const state = {
  title: String,
  password: String,
  description: String,
  design: Object,
  images: Array,
  imageSets: Array,
  scales: Array,
  instructions: String,
  user_study_progress: Array
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
  // imgsets
  imgsets (state) {
    return state.imageSets
  },
  // design data
  viewerNumb (state) {
    return Number(state.design.numb_img)
  },
  viewerLayoutCols (state) {
    return Number(state.design.layout_img_cols)
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
  tools (state) {
    return state.design.tools
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

const mutations = {
  openStudy (state, study) {
    state.title = study.title
    state.password = ''
    state.description = study.description
    state.design = study.design
    state.images = study.images
    state.stacks = study.cs_stacks
    state.imageSets = study.imgsets
    state.scales = study.scales
    state.instructions = study.instructions
    state.user_study_progress = study.user_study_progress
  },
  closeStudy () {
    state.title = String
    state.password = String
    state.description = String
    state.design = Object
    state.images = Array
    state.imageSets = Array
    state.scales = Array
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
  },
  scaleMax (state, payload) {
    state.design.scales[payload.index].max = payload.max
  },
  addScale (state, payload) {
    state.design.scales.push(payload)
  },
  delScale (state, payload) {
    state.design.scales.splice(payload.index)
  },
  tools (state, tools) {
    state.design.tools = tools
  },
  viewerNumber (state, numbViewer) {
    state.design.numb_img = numbViewer
  },
  refviewerNumber (state, refnumbViewer) {
    state.design.numb_refimg = refnumbViewer
  },
  viewerLayoutRows (state, rowNumb) {
    state.design.layout_img_rows = rowNumb
  },
  viewerLayoutCols (state, colNumb) {
    state.design.layout_img_cols = colNumb
  }
  // imgsets
}

const actions = {
  createStudy ({ commit }) {
    axios
      .post('http://localhost:5000/study')
      .then(response => {
        const study = response.data.study
        commit('openStudy', study)
        const route = '/study-management/' + study.id + '/metainfos'
        router.push(route)
      })
      .catch(error => {
        console.log(error)
      })
      .then(() => {})
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
