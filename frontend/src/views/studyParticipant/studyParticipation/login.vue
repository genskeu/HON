<template>
  <div class="container" style="height:90%">
    <div class="row justify-content-center align-items-center h-100">
      <form class="form-horizontal mx-auto my-auto col-3" @submit.prevent="studyLogin">
        <div class="form-group mb-1">
          <input v-model="studyId" class="form-control form-control-lg" placeholder="StudyId" type="number">
        </div>
        <div class="form-group mb-1">
          <input v-model="studyPassword" class="form-control form-control-lg" type="password" name="password"
            id="password" placeholder="Password" required>
        </div>
        <div class="form-group">
          <input type="submit" value="Login to study" class="bg-success btn btn-success btn-lg btn-block w-100">
        </div>
      </form>
    </div>
  </div>
                <!-- <div class="row">
                    <div class="input-group mx-auto">
                        <label class="input-group-text">Study ID</label>
                        <input class="form-control" type="number" v-model="studyId">
                        <label class="input-group-text" for="viewerHeightAuto">Password</label>
                        <input class="form-control" type="password" v-model="studyPassword">
                        <button type="form-control" class="btn btn-success btn-block" @click="studyLogin">Login</button>
                    </div>
                </div> -->
</template>

<script>
export default {
  data: () => ({
    studyId: null,
    studyPassword: null
  }),
  methods: {
    studyLogin () {
      // get study data from backend
      this.$store.dispatch('currentStudy/studyLogin', { study_id: this.studyId, password: this.studyPassword })
    }
  }
}
</script>

<style>

</style>
