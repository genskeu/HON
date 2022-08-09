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

const routes = [
  {
    path: '/user-overview',
    name: 'UserOverview',
    component: UserOverview
  },
  {
    path: '/user-profile/:id',
    name: 'UserProfile',
    component: UserProfile
  },
  {
    path: '/tutorials',
    name: 'Tutorials',
    component: Tutorials
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
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
