<template>
  <div v-if="study_opened" id="study_management" class="">
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
      <div class="container mx-auto">
        <router-link to="/study-overview" @click="finishEditing" class="nav-link">&times; Close {{studyTitle}}</router-link>
        <router-link :to="{ name: 'StudyMetainfos', params: { id: this.$route.params.id }}" class="nav-link">Metainfos</router-link>
        <router-link :to="{ name: 'StudyFiles', params: { id: this.$route.params.id }}" class="nav-link">Files</router-link>
        <router-link :to="{ name: 'StudyDesign', params: { id: this.$route.params.id }}" class="nav-link">Design</router-link>
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
import axios from 'axios'

export default {
  name: 'StudyManagement',
  data () {
    return {
    }
  },
  methods: {
    finishEditing () {
      this.$store.commit('closeStudy')
    }
  },
  computed: {
    study_opened () {
      return this.$store.state.open_study !== undefined
    },
    studyTitle () {
      return this.$store.getters.studyTitle
    }
  },
  created () {
    const id = this.$route.params.id
    axios
      .get('http://localhost:5000/study/' + id)
      .then((response) => {
        const data = response.data
        this.$store.commit('openStudy', data.study)
      })
  }
}
</script>

<style>
#study_management {
  height: calc(100% - 60px);
}

#router_helper_view {
  min-height: calc(100% - 50px);
}
</style>
