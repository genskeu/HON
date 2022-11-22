<template>
  <div class="container-fluid pt-4" id="content" :style="cssStyle">
      <div v-if="studyFinished">Finished with Study.</div>
      <Description v-if="studyDescription" id="studyDescription"></Description>
      <div v-if="!studyFinished" class="row mx-auto">
      <!-- Imgsets -->
      <div class="col-lg-10 pt-1" id="imgset_creation">
        <!-- Create Image Sets -->
        <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
        <div id="imgset" class="mx-auto px-0 w-100">
          <!--Images -->
          <DicomViewerTools class="sticky-top"></DicomViewerTools>
          <div id="ref-stacks" :class="refviewerLayout">
            <div v-for="index in refviewerNumb" :key="index">
                <dicom-viewer viewer-type="refviewers" :viewer-index="index-1"></dicom-viewer>
            </div>
          </div>
          <div id="stacks" :class="viewerLayout">
            <div v-for="index in viewerNumb" :key="index">
              <dicom-viewer @cornerstonetoolsmeasurementmodified="(event) => applySize(event)" viewer-type="viewers" :viewer-index="index - 1">
              </dicom-viewer>
              <Votebtn :viewer-index="index-1" class="my-2"></Votebtn>
            </div>
          </div>
          <div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2 pt-1 overflow-auto sticky-top" id="sidebar">
        <button v-if="studyDescription" class="btn-secondary btn w-100 mb-1" data-bs-toggle="modal" data-bs-target="#studyDescription">Show Description
        </button>
        <Instructions></Instructions>
        <Scales></Scales>
      </div>
      </div>
      <Progressbar></Progressbar>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'
import DicomViewerTools from '@/components/studyParticipation/DicomViewerTools.vue'
import Instructions from '@/components/studyParticipation/Instructions.vue'
import Scales from '@/components/studyParticipation/Scales.vue'
import Progressbar from '@/components/studyParticipation/progressBar.vue'
import Votebtn from '@/components/studyParticipation/Votebtn.vue'
import Description from '@/components/studyParticipation/Description.vue'

export default {
  name: 'participation',
  components: {
    DicomViewer,
    DicomViewerTools,
    Instructions,
    Scales,
    Progressbar,
    Votebtn,
    Description
  },
  data () {
    return {
    }
  },
  mounted () {
    // get starting imgset (first without results)
    const idsImgsetFinished = this.resultsCurrentUser.map(result => result.imgset_id)
    const imgsetDisplayed = this.imgsets.find(imgset => !idsImgsetFinished.includes(imgset.id))
    this.$store.commit('currentStudy/imgsetDisplayed', imgsetDisplayed)
  },
  activated () {
    const idsImgsetFinished = this.resultsCurrentUser.map(result => result.imgset_id)
    const imgsetDisplayed = this.imgsets.find(imgset => !idsImgsetFinished.includes(imgset.id))
    this.$store.commit('currentStudy/imgsetDisplayed', imgsetDisplayed)
  },
  deactivated () {
  },
  computed: {
    viewerNumb () {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    viewerLayout () {
      // var colClass = 'grid-cols-' + this.$store.getters.viewerLayoutCols
      // var rowClass = 'grid-rows-' + this.$store.getters.viewerLayoutRows
      var gridClass = {
        'mb-4': true,
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
    imgsets () {
      return this.$store.getters['currentStudy/imgsets']
    },
    resultsCurrentUser () {
      return this.$store.getters['currentStudy/resultsCurrentUser']
    },
    imgsetDisplayed () {
      return this.$store.getters['currentStudy/imgsetDisplayed']
    },
    toolsParticipant () {
      return this.$store.getters['currentStudy/tools']
    },
    studyDescription () {
      const description = this.$store.getters['currentStudy/studyDescription']
      if (description) {
        return description.length > 0
      } else {
        return 0
      }
    },
    studyFinished () {
      return this.resultsCurrentUser.length === this.imgsets.length
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    }
  },
  watch: {
    imgsetDisplayed: {
      handler (newImgset) {
        // code could be moved to store to avoid duplication?
        if (newImgset) {
          const viewers = this.refimageViewers.concat(this.imageViewers)
          // itterate over viewers and display stack according to div_id
          // if no stack found reset stack to trigger viewer reset
          viewers.forEach((viewer, index) => {
            var stack = newImgset.image_stacks.find(stack => stack.div_id === 'dicom_img_' + index)
            if (stack === undefined) {
              stack = {
                cs_stack: {
                  imageIds: [],
                  currentImageIdIndex: Number
                },
                name: String,
                savedSegmentation: undefined,
                savedToolstate: undefined,
                savedViewport: undefined
              }
            }
            var viewertype = this.refimageViewers.includes(viewer) ? 'refviewers' : 'viewers'
            var viewerindex = this.refimageViewers.includes(viewer) ? index : index - this.refimageViewers.length
            const stackData = {
              stack_id: stack.stack_id,
              name: stack.name,
              stackDisplayed: stack.cs_stack,
              savedViewport: stack.viewport,
              savedToolstate: stack.tool_state,
              savedSegmentation: stack.seg_data,
              index: viewerindex,
              viewertype: viewertype
            }
            this.$store.commit('imageViewers/stackDisplayed', stackData)
          })
        } else {
          const emptyStack = {
            cs_stack: {
              currentImageIdIndex: Number,
              imageIds: []
            },
            name: String
          }
          const viewers = this.refimageViewers.concat(this.imageViewers)
          // itterate over viewers and display stack according to div_id
          // if no stack found reset stack to trigger viewer reset
          viewers.forEach((viewer, index) => {
            var viewertype = this.refimageViewers.includes(viewer) ? 'refviewers' : 'viewers'
            var viewerindex = this.refimageViewers.includes(viewer) ? index : index - this.refimageViewers.length
            const stackData = {
              name: emptyStack.name,
              stackDisplayed: emptyStack.cs_stack,
              index: viewerindex,
              viewertype: viewertype
            }
            this.$store.commit('imageViewers/stackDisplayed', stackData)
          })
        }
      }
    },
    resultsCurrentUser: {
      deep: true,
      handler () {
        const idsImgsetFinished = this.resultsCurrentUser.map(result => result.imgset_id)
        const imgsetDisplayed = this.imgsets.find(imgset => !idsImgsetFinished.includes(imgset.id))
        this.$store.commit('currentStudy/imgsetDisplayed', imgsetDisplayed)
      }
    }
  },
  methods: {
    // enforece ann too size limits (settings)
    applySize (event) {
      var handles = event.detail.measurementData.handles
      const toolname = event.detail.toolName
      if (toolname === undefined) { return false }
      const tool = this.toolsParticipant.find(tool => toolname.includes(tool.cs_name))
      if (tool && tool.settings && tool.settings.size) {
        const size = Number(tool.settings.size)
        var startX = handles.start.x
        var startY = handles.start.y
        var endX = handles.end.x
        var endY = handles.end.y
        const distance = Math.sqrt(Math.pow(startX - endX, 2) + Math.pow(startY - endY, 2))
        if (Math.round(distance) !== size) {
          var endX2 = Math.sqrt(Math.pow(size, 2) / 2) + startX
          var endY2 = Math.sqrt(Math.pow(size, 2) / 2) + startY
          // var distance2 = Math.sqrt(Math.pow(startX - endX2, 2) + Math.pow(startY - endY2, 2))
          handles.end.x = endX2
          handles.end.y = endY2
        }
      }
    }
  }
}
</script>

<style>
#sidebar {
  height: 85vh;
}
</style>
