<template>
  <div v-if="studyOpened" id="study_management" class="">
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
      <div class="container mx-auto">
        <router-link to="/study-overview" @click="finishEditing" class="nav-link">&times; Close {{studyTitle}}</router-link>
        <router-link :to="{ name: 'StudyMetainfos', params: { id: this.$route.params.id }}" class="nav-link">Metainfos</router-link>
        <router-link :to="{ name: 'StudyFiles', params: { id: this.$route.params.id }}" class="nav-link">Files</router-link>
        <router-link :to="{ name: 'StudyDesign', params: { id: this.$route.params.id }}" class="nav-link">Design</router-link>
        <router-link :to="{ name: 'StudyParticipation', params: { id: this.$route.params.id }}" class="nav-link">Participant Preview</router-link>
        <router-link :to="{ name: 'StudyResults', params: { id: this.$route.params.id }}" class="nav-link">Results</router-link>
      </div>
    </div>
    <router-view name="helper" id="router_helper_view">
    </router-view>
  </div>
  <div v-else id="study_management" class="">
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
    </div>
  </div>

</template>

<script>
import { fetchStudy } from '@/api'
export default {
  name: 'StudyManagement',
  data () {
    return {
    }
  },
  methods: {
    finishEditing () {
      this.$store.commit('openStudy/closeStudy')
    },
    saveStudy () {
    }
  },
  computed: {
    studyOpened () {
      return this.$store.getters['openStudy/studyTitle'] !== String
    },
    studyTitle () {
      return this.$store.getters['openStudy/studyTitle']
    }
  },
  created () {
    const id = this.$route.params.id
    fetchStudy(id)
      .then((response) => {
        const data = response.data
        this.$store.commit('openStudy/openStudy', data.study)
      })
  }
}
</script>

<style>
#study_management {
  height: calc(100% - 60px);
}

#router_helper_view {
  min-height: calc(100% - 75px);
}
</style>
