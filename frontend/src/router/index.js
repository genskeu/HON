import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import StudyManagement from '../views/StudyManagement.vue'
import StudyOverview from '@/components/studyManagement/StudyOverview.vue'
import StudyMetainfo from '@/components/studyManagement/StudyMetainfo'
import FileManagement from '@/components/studyManagement/FileManagement'
import StudyDesign from '@/components/studyManagement/StudyDesign'
import ResultsOverview from '@/components/resultsManagement/ResultsOverview'

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
    path: '/study-management',
    name: 'StudyManagement',
    component: StudyManagement,
    children: [
      {
        path: 'overview',
        components: {
          helper: StudyOverview
        }
      },
      {
        path: 'metainfos',
        components: {
          helper: StudyMetainfo
        }
      },
      {
        path: 'files',
        components: {
          helper: FileManagement
        }
      },
      {
        path: 'design',
        components: {
          helper: StudyDesign
        }
      },
      {
        path: 'results',
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
