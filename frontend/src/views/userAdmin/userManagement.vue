<template>
    <div id="study_management" class="">
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

export default {
  name: 'StudyManagement',
  data () {
    return {
    }
  },
  beforeCreate () {
    return this.$store.dispatch('users/initUsers')
  },
  methods: {
  },
  computed: {
  },

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
