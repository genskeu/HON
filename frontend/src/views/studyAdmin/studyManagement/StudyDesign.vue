<template>
  <div class="container-fluid" id="content" :style="cssStyle">
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
              <DicomViewerTools class="mb-2"></DicomViewerTools>
              <span v-if="refviewerNumb" class="badge bg-secondary mx-auto w-100">
                <h4 class="">Reference-Stack(s)</h4>
              </span>
              <div id="ref-stacks" :class="refviewerLayout">
                <dicom-viewer v-for="index in refviewerNumb" :key="index"></dicom-viewer>
              </div>
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Stack(s)</h4>
              </span>
              <div id="stacks" :class="viewerLayout">
                <div v-for="index in viewerNumb" :key="index">
                  <h4>Image Viewer {{index}}</h4>
                  <dicom-viewer :viewer-index="index-1"></dicom-viewer>
                </div>
              </div>
            <div>
          </div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2 pt-1 overflow-auto vh-100">
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
        <ImgsetNav class="w-100"></ImgsetNav>
        <!-- default viewport settings -->
        <div id="viewport_settings_container" class="w-100 mt-2" title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                        Each viewport can be controlled individually.
                        To globally control viewport settings use the defaults submenu.">
          <div class="row mt-1 mx-auto">
            <button class="btn btn-dark col-12 mb-2" data-bs-toggle="collapse" data-bs-target="#viewport_settings"
              aria-expanded="true" aria-controls="viewport_settings">
              <h4 class="w-100 mt-1" id="imgset_btn">Image Viewer &#9776;</h4>
            </button>
          </div>
        </div>
        <div id="viewport_settings" class="collapse show">
          <div id="viewports_man_container" v-for="(viewer, index) in imageViewers" :key="index">
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
import DicomViewerTools from '@/components/dicomViewer/DicomViewerTools.vue'
import ImgsetNav from '@/components/studyDesign/ImgsetNav.vue'

import cornerstone from 'cornerstone-core'

export default {
  name: 'Design',
  components: {
    DicomViewer,
    GeneralSettings,
    DicomViewportControl,
    DicomViewerTools,
    ImgsetNav
  },
  computed: {
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
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
    imageViewers () {
      return this.$store.getters['imageViewers/cornerstoneViewers']
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
      handler () {
        this.setViewerHeight()
      },
      flush: 'post'
    },
    viewerHeight: {
      handler () {
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
    // fct should be moved to dicomviewer.vue
    setViewerHeight () {
      var elements = cornerstone.getEnabledElements()
      var heigth
      elements.forEach((e) => {
        if (this.$store.getters['openStudy/viewerHeightAuto']) {
          heigth = Math.min(Number(e.element.clientWidth), Number(window.innerHeight - 200))
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
