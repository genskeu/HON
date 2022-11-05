/* fetchUser, createUser, updateUser,  */
import { fetchUsers, deleteUser } from '@/api'
import store from '@/store'

const getDefaultState = () => {
  return {
    users: [],
    currentUser: {
      name: null,
      password: null,
      access_level: null
    }
  }
}

const state = getDefaultState()

const getters = {
  users: state => state.users,
  currentUser: state => state.currentUser
}

const actions = {
  initUsers ({ commit }) {
    store.commit('loadingState/startLoading', { title: 'Loading User Overview' })
    fetchUsers()
      .then((response) => {
        const users = response.data.users
        commit('initUsers', users)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  delUser ({ commit }, userId) {
    store.commit('loadingState/startLoading', { title: 'Deleting User' })
    deleteUser(userId)
      .then(() => {
        commit('delUser', userId)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
  },
  reset ({ commit }) {
    commit('reset')
  }
}

const mutations = {
  reset (state) {
    Object.assign(state, getDefaultState())
  },
  initUsers (state, users) {
    state.users = users
  },
  adduser (state, user) {
    state.users.push(user)
  },
  deleteStudy (state, userId) {
    const index = state.users.findIndex(user => user.id === userId)
    state.users.splice(index, 1)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
