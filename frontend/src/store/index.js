import { createStore } from 'vuex'
import openStudy from './modules/openStudy'
import imageViewers from './modules/imageViewers'
import auth from './modules/auth'
import studies from './modules/studies'

export default createStore({
  modules: {
    studies: studies,
    openStudy: openStudy,
    imageViewers: imageViewers,
    auth
  }
})
