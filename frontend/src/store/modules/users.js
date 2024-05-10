/* fetchUser, createUser, updateUser,  */
import { fetchUser, fetchUsers, updateUser, deleteUser } from '@/api'
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
  updUser ( {commit, state }, userId ) {
    store.commit('loadingState/startLoading', { title: 'Updating User' })
    updateUser(userId, state.currentUser)
    .then(() => {
      commit('updCurrentUser', userId, state.currentUser)
      commit('updUser', state.currentUser)
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
  },
  setUser ({ commit }, userId) {
    store.commit('loadingState/startLoading', { title: 'Loading User' })
    fetchUser(userId)
      .then((response) => {
        var user = response.data.user
        user["password"] = ""
        commit('setUser', response.data.user)
        store.commit('loadingState/finishLoading')
      })
      .catch((response) => {
        store.commit('loadingState/errorOccured', { errorData: response })
      })
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
  },
  setUser (state, user) {
    state.currentUser = user
  },
  updCurrentUser (state, user) {
    for (const key in user) {
      state.currentUser[key] = user[key]
    }
  },
  updUser (state, user) {
    const index = state.users.findIndex(u => u.id === user.id)
    state.users.splice(index, 1, user)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
