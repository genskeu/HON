<template>
    <div>
        <div class="row mx-auto" id="design_options_title">
            <button class="btn btn-dark btn-lg col-12" data-bs-toggle="collapse" data-bs-target="#design_options_content"
                title="Click on the sections to expand the sub-menus.
                    Study design options were divided into general settings, tools, instructions and scales.
                    After changing any design options dont forget to press the Save Design button.
                              " aria-expanded="true" aria-controls="design_settings_content">
                <h4 class="w-100">Design Options &#9776;</h4>
            </button>
        </div>
        <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#design_settings_explanation"
              aria-expanded="true">
              <h4 class="w-100">&#9432; Section Info</h4>
            </button>
            <div id="design_settings_explanation" class="row mx-auto text-dark bg-white text-left collapse">
              <ul class="list-group mx-0 px-0">
                <li class="list-group-item">This section controls the study design.</li>
              </ul>
            </div>
        <div id="design_options_content" class="collapse show">
            <GeneralSettings></GeneralSettings>
            <Instructions></Instructions>
            <Scales></Scales>
            <Tools></Tools>
            <button @click="saveDesign" class="mt-1 btn btn-lg btn-success w-100">
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

export default {
  name: 'DesignOptions',
  components: {
    GeneralSettings,
    Scales,
    Instructions,
    Tools
  },
  data () {
    return {
    }
  },
  methods: {
    saveDesign () {
      const studyId = this.$route.params.id
      this.$store.dispatch('currentStudy/updateDesign', studyId)
    }
  }
}
</script>

<style>

</style>
