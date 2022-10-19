import { createStore } from 'vuex'
import currentStudy from './modules/currentStudy'
import imageViewers from './modules/imageViewers'
import auth from './modules/auth'
import studies from './modules/studies'
import loadingState from './modules/loadingState'

export default createStore({
  modules: {
    studies: studies,
    currentStudy: currentStudy,
    imageViewers: imageViewers,
    auth: auth,
    loadingState: loadingState
  }
})
