// api/index.js
import axios from 'axios'
// import router from '@/router'

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

export function delStudy (studyId) {
  return axios.delete(`${API_URL}/study/${studyId}`, { headers: authHeader() })
}

export function uploadFiles (studyId, payload, config) {
  config.headers = authHeader()
  return axios.post(`${API_URL}/upload_files/${studyId}`, payload, config)
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
