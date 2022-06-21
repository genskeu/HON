import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import StudyManagement from '@/views/studyAdmin/StudyManagement.vue'
import StudyOverview from '@/views/studyAdmin/StudyOverview.vue'
import StudyMetainfo from '@/views/studyAdmin/studyManagement/StudyMetainfo'
import FileManagement from '@/views/studyAdmin/studyManagement/FileManagement'
import StudyDesign from '@/views/studyAdmin/studyManagement/StudyDesign'
import ResultsOverview from '@/views/studyAdmin/studyManagement/ResultsOverview'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/study-overview',
    name: 'StudyOverview',
    component: StudyOverview
  },
  {
    path: '/study-management/:id',
    name: 'StudyManagement',
    component: StudyManagement,
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
        path: 'results',
        name: 'StudyResults',
        components: {
          helper: ResultsOverview
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
