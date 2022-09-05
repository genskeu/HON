<template>
    <div>
        <loadingModal :title="errorTitle" :text="loadingText" :loading="loading" :error="error" :errorMsg="errorMsg" id="loadingModal"></loadingModal>
        <div class="row mx-auto" id="design_options_title">
            <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#design_options_content"
                title="Click on the sections to expand the sub-menus.
                    Study design options were divided into general settings, tools, instructions and scales.
                    After changing any design options dont forget to press the Save Design button.
                              " aria-expanded="true" aria-controls="design_settings_content">
                <h4 class="w-100 mt-1">Design Options &#9776;</h4>
            </button>
        </div>
        <div id="design_options_content" class="collapse show">
            <GeneralSettings></GeneralSettings>
            <Instructions></Instructions>
            <Scales></Scales>
            <Tools></Tools>
            <button @click="saveDesign" class="mt-1 btn btn-success w-100">
                Save Design
            </button>
        </div>

    </div>
</template>

<script>
import GeneralSettings from '@/components/studyDesign/designOptions/GeneralSettings.vue'
import Scales from '@/components/studyDesign/designOptions/Scales.vue'
import Instructions from '@/components/studyDesign/designOptions/Instructions.vue'
import Tools from '@/components/studyDesign/designOptions/Tools.vue'
import { updateStudyDesign } from '@/api'
import loadingModal from '@/components/misc/loadingModal'
import { Modal } from 'bootstrap'

export default {
  name: 'DesignOptions',
  components: {
    GeneralSettings,
    Scales,
    Instructions,
    Tools,
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
  methods: {
    saveDesign () {
      const design = this.$store.getters['openStudy/design']
      const studyId = this.$route.params.id
      const loadingModal = new Modal(document.getElementById('loadingModal'), { fade: true })
      loadingModal.show()

      updateStudyDesign(studyId, design)
        .then(response => {
          this.loading = false
          this.loadingText = 'Saving successful.'
          setTimeout(function () {
            loadingModal.hide()
          }, 1000)
        })
        .catch(error => {
          this.errorTitle = 'Error Saving Design...'
          this.error = true
          this.errorMsg = error
        })
        .then()
    }
  }
}
</script>

<style>

</style>
