<template>
  <div class="">
    <div id="nav">
      <router-link to="/study-management">Studies</router-link> |
      <router-link to="/study-management">Results</router-link>
      <router-link to="/study-management"></router-link>
    </div>
    <study-overview>
    </study-overview>
  </div>
</template>

<script>
// @ is an alias to /src
import StudyOverview from '@/components/studyManagement/StudyOverview.vue'

export default {
  name: 'StudyManagement',
  components: {
    StudyOverview
  }
}
</script>
