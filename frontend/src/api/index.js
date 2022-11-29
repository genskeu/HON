// api/index.js
import axios from 'axios'
// import router from '@/router'
// import store from '@/store'
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader'

// production backend reached via nginx proxy (nginx.conf)
// development backend reached via vue-cli-service dev server proxy (vue.config.js)
const API_URL = 'flask-api'

//
cornerstoneWADOImageLoader.configure({
  beforeSend: function (xhr) {
    // debugger // eslint-disable-line no-debugger
    const user = JSON.parse(localStorage.getItem('user'))
    xhr.setRequestHeader('Authorization', 'Bearer ' + user.accessToken)
  }
})

export function fetchUsers () {
  return axios.get(`${API_URL}/users`, { headers: authHeader() })
}

export function fetchUser (userId) {
  return axios.get(`${API_URL}/user/${userId}`, { headers: authHeader() })
}

export function createUser (payload = {}) {
  return axios.post(`${API_URL}/user`, payload, { headers: authHeader() })
}

export function updateUser (userId, payload) {
  return axios.put(`${API_URL}/user/${userId}`, payload, { headers: authHeader() })
}

export function delelteUser (userId) {
  return axios.delete(`${API_URL}/user/${userId}`, { headers: authHeader() })
}

export function fetchStudies () {
  return axios.get(`${API_URL}/studies`, { headers: authHeader() })
}

export function fetchStudy (studyId) {
  return axios.get(`${API_URL}/study/${studyId}`, { headers: authHeader() })
}

export function studyLoginParticipant (payload) {
  return axios.post(`${API_URL}/study/login`, payload, { headers: authHeader() })
}

export function createStudy (payload = {}) {
  return axios.post(`${API_URL}/study`, payload, { headers: authHeader() })
}

export function updateStudy (studyId, payload) {
  return axios.put(`${API_URL}/study/${studyId}`, payload, { headers: authHeader() })
}

export function delStudy (studyId) {
  return axios.delete(`${API_URL}/study/${studyId}`, { headers: authHeader() })
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
export function createImgset (studyId, payload) {
  return axios.post(`${API_URL}/study/imgset/${studyId}`, payload, { headers: authHeader() })
}

export function updateImgset (studyId, position, payload) {
  return axios.put(`${API_URL}/study/imgset/${studyId}/${position}`, payload, { headers: authHeader() })
}

export function deleteImgset (studyId, position) {
  return axios.delete(`${API_URL}/study/imgset/${studyId}/${position}`, { headers: authHeader() })
}

export function createImgsets (studyId, payload) {
  return axios.post(`${API_URL}/study/imgsets/${studyId}`, payload, { headers: authHeader() })
}

export function updateImgsets (studyId, payload) {
  return axios.put(`${API_URL}/study/imgsets/${studyId}`, payload, { headers: authHeader() })
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
  }

  logout () {
    return axios
      .post(`${API_URL}/auth/logout`)
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

function authHeader () {
  const user = JSON.parse(localStorage.getItem('user'))
  if (user && user.accessToken) {
    return { Authorization: 'Bearer ' + user.accessToken }
  } else {
    return {}
  }
}

// to do use inceptors for jwt refresh
// axios.interceptors.response.use(
//   response => {
//     return response
//   },
//   function (error) {
//     console.log(error)
//     if (
//       error.response.status === 401
//     ) {
//       store.dispatch('auth/logout')
//       router.push('/login')
//     }
//     return Promise.reject(error)
//   }
// )
