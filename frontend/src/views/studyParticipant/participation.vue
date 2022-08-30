<template>
    <div class="container-fluid pt-4" id="content" :style="cssStyle">
        <div class="row mx-auto">
            <!-- Imgsets -->
            <div class="col-lg-10 pt-1" id="imgset_creation">
                <!-- Create Image Sets -->
                <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
                <div id="imgset" class="mx-auto px-0 w-100">
                    <!--Images -->
                    <DicomViewerTools :toolsMousekeysp="toolsMousekeysAvailable" :toolsMousewheelp="toolsMousewheelAvailable" class="sticky-top"></DicomViewerTools>
                    <div id="ref-stacks" :class="refviewerLayout">
                        <dicom-viewer v-for="index in refviewerNumb" :key="index"></dicom-viewer>
                    </div>
                    <div id="stacks" :class="viewerLayout">
                        <div v-for="index in viewerNumb" :key="index">
                          <dicom-viewer :viewer-index="index - 1" :style="viewerHeight"></dicom-viewer>
                          <Votebtn class="my-4"></Votebtn>
                        </div>
                    </div>
                    <div>
                    </div>
                </div>
            </div>
            <!-- sidebar for design, viewport settings, scales etc (rigth) -->
            <div class="col-lg-2 pt-1 overflow-auto sticky-top" id="sidebar">
              <Instructions></Instructions>
              <Scales></Scales>
            </div>
        </div>
      <Progressbar></Progressbar>
    </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import DicomViewerTools from '@/components/dicomViewer/DicomViewerTools.vue'
import Instructions from '@/components/studyParticipation/Instructions.vue'
import Scales from '@/components/studyParticipation/Scales.vue'
import Progressbar from '@/components/studyParticipation/progressBar.vue'
import Votebtn from '@/components/studyParticipation/Votebtn.vue'

export default {
  components: {
    DicomViewer,
    DicomViewerTools,
    Instructions,
    Scales,
    Progressbar,
    Votebtn
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
    },
    toolsMousekeys () {
      return this.$store.getters['imageViewers/toolsMousekeys']
    },
    toolsMousewheel () {
      return this.$store.getters['imageViewers/toolsMousewheel']
    },
    toolsMousekeysAvailable () {
      var toolsAvailable = this.$store.getters['openStudy/tools']
      var tools = {}
      toolsAvailable.forEach(tool => {
        if (Object.keys(this.toolsMousekeys).includes(tool.cs_name)) {
          tools[tool.cs_name] = this.toolsMousekeys[tool.cs_name]
        }
      })
      return tools
    },
    toolsMousewheelAvailable () {
      var toolsAvailable = this.$store.getters['openStudy/tools']
      var tools = {}
      toolsAvailable.forEach(tool => {
        if (Object.keys(this.toolsMousewheel).includes(tool.cs_name)) {
          tools[tool.cs_name] = this.toolsMousewheel[tool.cs_name]
        }
      })
      return tools
    }
  },
  watch: {
    imgsetActive: {
      handler (newImgset) {
        newImgset.imageStacks.forEach((stack, index) => {
          // ensure same structure as select menu values
          stack.csStack.name = stack.name
          this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack.csStack, index: index })
        })
      }
    }
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
