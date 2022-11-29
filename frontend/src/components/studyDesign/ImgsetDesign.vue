<template>
  <div class="accordion mt-4">
    <div class="accordion-item bg-dark">
      <!-- header -->
      <div class="row">
        <div class="col-2 my-auto mx-auto">
          <button class="btn btn-lg btn-dark" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
            :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
          </button>
        </div>

        <div class="col-10 my-auto pr-5">
          <h1 class="accordion-header" id="imgset_settings_title">
            <button class="primary-accordion accordion-button show" type="button" data-bs-toggle="collapse"
              data-bs-target="#imgset_settings" aria-expanded="true" aria-controls="imgset_settings">
              <strong>Image-Sets &#9776;</strong>
            </button>
          </h1>
        </div>
      </div>

      <!-- content -->
      <div id="imgset_settings" class="show accordion-collapse accordion">
        <!-- manual creation -->
        <manual-creation class="accordion-item"></manual-creation>
        <!-- auto creation -->
        <auto-creation class="accordion-item"></auto-creation>
      </div>
    </div>
  </div>
</template>

<script>
import { Popover } from 'bootstrap'
import manualCreation from '@/components/studyDesign/imgsetDesign/manualCreation.vue'
import autoCreation from '@/components/studyDesign/imgsetDesign/autoCreation.vue'

export default {
  name: 'ImgsetControl',
  components: {
    manualCreation,
    autoCreation
  },
  data () {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'This section controls the images displayed to users during a study. Images displayed simultaneously are called an Image-Set. Image-Sets can be created manually (one by one) using the Manual-Creation section or automatically using the Auto-Creation Menu.'
    }
  },
  mounted () {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    Array.from(popoverTriggerList).map(popoverTriggerEl => new Popover(popoverTriggerEl))
  }
}
</script>

<style>
</style>
