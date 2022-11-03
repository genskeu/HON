import { createRouter, createWebHashHistory } from 'vue-router'
import StudyManagement from '@/views/studyAdmin/StudyManagement.vue'
import StudyOverview from '@/views/studyAdmin/studyManagement/StudyOverview.vue'
import StudyMetainfo from '@/views/studyAdmin/studyManagement/StudyMetainfo'
import FileManagement from '@/views/studyAdmin/studyManagement/FileManagement'
import StudyDesign from '@/views/studyAdmin/studyManagement/StudyDesign'
import ResultsOverview from '@/views/studyAdmin/studyManagement/ResultsOverview'
import Participation from '@/views/studyParticipant/studyParticipation/participation.vue'
import UserOverview from '@/views/userAdmin/userOverview.vue'
import UserProfile from '@/views/userAdmin/userProfile.vue'
import Tutorials from '@/views/tutorials.vue'
import Login from '@/views/login.vue'
import studyParticipation from '@/views/studyParticipant/studyParticipation.vue'
import StudyLogin from '@/views/studyParticipant/studyParticipation/login.vue'

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
    path: '/study-management',
    name: 'StudyManagement',
    component: StudyManagement,
    meta: { requireAuth: true, requireStudyAdmin: true },
    children: [
      {
        path: 'study-overview',
        name: 'StudyOverview',
        components: {
          helper: StudyOverview
        }
      },
      {
        path: ':id/metainfos',
        name: 'StudyMetainfos',
        components: {
          helper: StudyMetainfo
        }
      },
      {
        path: ':id/files',
        name: 'StudyFiles',
        components: {
          helper: FileManagement
        }
      },
      {
        path: ':id/design',
        name: 'StudyDesign',
        components: {
          helper: StudyDesign
        }
      },
      {
        path: ':id/participation',
        name: 'StudyParticipationPreview',
        components: {
          helper: Participation
        }
      },
      {
        path: ':id/results',
        name: 'StudyResults',
        components: {
          helper: ResultsOverview
        }
      }
    ]
  },
  {
    path: '/study',
    name: 'studyParticipation',
    component: studyParticipation,
    meta: { requireAuth: true },
    children: [
      {
        path: 'login',
        name: 'StudyLogin',
        components: {
          helper: StudyLogin
        }
      },
      {
        path: ':id/participation',
        name: 'StudyParticipation',
        components: {
          helper: Participation
        }
      }
    ]
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
      router.push('/study/login')
    } else if (store.state.auth.user.role === 'study_admin') {
      router.push('/study-management/study-overview')
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
      router.push('/study/login')
    } else if (store.state.auth.user.role === 'study_admin') {
      router.push('/study-management/study-overview')
    } else if (store.state.auth.user.role === 'user_admin') {
      router.push('/user-overview')
    } else {
    }
  }
})

// prevent double login study
router.beforeEach(async (to, from) => {
  if (to.name === 'StudyLogin' && store.state.auth.user && store.state.currentStudy.title !== String) {
    if (store.state.auth.user.role === 'study_participant') {
      router.push('/study/' + store.state.currentStudy.id + '/participation')
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
