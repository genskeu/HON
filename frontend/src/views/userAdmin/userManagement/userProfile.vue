<template>
<div class="container h-100">
  <div class="row justify-content-center align-items-center h-100">
    <div class="col-5 my-auto">
      <form class="form-horizontal" method="post" id="study_data" action="">
        <div class="input-group row mx-auto">
          <label class="input-group-text col-3">Username</label>
          <input class="form-control form-control" name="username" id="username" placeholder="username" v-model="username" required>
        </div>

        <div class="input-group row mx-auto">
          <label class="input-group-text col-3">Password</label>
          <input v-model="password" class="form-control form-control" type="password" name="password" id="password" placeholder="password">
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text col-3">Type</label>
          <select v-model="userAccesslevel" class="form-select" name="access_level" id="access_level">
            <option value=""></option>
            <option value="1">Participant</option>
            <option value="2">Study Admin</option>
            <option value="3">User Admin</option>
          </select>
        </div>

        <div class="row mx-auto mt-2">
          <input class="btn-secondary btn" value="update user information" @click="saveUser">
        </div>
      </form>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'UserProfile',
  computed: {
    user () {
      return this.$store.getters['users/currentUser']
    },
    userAccesslevel: {
      get () {
        return this.user.access_level
      },
      set (value) {
        this.$store.commit('users/updCurrentUser', { id: this.user.id, access_level: value })
      }
    },
    username: {
      get () {
        return this.user.username
      },
      set (value) {
        this.$store.commit('users/updCurrentUser', { id: this.user.id, username: value })
      }
    },
    password: {
      get () {
        return this.user.password
      },
      set (value) {
        this.$store.commit('users/updCurrentUser', { id: this.user.id, password: value })
      }
    }
  },
  methods: {
    saveUser () {
      const userId = this.user.id
      this.$store.dispatch('users/updUser', userId)
    }
  },
  beforeCreate () {
    // get study data from backend
    const id = this.$route.params.id
    if (id) {
      this.$store.dispatch('users/setUser', id)
    } else {
      const user = this.$store.getters['auth/user']
      this.$store.commit('users/setUser', user)
    }
  }
}
</script>

<style>

</style>
