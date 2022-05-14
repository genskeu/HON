<template>
  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark ms-auto mb-2 mb-lg-0" id="navbar">
    <div class="container-fluid">
      <button class="navbar-toggler ms-auto hidden-sm-up float-xs-right" type="button" data-toggle="collapse"
        data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse text-right ms-auto bg-dark" id="navbarResponsive">
        <ul class="navbar-nav ml-auto" id="navlinks">
          <li class="nav-item">
            <a class="nav-link" href="">User Profile</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="">Tutorials</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="">Log Out</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="">Register</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="">Log In</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
