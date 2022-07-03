import { createStore } from 'vuex'
import openStudy from './modules/openStudy'
import imageViewers from './modules/imageViewers'

export default createStore({
  modules: {
    openStudy: openStudy,
    imageViewers: imageViewers
  }
})
