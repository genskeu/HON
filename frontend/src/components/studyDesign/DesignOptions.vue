<template>
    <div class="accordion">

      <div class="accordion-item bg-dark">
        <div class="row">
          <div class="col-2 my-auto mx-auto">
            <button class="btn btn-lg btn-dark" data-bs-toggle="popover" :data-bs-title="this.popoverTitle" :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
            </button>
          </div>

          <div class="col-10 my-auto">
            <h1 class="accordion-header" id="design_options_title">
              <button class="primary-accordion accordion-button pr-0" type="button" data-bs-toggle="collapse" data-bs-target="#design_options_content" aria-expanded="true" aria-controls="design_options_content">
                <strong>Design Options &#9776;</strong>
              </button>
            </h1>
          </div>
        </div>
            <!-- <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#design_settings_explanation"
              aria-expanded="true">
              <h4 class="w-100">&#9432; Section Info</h4>
            </button>
            <div id="design_settings_explanation" class="row mx-auto text-dark bg-white text-left collapse">
              <ul class="list-group mx-0 px-0">
                <li class="list-group-item">This section controls the study design.</li>
              </ul>
            </div> -->
        <div id="design_options_content" class="accordion-collapse show" aria-labelledby="design_options_title">
            <GeneralSettings class="mb-1"></GeneralSettings>
            <Instructions class="mb-1"></Instructions>
            <Scales class="mb-1"></Scales>
            <Tools class="mb-1"></Tools>
            <button @click="saveDesign" class="btn btn-lg btn-success w-100">
                Save Design
            </button>
        </div>
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
      popoverTitle: 'Section Info',
      popoverText: 'Click on the sections to expand the sub-menus. Study design options were divided into general settings, tools, instructions and scales. After changing any design options dont forget to press the Save Design button.'
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
