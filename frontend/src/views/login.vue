<template>
  <div class="container" style="height:90%">
    <div class="row justify-content-center align-items-center h-100">
      <form class="form-horizontal mx-auto my-auto col-3" @submit.prevent="handleLogin">
        <div class="form-group mb-1">
          <input v-model="user.username" class="form-control form-control-lg" name="username" id="username"
            placeholder="Username">
        </div>
        <div class="form-group mb-1">
          <input v-model="user.password" class="form-control form-control-lg" type="password" name="password"
            id="password" placeholder="Password" required>
        </div>
        <div class="form-group">
          <input type="submit" value="Login" class="bg-success btn btn-success btn-lg btn-block w-100">
        </div>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  data: () => ({
    user: {
      username: null,
      password: null
    }
  }),
  computed: {
    loggedIn () {
      return this.$store.state.auth.status.loggedIn
    }
  },
  methods: {
    handleLogin () {
      this.loading = true
      this.$store.dispatch('auth/login', this.user).then(
        () => {
          this.$router.push('/study-overview')
        }
      )
    }
  }
}
</script>
