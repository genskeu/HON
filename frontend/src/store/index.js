import { createStore } from 'vuex'
import openStudy from './modules/openStudy'
import imageViewers from './modules/imageViewers'
import auth from './modules/auth'

export default createStore({
  modules: {
    openStudy: openStudy,
    imageViewers: imageViewers,
    auth
  }
})
