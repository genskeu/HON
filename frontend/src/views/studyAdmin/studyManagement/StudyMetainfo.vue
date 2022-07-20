<template>
  <div class="container d-flex align-items-center">
    <form class="form-horizontal w-100" id="study_metadata">

      <div class="row mx-auto mt-4">
        <div class="input-group">
          <label class="input-group-text w-40" for="title">Title</label>
          <input class="form-control" name="title" id="title" placeholder="Study Title" v-model="study_name">
        </div>
      </div>

      <div class="row mx-auto">
        <div class="input-group">
          <label class="input-group-text w-40">Password</label>
          <input class="form-control" type="password" name="password" id="password" placeholder="Access Password">
        </div>
      </div>

      <div class="row mx-auto">
        <div class="input-group" data-toggle="tooltip" data-placement="left" title="The study description is shown to participants
at the beginning of the study and should include
basic information about the study
e.g. how many images have to be evaluated.">
          <label class="input-group-text w-40">Study Description</label>
          <textarea v-model="study_desc" class="form-control" name="description" id="description" rows="20"></textarea>
        </div>
      </div>

      <div class="row mx-auto" id="study_setup_navbar">
        <div class="col-12">
          <button class="btn btn-light btn-lg btn-block w-100">
            Save Metainfos
          </button>
        </div>
      </div>

    </form>
  </div>
</template>

<script>

export default {
  name: 'StudyMetainfo',
  computed: {
    study_name: {
      get () {
        return this.$store.getters['openStudy/studyTitle']
      },
      set (value) {
        this.$store.commit('openStudy/updateStudyTitle', value)
      }
    },
    study_desc: {
      get () {
        return this.$store.getters['openStudy/studyDescription']
      },
      set (value) {
        this.$store.commit('openStudy/updateStudyDesc', value)
      }
    }
  }
}
</script>
