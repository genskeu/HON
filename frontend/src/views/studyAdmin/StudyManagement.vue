<template>
  <div id="study_management" class="">
    <loadingModal id="globalLoadingState" :isLoading="loadingState.isLoading" :title="loadingState.title" :errorOccured="loadingState.errorOccured" :errorData="loadingState.errorData"></loadingModal>
    <div id="nav" class="navbar bg-dark p-0 pb-2" style="height: 50px;">
      <div class="container mx-auto" v-if="studyOpened">
          <a id="close-study" @click="closeStudy" class="btn router-link">&times; Close {{studyTitle}}</a>
          <router-link id="metainfos" :to="{ name: 'StudyMetainfos', params: { id: studyId }}" class="nav-link">Metainfos</router-link>
          <router-link id="fileupload" :to="{ name: 'StudyFiles', params: { id: studyId }}" class="nav-link">Files</router-link>
          <router-link id="design" :to="{ name: 'StudyDesign', params: { id: studyId }}" class="nav-link">Design</router-link>
          <router-link id="preview" :to="{ name: 'StudyParticipationPreview', params: { id: studyId }}" class="nav-link">Participant Preview</router-link>
          <router-link id="results" :to="{ name: 'StudyResults', params: { id: studyId }}" class="nav-link">Results</router-link>
        </div>
          <div class="container mx-auto" v-else id="">
        <router-link id="create-study" to="#" @click.prevent="createStudy" class="btn btn-succcess">Create New Study
        </router-link>
      </div>
    </div>
    <router-view class="pt-4" v-if="studyOpened | this.$route.name === 'StudyOverview'" v-slot="{ Component }" name="helper" id="router_helper_view">
      <!-- only keep comp alive aslong as study is opened -->
      <keep-alive v-if="studyOpened">
        <component :is="Component" />
      </keep-alive>
      <component v-else :is="Component" />
    </router-view>
  </div>
</template>

<script>
import loadingModal from '@/components/misc/loadingModal'

export default {
  name: 'StudyManagement',
  components: {
    loadingModal
  },
  data () {
    return {
    }
  },
  methods: {
    createStudy () {
      this.$store.dispatch('currentStudy/createNewStudy')
    },
    closeStudy () {
      this.$store.dispatch('currentStudy/closeStudy')
    },
    saveStudy () {
    }
  },
  computed: {
    studyId () {
      return this.$store.getters['currentStudy/id']
    },
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
#router_helper_view {
  height: calc(100% - 50px);
}
</style>
