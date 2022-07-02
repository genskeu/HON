import { createStore } from 'vuex'
import openStudy from './modules/openStudy'
import cornerstoneViewers from './modules/cornerstoneViewers'

export default createStore({
  modules: {
    openStudy: openStudy,
    cornerstoneViewers: cornerstoneViewers
  }
})
