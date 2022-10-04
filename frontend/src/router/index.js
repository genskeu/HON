import { createRouter, createWebHashHistory } from 'vue-router'
import StudyManagement from '@/views/studyAdmin/StudyManagement.vue'
import StudyOverview from '@/views/studyAdmin/StudyOverview.vue'
import StudyMetainfo from '@/views/studyAdmin/studyManagement/StudyMetainfo'
import FileManagement from '@/views/studyAdmin/studyManagement/FileManagement'
import StudyDesign from '@/views/studyAdmin/studyManagement/StudyDesign'
import ResultsOverview from '@/views/studyAdmin/studyManagement/ResultsOverview'
import StudyParticipation from '@/views/studyParticipant/participation.vue'
import UserOverview from '@/views/userAdmin/userOverview.vue'
import UserProfile from '@/views/userAdmin/userProfile.vue'
import Tutorials from '@/views/tutorials.vue'
import Login from '@/views/login.vue'
import studyLogin from '@/views/studyParticipant/studyLogin.vue'

import store from '@/store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    meta: { requireAuth: true }
  },
  {
    path: '/user-overview',
    name: 'UserOverview',
    component: UserOverview,
    meta: { requireAuth: true, requireUserAdmin: true }
  },
  {
    path: '/user-profile/:id',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requireAuth: true }
  },
  {
    path: '/tutorials',
    name: 'Tutorials',
    component: Tutorials,
    meta: { requireAuth: true }
  },
  {
    path: '/study-overview',
    name: 'StudyOverview',
    component: StudyOverview,
    meta: { requireAuth: true, requireStudyAdmin: true }
  },
  {
    path: '/study-management/:id',
    name: 'StudyManagement',
    component: StudyManagement,
    meta: { requireAuth: true, requireStudyAdmin: true },
    children: [
      {
        path: 'metainfos',
        name: 'StudyMetainfos',
        components: {
          helper: StudyMetainfo
        }
      },
      {
        path: 'files',
        name: 'StudyFiles',
        components: {
          helper: FileManagement
        }
      },
      {
        path: 'design',
        name: 'StudyDesign',
        components: {
          helper: StudyDesign
        }
      },
      {
        path: 'participation',
        name: 'StudyParticipation',
        components: {
          helper: StudyParticipation
        }
      },
      {
        path: 'results',
        name: 'StudyResults',
        components: {
          helper: ResultsOverview
        }
      }
    ]
  },
  {
    path: '/study-login',
    name: 'studyLogin',
    component: studyLogin,
    meta: { requireAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// check usertype and redirect accordingly
router.beforeEach(async (to, from) => {
  if (to.path === '/') {
    if (!store.state.auth.user) {
      router.push('/login')
    } else if (store.state.auth.user.role === 'study_participant') {
      router.push('/study-login')
    } else if (store.state.auth.user.role === 'study_admin') {
      router.push('/study-overview')
    } else if (store.state.auth.user.role === 'user_admin') {
      router.push('/user-overview')
    } else {
    }
  }
})

// prevent double login
router.beforeEach(async (to, from) => {
  if (to.name === 'Login' && store.state.auth.user) {
    if (store.state.auth.user.role === 'study_participant') {
      router.push('/study-login')
    } else if (store.state.auth.user.role === 'study_admin') {
      router.push('/study-overview')
    } else if (store.state.auth.user.role === 'user_admin') {
      router.push('/user-overview')
    } else {
    }
  }
})

// protect routes for logged in users
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (!localStorage.getItem('user')) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

// protect routes for user types
router.beforeEach((to, from, next) => {
  if (to.meta.requireStudyAdmin) {
    if (store.state.auth.user.role !== 'study_admin') {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireUserAdmin) {
    if (store.state.auth.user.role !== 'user_admin') {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireStudyParticipant) {
    if (store.state.auth.user.role !== 'study_participant') {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
