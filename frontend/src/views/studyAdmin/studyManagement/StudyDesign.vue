<template>
  <div class="container-fluid" id="content" :style="cssStyle">
    <div class="row mx-auto">
      <!-- Imgsets -->
      <div class="col-lg-10 pt-1" id="imgset_creation">
        <div class="row w-100 mx-auto pb-2" id = "imgset_creation_title">
          <button
            class="btn btn-dark"
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
          <div id="imgset" class="mx-auto px-0 w-100">
            <!--Images -->
            <!-- <div id="ref_images">
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Reference Image Stack(s)</h4>
              </span>
            </div> -->
              <span class="badge bg-secondary mx-auto w-100">
                <h4 class="">Reference-Stack(s)</h4>
              </span>
              <div id="ref-stacks" :class="refviewerLayout">
                <dicom-viewer v-for="index in refviewerNumb" :key="index"></dicom-viewer>
              </div>
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Stack(s)</h4>
              </span>
              <div id="stacks" :class="viewerLayout">
                <dicom-viewer v-for="index in viewerNumb" :key="index" :viewer-index="index-1"></dicom-viewer>
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
      <div class="col-lg-2 pt-1">
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
        <!-- default viewport settings -->
        <div id="viewport_settings_container" class="w-100" title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                        Each viewport can be controlled individually.
                        To globally control viewport settings use the defaults submenu.">
          <div class="row mt-1 mx-auto">
            <button class="btn btn-dark col-12 mb-2" data-bs-toggle="collapse" data-bs-target="#viewport_settings"
              aria-expanded="true" aria-controls="viewport_settings">
              <h4 class="w-100 mt-1" id="imgset_btn">Image Viewer &#9776;</h4>
            </button>
          </div>
        </div>
        <div id="viewport_settings">
          <div id="viewports_man_container" v-for="(viewer, index) in cornerstoneViewers" :key="index">
            <DicomViewportControl :target-viewer="index"></DicomViewportControl>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import GeneralSettings from '@/components/studyDesign/GeneralSettings.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'
import cornerstone from 'cornerstone-core'

export default {
  name: 'Design',
  components: {
    DicomViewer,
    GeneralSettings,
    DicomViewportControl
  },
  computed: {
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
    },
    cornerstoneViewers () {
      return this.$store.getters['cornerstoneViewers/cornerstoneViewers']
    },
    viewerLayout () {
      // var colClass = 'grid-cols-' + this.$store.getters.viewerLayoutCols
      // var rowClass = 'grid-rows-' + this.$store.getters.viewerLayoutRows
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'grid-cols-5': this.$store.getters['openStudy/viewerLayoutCols'] === 5,
        'grid-cols-4': this.$store.getters['openStudy/viewerLayoutCols'] === 4,
        'grid-cols-3': this.$store.getters['openStudy/viewerLayoutCols'] === 3,
        'grid-cols-2': this.$store.getters['openStudy/viewerLayoutCols'] === 2,
        'grid-cols-1': this.$store.getters['openStudy/viewerLayoutCols'] === 1
      }
      return gridClass
    },
    refviewerNumb () {
      return this.$store.getters['openStudy/refviewerNumb']
    },
    refviewerLayout () {
      var gridClass = {
        flex: true,
        relative: true,
        grid: true,
        'gap-2': true,
        'grid-cols-1': this.$store.getters['openStudy/refviewerNumb'] === 1,
        'grid-cols-2': this.$store.getters['openStudy/refviewerNumb'] === 2,
        'grid-rows-1': true
      }
      return gridClass
    },
    cssStyle () {
      return {
        'background-color': this.$store.getters['openStudy/backgroundColor'],
        color: this.$store.getters['openStudy/textColor']
      }
    },
    viewerHeight () {
      return this.$store.getters['openStudy/viewerHeight']
    }
  },
  watch: {
    viewerLayout: {
      handler (oldLayout, newLayout) {
        this.setViewerHeight()
      },
      flush: 'post'
    },
    viewerHeight: {
      handler (oldHeight, newHeigth) {
        this.setViewerHeight()
      },
      flush: 'post'
    },
    viewerNumb: {
      handler () {
        this.setViewerHeight()
      },
      flush: 'post'
    }
  },
  mounted () {
    // watcher with flag immdiate runs to early => set height on mount
    this.setViewerHeight()
  },
  methods: {
    setViewerHeight () {
      var elements = cornerstone.getEnabledElements()
      var heigth
      elements.forEach((e) => {
        if (this.$store.getters['openStudy/viewerHeightAuto']) {
          heigth = Math.min(Number(e.element.clientWidth), Number(window.innerHeight - 350))
        } else {
          heigth = this.$store.getters['openStudy/viewerHeight']
        }
        e.element.style.height = heigth + 'px'
        cornerstone.resize(e.element)
        cornerstone.updateImage(e.element)
      })
      this.$store.commit('openStudy/viewerHeight', heigth)
    }
  }
}
</script>

<style>

</style>
