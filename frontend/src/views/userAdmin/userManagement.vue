<template>
    <div id="study_management" class="">
      <loadingModal id="globalLoadingState" :isLoading="loadingState.isLoading" :title="loadingState.title" :errorOccured="loadingState.errorOccured" :errorData="loadingState.errorData"></loadingModal>
      <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
        <div class="container mx-auto">
          <!-- <router-link to="#" @click.prevent="createUser" class="btn btn-succcess">Create New User
          </router-link> -->
        </div>
      </div>
      <router-view name="helper" id="router_helper_view">
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
  },
  computed: {
    loadingState () {
      return this.$store.getters['loadingState/state']
    }
  },
  mounted () {
    return this.$store.dispatch('users/initUsers')
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
