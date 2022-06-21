<template>
  <div class="container-fluid pt-4 h-100" id="content" :style="cssStyle">
    <div class="row mx-auto h-100">
      <!-- Imgsets -->
      <div class="col-lg-10 mb-2 h-100" id="imgset_creation">
        <div class="row w-100 mx-auto mb-2" id = "imgset_creation_title">
          <button
            class="btn btn-dark mb-2"
            data-bs-toggle="collapse"
            data-bs-target="#imgset_creation_content"
            aria-expanded="true"
            aria-controls="imgset_creation_content">
            <h4 class="mt-1">Image Sets &#9776;</h4>
          </button>
        </div>
        <!-- Create Image Sets -->
        <div class="show collapse row w-100 mx-auto" id = "imgset_creation_content">
          <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
          <div id="imgset" class="min-h-100 mx-auto px-0 w-100">
            <!--Images -->
            <!-- <div id="ref_images">
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Reference Image Stack(s)</h4>
              </span>
            </div> -->
              <span class="badge bg-secondary mx-auto w-100 mb-2">
                <h4 class="mt-1">Reference-Stack(s)</h4>
              </span>
              <div id="ref-stacks" :class="refviewerLayout">
                <dicom-viewer v-for="index in refviewerNumb" :key="index"></dicom-viewer>
              </div>
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Stack(s)</h4>
              </span>
              <div id="stacks" :class="viewerLayout">
                <dicom-viewer v-for="index in viewerNumb" :key="index"></dicom-viewer>
              </div>
            <!-- modify buttons -->
            <div id="imgset_creation_buttons">
              <div class="row mt-3 mb-2">
                <div class="col-lg-12 text-center">
                  <button
                    value="append imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="add_imgset"
                    title="add image-set to the end of the study"
                  >append imgset</button>
                  <input
                    value="insert imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="insert_imgset"
                    title="inserts image-set at the currently selected position"
                  />
                  <input
                    value="update imgset"
                    class="imgset_btn btn-light btn col-lg-2"
                    id="upd_imgset"
                    title="update currently selected image-set"
                  />
                  <input
                    value="delete imgset"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_imgset"
                    title="delete currently selected image-set"
                  />
                  <input
                    value="delete all imgsets"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_all_imgsets"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2">
        <!-- Design Settings -->
        <div class="row mx-auto" id="design_settings_title">
          <button
            class="btn btn-dark col-12 mb-1"
            data-bs-toggle="collapse"
            data-bs-target="#design_settings_content"
            title="Click on the sections to expand the sub-menus.
                    Study design options were divided into general settings, tools, instructions and scales.
                    After changing any design options dont forget to press the Save Design button.
                              "
            aria-expanded="true"
            aria-controls="design_settings_content"
          >
            <h4 class="w-100 mt-1">Design Options &#9776;</h4>
          </button>
        </div>
        <div id="design_settings_content" class="collapse show">
          <GeneralSettings></GeneralSettings>
        </div>
        <div>
          <DicomViewportControl v-for="index in viewerNumb" :key="index"></DicomViewportControl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import GeneralSettings from '@/components/studyDesign/GeneralSettings.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'

export default {
  name: 'Design',
  components: {
    DicomViewer,
    GeneralSettings,
    DicomViewportControl
  },
  computed: {
    viewerNumb () {
      return this.$store.getters.viewerNumb
    },
    viewerLayout () {
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'grid-cols-5': this.$store.getters.viewerLayoutCols === 5,
        'grid-cols-4': this.$store.getters.viewerLayoutCols === 4,
        'grid-cols-3': this.$store.getters.viewerLayoutCols === 3,
        'grid-cols-2': this.$store.getters.viewerLayoutCols === 2,
        'grid-cols-1': this.$store.getters.viewerLayoutCols === 1,
        'grid-rows-5': this.$store.getters.viewerLayoutRows === 5,
        'grid-rows-4': this.$store.getters.viewerLayoutRows === 4,
        'grid-rows-3': this.$store.getters.viewerLayoutRows === 3,
        'grid-rows-2': this.$store.getters.viewerLayoutRows === 2,
        'grid-rows-1': this.$store.getters.viewerLayoutRows === 1
      }
      return gridClass
    },
    refviewerNumb () {
      return this.$store.getters.refviewerNumb
    },
    refviewerLayout () {
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'gap-2': true,
        'grid-cols-1': this.$store.getters.refviewerNumb === 1,
        'grid-cols-2': this.$store.getters.refviewerNumb === 2,
        'grid-rows-1': true
      }
      return gridClass
    },
    cssStyle () {
      return {
        'background-color': this.$store.getters.backgroundColor,
        color: this.$store.getters.textColor
      }
    }
  },
  watch: {
    backgroundColor (oldColor, newColor) {
      console.log(oldColor)
      console.log(newColor)
    }
  }
}
</script>

<style>
#imgset_creation_title {
  height: 5%;
}
#imgset_creation_content {
  height: 95%;
}
</style>
