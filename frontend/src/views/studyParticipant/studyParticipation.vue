<template>
  <div>
    <loadingModal id="globalLoadingState" :isLoading="loadingState.isLoading" :title="loadingState.title" :errorOccured="loadingState.errorOccured" :errorMsg="loadingState.errorMsg"></loadingModal>
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
      <div class="container mx-auto" v-if="studyOpened">
        <div>{{studyTitle}}</div>
      </div>
    </div>
    <router-view v-if="studyOpened | this.$route.name === 'StudyLogin'" v-slot="{ Component }" name="helper" id="router_helper_view">
      <component :is="Component" />
    </router-view>
  </div>
</template>

<script>
import loadingModal from '@/components/misc/loadingModal'

export default {
  components: {
    loadingModal
  },
  computed: {
    studyOpened () {
      return this.$store.getters['currentStudy/studyTitle'] !== String
    },
    studyTitle () {
      return this.$store.getters['currentStudy/studyTitle']
    },
    loadingState () {
      return this.$store.getters['loadingState/state']
    }
  },
  beforeCreate () {
    // get study data from backend
    const id = this.$route.params.id
    if (id) {
      this.$store.dispatch('currentStudy/openStudy', id)
    }
  }
}
</script>

<style>

</style>
