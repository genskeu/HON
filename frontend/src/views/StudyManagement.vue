<template>
  <div id="study_management" class="">
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
      <div class="container mx-auto">
        <router-link v-if="study_open" to="/study-management/overview" @click="finishEditing" class="nav-link">&times; Close {{this.$store.state.open_study.title}}</router-link>
        <router-link v-if="study_open" to="/study-management/metaInfos" class="nav-link">Metainfos</router-link>
        <router-link v-if="study_open" to="/study-management/files" class="nav-link">Files</router-link>
        <router-link v-if="study_open" to="/study-management/design" class="nav-link">Design</router-link>
        <router-link v-if="study_open" to="/study-management/results" class="nav-link">Results</router-link>
      </div>
    </div>
    <router-view name="helper" class="">
    </router-view>
  </div>
</template>

<script>
// @ is an alias to /src
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
    study_open () {
      return this.$store.state.open_study !== undefined
    }
  },
  mounted () {
    axios
      .get('http://localhost:5000/studies')
      .then((response) => {
        const overview = response.data
        overview.studies.forEach((study) => {
          this.$store.commit('addStudy', study)
        })
      })
  }
}
</script>

<style scoped>
#study_management {
    height:calc(100% - 110px); /*both html and body*/
}
</style>
