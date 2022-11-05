<template>
  <div id="study_participation">
    <loadingModal id="globalLoadingState" :isLoading="loadingState.isLoading" :title="loadingState.title" :errorOccured="loadingState.errorOccured" :errorData="loadingState.errorData"></loadingModal>
    <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
      <div class="container-fluid mx-auto" v-if="studyOpened">
        <div class="btn btn-danger col-2 ms-auto" @click="studyLogout">Pause {{studyTitle}} (Logout from study)</div>
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
  },
  methods: {
    studyLogout () {
      this.$store.dispatch('currentStudy/logoutStudy')
    }
  }
}
</script>

<style>
#study_participation {
  height: calc(100% - 60px);
}
</style>
