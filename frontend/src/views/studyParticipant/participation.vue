<template>
    <div class="container-fluid" id="content" :style="cssStyle">
        <div class="row mx-auto">
            <!-- Imgsets -->
            <div class="col-lg-10 pt-1" id="imgset_creation">
                <!-- Create Image Sets -->
                <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
                <div id="imgset" class="mx-auto px-0 w-100">
                    <!--Images -->
                    <DicomViewerTools></DicomViewerTools>
                    <div id="ref-stacks" :class="refviewerLayout">
                        <dicom-viewer v-for="index in refviewerNumb" :key="index"></dicom-viewer>
                    </div>
                    <div id="stacks" :class="viewerLayout">
                        <dicom-viewer v-for="index in viewerNumb" :key="index" :viewer-index="index - 1" :style="viewerHeight"></dicom-viewer>
                    </div>
                    <div>
                    </div>
                </div>
            </div>
            <!-- sidebar for design, viewport settings, scales etc (rigth) -->
            <div class="col-lg-2 pt-1">
            </div>
        </div>
    </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import DicomViewerTools from '@/components/dicomViewer/DicomViewerTools.vue'
import cornerstone from 'cornerstone-core'

export default {
  components: {
    DicomViewer,
    DicomViewerTools
  },
  data () {
    return {
      imgsetActive: undefined
    }
  },
  mounted () {
    this.imgsetActive = this.imgsets[0]
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
    cssStyle () {
      return {
        'background-color': this.$store.getters['openStudy/backgroundColor'],
        color: this.$store.getters['openStudy/textColor']
      }
    },
    viewerHeight () {
      return {
        height: this.$store.getters['openStudy/viewerHeight'] + 'px'
      }
    },
    imgsets () {
      return this.$store.getters['openStudy/imgsets']
    }
  },
  watch: {
    imgsetActive: {
      handler (newImgset) {
        newImgset.image_stacks.forEach((stack, index) => {
          // ensure same structure as select menu values
          stack.cs_stack.name = stack.name
          this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack.cs_stack, index: index })
        })
      }
    }
  },
  methods: {
    setViewerHeight () {
      var elements = cornerstone.getEnabledElements()
      var heigth
      elements.forEach((e) => {
        if (this.$store.getters['openStudy/viewerHeightAuto']) {
          heigth = Math.min(Number(e.element.clientWidth), Number(window.innerHeight - 420))
        } else {
          heigth = this.$store.getters['openStudy/viewerHeight']
        }
        e.element.style.height = heigth + 'px'
        cornerstone.resize(e.element)
        cornerstone.updateImage(e.element)
      })
    }
  }
}
</script>

<style>

</style>
