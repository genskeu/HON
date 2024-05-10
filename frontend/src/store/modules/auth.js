import { authService } from '@/api'
import router from '@/router'
const user = JSON.parse(localStorage.getItem('user'))

const state = user
  ? { status: { loggedIn: true }, user, errorLogin: null, errorRegister: null }
  : { status: { loggedIn: false }, user: null, errorLogin: null, errorRegister: null }

const getters = {
  user: state => state.user,
  errorLogin: state => state.errorLogin,
  errorRegister: state => state.errorRegister
}

const actions = {
  login ({ commit }, user) {
    authService.login(user)
      .then(response => {
        if (response.data.accessToken) {
          commit('loginSuccess', response.data)
          if (response.data.role === 'study_participant') {
            router.push('/study/login')
          } else if (response.data.role === 'study_admin') {
            router.push('/study-management/study-overview')
          } else if (response.data.role === 'user_admin') {
            router.push('/user-management/user-overview')
          }
        }
      }).catch(error => {
        commit('loginFailure', error.response)
      })
  },
  logout ({ commit, dispatch }) {
    authService.logout()
      .then(() => {
        dispatch('currentStudy/closeStudy', null, { root: true })
        dispatch('imageViewers/reset', null, { root: true })
        dispatch('studies/reset', null, { root: true })
        commit('logout')
        router.push('/login')
      }).catch(error => {
        console.log(error.response)
      })
  },
  register ({ commit }, user) {
    authService.register(user)
      .then(() => {
        commit('registerSuccess')
        router.push('/login')
      })
      .catch(error => {
        commit('registerFailure', error.response)
      })
  }
}

const mutations = {
  loginSuccess (state, user) {
    localStorage.setItem('user', JSON.stringify(user))
    state.status.loggedIn = true
    state.user = user
    state.errorLogin = null
  },
  loginFailure (state, error) {
    state.status.loggedIn = false
    state.user = null
    state.errorLogin = error
  },
  logout (state) {
    localStorage.removeItem('user')
    state.status.loggedIn = false
    state.user = null
    state.error = null
  },
  registerSuccess (state) {
    state.status.loggedIn = false
    state.errorRegister = null
    state.errorLogin = null
  },
  registerFailure (state, error) {
    state.status.loggedIn = false
    state.errorRegister = error
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
