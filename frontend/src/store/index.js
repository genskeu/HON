import { createStore } from 'vuex'
import currentStudy from './modules/currentStudy'
import imageViewers from './modules/imageViewers'
import auth from './modules/auth'
import studies from './modules/studies'
import users from './modules/users'
import loadingState from './modules/loadingState'
import studyInput from './modules/studyInput'

export default createStore({
  modules: {
    studies: studies,
    currentStudy: currentStudy,
    studyInput: studyInput,
    imageViewers: imageViewers,
    auth: auth,
    loadingState: loadingState,
    users: users
  }
})
