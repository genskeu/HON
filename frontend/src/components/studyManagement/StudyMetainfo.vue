<template>
  <div class="container">
    <div class="row h-100">
      <div class="col-12 my-auto">
        <div class="form-horizontal" id="study_data">
          <div class="row mx-auto mt-4">
            <div class="input-group">
              <div class="input-group-prepend col-2 px-0">
                <span class="input-group-text col-12">Title</span>
              </div>
              <input class="form-control form-control" name="title" id="title" placeholder="Study Title" v-model="study_name">
            </div>
          </div>

          <div class="row mx-auto">
            <div class="input-group">
              <div class="input-group-prepend col-2 px-0">
                <span class="input-group-text col-12">Password</span>
              </div>
              <input class="form-control" type="password" name="password" id="password" placeholder="Access Password">
            </div>
          </div>

          <div class="row mx-auto">
            <div class="input-group" data-toggle="tooltip" data-placement="left" title="The study description is shown to participants
at the beginning of the study and should include
basic information about the study
e.g. how many images have to be evaluated.">
              <div class="input-group-prepend col-2 px-auto">
                <span class="mx-auto input-group-text h-100">Study Description</span>
              </div>
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

        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'StudyMetainfo',
  computed: {
    study_name: {
      get () {
        return this.$store.state.open_study ? this.$store.state.open_study.title : undefined
      },
      set (value) {
        this.$store.commit('updateStudyTitle', value)
      }
    },
    study_desc: {
      get () {
        return this.$store.state.open_study ? this.$store.state.open_study.description : undefined
      },
      set (value) {
        this.$store.commit('updateStudyDesc', value)
      }
    }
  }
}
</script>
