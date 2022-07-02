const state = {
  title: String,
  password: String,
  description: String,
  design: Object,
  images: Array,
  imageSets: Array,
  scales: Array,
  instructions: String
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
  instructions (state) {
    return state.design.instructions
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
  viewerWidth (state) {
    return Number(state.design.img_width)
  },
  viewerWidthAuto (state) {
    return state.design.img_width_auto
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
  scales (state) {
    return state.design.scales
  },
  tools (state) {
    return state.design.tools
  }
}

const mutations = {
  addStudy (state, study) {
    state.studies.push(study)
  },
  openStudy (state, study) {
    state.title = study.title
    state.password = study.title
    state.description = study.description
    state.design = study.design
    state.images = study.images
    state.imageSets = study.image_sets
    state.scales = study.scales
    state.instructions = study.instructions
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
  scales (state, scales) {
    state.design.scales = scales
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
