<template>
  <div class="container d-flex mt-4">
    <div class="form-horizontal w-100" id="study_metadata">
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-40" for="title">Title</label>
          <input class="form-control" name="title" id="title" placeholder="Study Title" v-model="studyName">
        </div>
      </div>

      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-40">Password</label>
          <input class="form-control" type="password" name="password" id="password" placeholder="Access Password" v-model="studyPassword">
        </div>
      </div>

      <div class="mx-auto">
        <div class="input-group" data-toggle="tooltip" data-placement="left" title="The study description is shown to participants
at the beginning of the study and should include
basic information about the study
e.g. how many images have to be evaluated.">
          <label class="input-group-text w-40">Study Description</label>
          <textarea v-model="studyDesc" class="form-control" name="description" id="description" rows="20"></textarea>
        </div>
      </div>
      <div class="row mx-auto mt-1">
        <button class="btn btn-lg btn-success" @click="saveMetaInfos">Save Metainfos</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudyMetainfo',
  data () {
    return {
    }
  },
  computed: {
    studyName: {
      get () {
        return this.$store.getters['currentStudy/studyTitle']
      },
      set (value) {
        this.$store.commit('currentStudy/updateStudyTitle', value)
      }
    },
    studyPassword: {
      get () {
        return this.$store.getters['currentStudy/studyPassword']
      },
      set (value) {
        this.$store.commit('currentStudy/updateStudyPassword', value)
      }
    },
    studyDesc: {
      get () {
        return this.$store.getters['currentStudy/studyDescription']
      },
      set (value) {
        this.$store.commit('currentStudy/updateStudyDesc', value)
      }
    }
  },
  methods: {
    saveMetaInfos () {
      const studyId = this.$route.params.id
      const data = {
        title: this.studyName,
        password: this.studyPassword,
        description: this.studyDesc
      }
      this.$store.dispatch('currentStudy/updateStudyMetainfos', { studyId: studyId, data: data })
    }
  }
}
</script>
