<template>
  <div class="container d-flex mt-4">
    <loadingModal :title="errorTitle" :text="loadingText" :loading="loading" :error="error" :errorMsg="errorMsg" id="loadingModal"></loadingModal>
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
import { updateStudy } from '@/api'
import loadingModal from '@/components/misc/loadingModal'
import { Modal } from 'bootstrap'

export default {
  name: 'StudyMetainfo',
  components: {
    loadingModal
  },
  data () {
    return {
      loadingText: String,
      loading: Boolean,
      error: false,
      errorTitle: String,
      errorMsg: String
    }
  },
  computed: {
    studyName: {
      get () {
        return this.$store.getters['openStudy/studyTitle']
      },
      set (value) {
        this.$store.commit('openStudy/updateStudyTitle', value)
      }
    },
    studyPassword: {
      get () {
        return this.$store.getters['openStudy/studyPassword']
      },
      set (value) {
        this.$store.commit('openStudy/updateStudyPassword', value)
      }
    },
    studyDesc: {
      get () {
        return this.$store.getters['openStudy/studyDescription']
      },
      set (value) {
        this.$store.commit('openStudy/updateStudyDesc', value)
      }
    }
  },
  methods: {
    saveMetaInfos () {
      this.loadingText = 'Saving Metainfos. Please wait...'
      this.loading = true
      const loadingModal = new Modal(document.getElementById('loadingModal'), { fade: true })
      loadingModal.show()

      const studyId = this.$route.params.id
      const data = {
        title: this.studyName,
        password: this.studyPassword,
        description: this.studyDesc
      }

      updateStudy(studyId, data)
        .then(response => {
          this.loading = false
          this.loadingText = 'Saving successful.'
          setTimeout(function () {
            loadingModal.hide()
          }, 1000)
        })
        .catch(error => {
          this.errorTitle = 'Saving Metainfos...'
          this.error = true
          this.errorMsg = error
        })
        .then()
    }
  }
}
</script>
