<template>
  <div class="container-fluid pt-4" id="content" :style="cssStyle">
    <div class="row mx-auto">
      <!-- Imgsets -->
      <div class="col-lg-10 pt-1" id="imgset_creation">
        <!-- <div class="row w-100 mx-auto pb-2" id = "imgset_creation_title">
          <button
            class="btn btn-dark"
            data-bs-toggle="collapse"
            data-bs-target="#imgset_creation_content"
            aria-expanded="true"
            aria-controls="imgset_creation_content">
            <h4 class="mt-1">Image Sets &#9776;</h4>
          </button>
        </div> -->
        <!-- Create Image Sets -->
        <div class="show collapse row w-100 mx-auto" id = "imgset_creation_content">
          <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
          <div id="imgset" class="mx-auto px-0 w-100">
            <!--Images -->
              <DicomViewerTools class="sticky-top mb-2"></DicomViewerTools>
              <div v-if="refviewerNumb" class="badge bg-secondary mx-auto w-100">
                <h4 class="">Reference-Image-Stack(s)</h4>
              </div>
              <div id="ref-stacks" :class="refviewerLayout">
                <div v-for="index in refviewerNumb" :key="index">
                  <h4>Reference Image Viewer {{index}}</h4>
                <dicom-viewer viewer-type="refviewers" :viewer-index="index-1"></dicom-viewer>
                </div>
              </div>
              <div v-if="refviewerNumb"  class="badge bg-secondary w-100 mb-2">
                <h4 class="">Image-Stack(s)</h4>
              </div>
              <div id="stacks" :class="viewerLayout">
                <div v-for="index in viewerNumb" :key="index">
                  <h4>Image Viewer {{index}}</h4>
                  <dicom-viewer viewer-type="viewers" :viewer-index="index-1"></dicom-viewer>
                </div>
              </div>
            <div>
          </div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2 pt-1 overflow-auto sticky-top" id="sidebar">
        <!-- Design Settings -->
        <DesignOptions></DesignOptions>
        <ImgsetDesign class="w-100 mb-2"></ImgsetDesign>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import DicomViewerTools from '@/components/dicomViewer/DicomViewerTools.vue'
import DesignOptions from '@/components/studyDesign/DesignOptions.vue'
import ImgsetDesign from '@/components/studyDesign/ImgsetDesign.vue'

export default {
  name: 'Design',
  components: {
    DicomViewer,
    DicomViewerTools,
    ImgsetDesign,
    DesignOptions
  },
  computed: {
    viewerNumb () {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    viewerLayout () {
      // var colClass = 'grid-cols-' + this.$store.getters.viewerLayoutCols
      // var rowClass = 'grid-rows-' + this.$store.getters.viewerLayoutRows
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'grid-cols-5': this.$store.getters['currentStudy/viewerLayoutCols'] === 5,
        'grid-cols-4': this.$store.getters['currentStudy/viewerLayoutCols'] === 4,
        'grid-cols-3': this.$store.getters['currentStudy/viewerLayoutCols'] === 3,
        'grid-cols-2': this.$store.getters['currentStudy/viewerLayoutCols'] === 2,
        'grid-cols-1': this.$store.getters['currentStudy/viewerLayoutCols'] === 1
      }
      return gridClass
    },
    refviewerNumb () {
      return this.$store.getters['currentStudy/refviewerNumb']
    },
    refviewerLayout () {
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'gap-2': true,
        'grid-cols-1': this.$store.getters['currentStudy/refviewerNumb'] === 1,
        'grid-cols-2': this.$store.getters['currentStudy/refviewerNumb'] === 2,
        'grid-cols-3': this.$store.getters['currentStudy/refviewerNumb'] === 3,
        'grid-cols-4': this.$store.getters['currentStudy/refviewerNumb'] === 4,
        'grid-cols-5': this.$store.getters['currentStudy/refviewerNumb'] === 5,
        'grid-rows-1': true
      }
      return gridClass
    },
    cssStyle () {
      return {
        'background-color': this.$store.getters['currentStudy/backgroundColor'],
        color: this.$store.getters['currentStudy/textColor']
      }
    },
    toolsMousekeys () {
      return this.$store.getters['imageViewers/toolsMousekeys']
    },
    toolsMousewheel () {
      return this.$store.getters['imageViewers/toolsMousewheel']
    }
  },
  watch: {
  },
  mounted () {
    // bug fix for switching between design and participation interface
    // set active imgset to undefined when mounting => find more elegant solution later
  },
  activated () {
  },
  deactivated () {
    this.$store.commit('currentStudy/imgsetDisplayed', undefined)
  },
  methods: {
  }
}
</script>

<style>
#sidebar {
  height: 85vh;
}

</style>
