// api/index.js
import axios from 'axios'
import { Modal } from 'bootstrap'
import router from '@/router'
import store from '@/store'

const API_URL = 'http://localhost:5000'

export function fetchStudies () {
  return axios.get(`${API_URL}/studies`, { headers: authHeader() })
}

export function fetchStudy (studyId) {
  return axios.get(`${API_URL}/study/${studyId}`, { headers: authHeader() })
}

export function createStudy (payload = {}) {
  return axios.post(`${API_URL}/study`, payload, { headers: authHeader() })
}

export function updateStudy (studyId, payload) {
  return axios.put(`${API_URL}/study/${studyId}`, payload, { headers: authHeader() })
}

export function delStudy (studyId, loadingScreenComponent) {
  loadingScreenComponent.$data.error = false
  loadingScreenComponent.$data.errorTitle = ''
  loadingScreenComponent.$data.errorMsg = ''
  loadingScreenComponent.$data.loadingTitle = 'Deleting Study. Please wait...'
  loadingScreenComponent.$data.loading = true
  const loadingModal = new Modal(loadingScreenComponent.$el, { fade: true })
  loadingModal.show()
  return axios.delete(`${API_URL}/study/${studyId}`, { headers: authHeader() })
    .then(response => {
      loadingScreenComponent.$data.loadingTitle = 'Deletion successful.'
      loadingScreenComponent.$data.loading = false
      setTimeout(function () {
        loadingModal.hide()
      }, 1000)
    })
    .catch(error => {
      loadingScreenComponent.$data.loading = false
      loadingScreenComponent.$data.loadingTitle = ''
      loadingScreenComponent.$data.error = true
      loadingScreenComponent.$data.errorTitle = 'Deleting Study...'
      loadingScreenComponent.$data.errorMsg = error
    })
    .finally(() => {
    })
}

export function updateStudyDesign (studyId, payload) {
  return axios.put(`${API_URL}/study/design/${studyId}`, payload, { headers: authHeader() })
}

export function uploadFiles (studyId, payload, config) {
  config.headers = authHeader()
  return axios.post(`${API_URL}/upload_files/${studyId}`, payload, config)
}

export function deleteFiles (studyId, payload) {
  return axios.delete(`${API_URL}/delete_files/${studyId}`, { data: payload, headers: authHeader() })
}

export function getResults (studyId) {
  return axios
    .get(`${API_URL}/results/${studyId}`, { headers: authHeader() })
    .then(() => { window.location = `${API_URL}/results/${studyId}/download` })
    .catch(() => {})
    .finally(() => {})
}

export function getResultsCurrentUser (studyId) {
  return axios
    .get(`${API_URL}/results/current_user/${studyId}`, { headers: authHeader() })
}

export function createImgset (studyId, payload) {
  return axios.post(`${API_URL}/study/imgset/${studyId}`, payload, { headers: authHeader() })
}

export function deleteImgsets (studyId) {
  return axios.delete(`${API_URL}/study/imgsets/${studyId}`, { headers: authHeader() })
}

export function saveResultDb (studyId, payload) {
  return axios.post(`${API_URL}/study/result/${studyId}`, payload, { headers: authHeader() })
}

export function deleteResultUserDb (studyId, userId) {
  return axios.delete(`${API_URL}/result/${studyId}/${userId}`, { headers: authHeader() })
}

class AuthService {
  login (user) {
    return axios
      .post(`${API_URL}/auth/login`, {
        username: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data.accessToken) {
          localStorage.setItem('user', JSON.stringify(response.data))
        }
        return response.data
      }).catch(error => console.log(error))
  }

  logout () {
    localStorage.removeItem('user')
  }

  register (user) {
    return axios.post(`${API_URL}/auth/register`, {
      username: user.username,
      password: user.password
    })
  }
}

var authService = new AuthService()
export { authService }

// adjust for flask jwt?
function authHeader () {
  const user = JSON.parse(localStorage.getItem('user'))
  if (user && user.accessToken) {
    return { Authorization: 'Bearer ' + user.accessToken }
  } else {
    return {}
  }
}

axios.interceptors.response.use(
  response => {
    return response
  },
  function (error) {
    if (
      error.response.status === 401
    ) {
      store.dispatch('auth/logout')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)
