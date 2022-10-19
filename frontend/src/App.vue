<template >
  <div class="h-full">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark ms-auto mb-2 mb-lg-0" id="navbar">
      <div class="container-fluid">
        <button class="navbar-toggler ms-auto hidden-sm-up float-xs-right" type="button" data-toggle="collapse"
          data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse text-right ms-auto bg-dark" id="navbarResponsive">
          <ul class="navbar-nav ms-auto" id="navlinks">
            <li v-if="isUserAdmin" class="nav-item">
              <router-link to="/user-overview" class="nav-link">Users Overview</router-link>
            </li>
            <li v-if="isStudyAdmin" class="nav-item">
              <router-link to="/study-management/study-overview" class="nav-link">Studies Overview</router-link>
            </li>
            <li v-if="loggedIn" class="nav-item">
              <router-link to="/user-profile/1" class="nav-link">User Profile</router-link>
            </li>
            <li v-if="isStudyAdmin" class="nav-item">
              <router-link to="/tutorials" class="nav-link">Tutorials</router-link>
            </li>
            <li v-if="loggedIn" @click="handleLogout" class="nav-item">
              <router-link to="/login" class="nav-link">Logout</router-link>
            </li>
            <li v-if="!loggedIn" class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li v-if="!loggedIn" class="nav-item">
               <a class="nav-link" href="">Register</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    currentUser () {
      return this.$store.state.auth.user
    },
    loggedIn () {
      if (this.currentUser) {
        return this.$store.state.auth.status.loggedIn
      }
      return false
    },
    isStudyAdmin () {
      if (this.currentUser && this.currentUser.role) {
        return this.currentUser.role === 'study_admin'
      }
      return false
    },
    isUserAdmin () {
      if (this.currentUser && this.currentUser.role) {
        return this.currentUser.role === 'user_admin'
      }
      return false
    }
  },
  methods: {
    handleLogout () {
      this.$store.dispatch('auth/logout')
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #f6f9fc;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#navbar {
  height: 60px;
}

html,
body {
  height: 100%;
  /*both html and body*/
}
</style>
