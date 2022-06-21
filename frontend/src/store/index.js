import { createStore } from 'vuex'

export default createStore({
  state: {
    open_study: undefined
  },
  getters: {
    // meta data
    studyTitle (state) {
      return state.open_study.title
    },
    studyPassword (state) {
      return state.open_study.title
    },
    studyDescription (state) {
      return state.open_study.title
    },
    // design data
    viewerNumb (state) {
      return Number(state.open_study.design.numb_img)
    },
    viewerLayoutCols (state) {
      return Number(state.open_study.design.layout_img_cols)
    },
    viewerLayoutRows (state) {
      return Number(state.open_study.design.layout_img_rows)
    },
    refviewerNumb (state) {
      return Number(state.open_study.design.numb_refimg)
    },
    instructions (state) {
      return state.open_study.design.instructions
    },
    buttonLabels (state) {
      return state.open_study.design.button_labels
    },
    backgroundColor (state) {
      return state.open_study.design.background_color
    },
    textColor (state) {
      return state.open_study.design.text_color
    },
    viewerWidth (state) {
      return Number(state.open_study.design.img_width)
    },
    viewerHeight (state) {
      return Number(state.open_study.design.img_height)
    },
    roiNumb (state) {
      return Number(state.open_study.design.numb_rois)
    },
    viewerMetainfo (state) {
      return state.open_study.design.show_viewport_info
    },
    transitionTime (state) {
      return Number(state.open_study.design.transition_time)
    },
    order (state) {
      return state.open_study.design.randomize_order
    },
    scales (state) {
      return state.open_study.design.scales
    },
    tools (state) {
      return state.open_study.design.tools
    }
  },
  mutations: {
    addStudy (state, study) {
      state.studies.push(study)
    },
    openStudy (state, study) {
      state.open_study = study
    },
    closeStudy () {
      this.state.open_study = undefined
    },
    // meta data
    updateStudyTitle (state, studyTitle) {
      state.open_study.title = studyTitle
    },
    updateStudyDesc (state, studyDesc) {
      state.open_study.description = studyDesc
    },
    // design
    instructions (state, instructions) {
      state.open_study.design.instructions = instructions
    },
    buttonLabels (state, buttonLabel) {
      state.open_study.design.button_labels = buttonLabel
    },
    backgroundColor (state, backgroundColor) {
      state.open_study.design.background_color = backgroundColor
    },
    textColor (state, textColor) {
      state.open_study.design.text_color = textColor
    },
    viewerWidth (state, viewerWidth) {
      state.open_study.design.img_width = viewerWidth
    },
    viewerHeight (state, viewerHeight) {
      state.open_study.design.img_height = viewerHeight
    },
    roiNumb (state, roiNumb) {
      state.open_study.design.numb_rois = roiNumb
    },
    viewerMetainfo (state, viewerMetainfo) {
      state.open_study.design.show_viewport_info = viewerMetainfo
    },
    transitionTime (state, transitionTime) {
      state.open_study.design.transition_time = transitionTime
    },
    order (state, order) {
      state.open_study.design.randomize_order = order
    },
    scales (state, scales) {
      state.open_study.design.scales = scales
    },
    tools (state, tools) {
      state.open_study.design.tools = tools
    },
    viewerNumber (state, numbViewer) {
      state.open_study.design.numb_img = numbViewer
    },
    refviewerNumber (state, refnumbViewer) {
      state.open_study.design.numb_refimg = refnumbViewer
    },
    viewerLayoutRows (state, rowNumb) {
      state.open_study.design.layout_img_rows = rowNumb
    },
    viewerLayoutCols (state, colNumb) {
      state.open_study.design.layout_img_cols = colNumb
    }
  },
  actions: {
  },
  modules: {
  }
})
