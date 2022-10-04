<template>
    <div>
        <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
            <div v-if="!studyOpened" class="container">
                <div class="row">
                    <div class="input-group mx-auto">
                        <label class="input-group-text">Study ID</label>
                        <input class="form-control" type="number" v-model="studyId">
                        <label class="input-group-text" for="viewerHeightAuto">Password</label>
                        <input class="form-control" type="password" v-model="studyPassword">
                        <button type="form-control" class="btn btn-success btn-block" @click="studyLogin">Login</button>
                    </div>
                </div>
            </div>
        </div>
        <participation v-if="studyOpened">
        </participation>
    </div>
</template>

<script>
import participation from '@/views/studyParticipant/participation'
export default {
  components: {
    participation
  },
  data: () => ({
    studyId: null,
    studyPassword: null
  }),
  computed: {
    studyOpened () {
      return this.$store.getters['openStudy/studyTitle'] !== String
    }
  },
  methods: {
    studyLogin () {
      // get study data from backend
      this.$store.dispatch('openStudy/studyLogin', { study_id: this.studyId, password: this.studyPassword })
    }
  }
}
</script>

<style>

</style>
