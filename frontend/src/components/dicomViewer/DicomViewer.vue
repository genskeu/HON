<template>
  <div class='relative grid grid-cols-1' @cornerstoneimagerendered.capture='(event) => displayStackIndex(event)'>
    <!-- image viewer :style='viewerSizeCSS' -->
    <div ref='viewer' class='dicom_viewer col-span-1 relative'
    @cornerstoneimagerendered="updateViewportSettings"
    @cornerstonetoolsmeasurementcompleted="addAnnotation"
    @cornerstonetoolsmeasurementmodified="updateAnnotation"
    @cornerstonetoolsmeasurementremoved="removeAnnotation">
      <!-- metadata viewer -->
      <div class='absolute top-0 left-0 p-4 text-white'>
        <ul class='list-none text-left'>
          <li v-for='(metadata, index) in stackMetadataTL' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute top-0 right-0 p-4 text-white'>
        <ul class='list-none text-right'>
          <li v-for='(metadata, index) in stackMetadataTR' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute bottom-0 left-0 p-4 text-white'>
        <ul id='viewer_bl' class='list-none text-left'>
          <li ref='slice_index'></li>
          <li v-for='(metadata, index) in stackMetadataBL' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute bottom-0 right-0 p-4 text-white'>
        <ul class='list-none text-right'>
          <li v-for='(metadata, index) in stackMetadataBR' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import Hammer from 'hammerjs'
import dicomParser from 'dicom-parser'
import cornerstoneMath from 'cornerstone-math'
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader'
import cornerstone from 'cornerstone-core'
import cornerstoneTools from 'cornerstone-tools'
// import axios from 'axios'

// Cornerstone DICOM Viewer Setup
cornerstoneWADOImageLoader.external.cornerstone = cornerstone
cornerstoneWADOImageLoader.external.dicomParser = dicomParser
cornerstoneTools.external.cornerstoneMath = cornerstoneMath
cornerstoneTools.external.cornerstone = cornerstone
cornerstoneTools.external.Hammer = Hammer

export default {
  name: 'DicomViewer',
  props: {
    viewerIndex: Number,
    viewerType: String
  },
  data () {
    return {
      // replace all by computed properties?
      activeImage: undefined,
      metaDataTL: ['x00100010', 'x00100020', 'x00081030', 'x0008103e'],
      metaDataTR: ['x00080080', 'x00081090', 'x00080090'],
      metaDataBL: ['x00200011', 'x00180050', 'x00201041'],
      metaDataBR: ['x00181151', 'x00281051', 'x00281051']
    }
  },
  computed: {
    viewerMetainfo () {
      return this.$store.getters['openStudy/viewerMetainfo']
    },
    stackMetadataTL () {
      var metadata = []
      if (this.activeImage && this.viewerMetainfo) {
        this.metaDataTL.forEach(string => {
          metadata.push({ tag: '', value: this.activeImage.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataTR () {
      var metadata = []
      if (this.activeImage && this.viewerMetainfo) {
        this.metaDataTR.forEach(string => {
          metadata.push({ tag: '', value: this.activeImage.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataBL () {
      var metadata = []
      if (this.activeImage && this.viewerMetainfo) {
        this.metaDataBL.forEach(string => {
          metadata.push({ tag: '', value: this.activeImage.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataBR () {
      var metadata = []
      if (this.activeImage && this.viewerMetainfo) {
        this.metaDataBR.forEach(string => {
          metadata.push({ tag: '', value: this.activeImage.data.string(string) })
        })
      }
      return metadata
    },
    stackDisplayed () {
      return this.$store.getters['imageViewers/stackDisplayed'](this.viewerIndex, this.viewerType)
    },
    viewerHeight () {
      return this.$store.getters['openStudy/viewerHeight']
    },
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
    },
    refviewerNumb () {
      return this.$store.getters['openStudy/refviewerNumb']
    },
    viewerLayout () {
      return this.$store.getters['openStudy/viewerLayoutCols']
    }
  },
  watch: {
    stackDisplayed: {
      handler (newStack) {
        if (newStack.csStack.imageIds.length > 0) {
          const stackToDisplay = {
            currentImageIdIndex: newStack.csStack.currentImageIdIndex,
            imageIds: newStack.csStack.imageIds
          }
          this.loadDisplayCornerstone(stackToDisplay, newStack.savedViewport, newStack.savedToolstate, newStack.savedSegmentation)
        } else {
          this.resetViewer()
        }
      }
    },
    viewerHeight: {
      handler () {
        this.updateViewerHeight()
      },
      flush: 'post'
    },
    viewerNumb: {
      handler () {
        this.updateViewerHeight()
      },
      flush: 'post'
    },
    viewerLayout: {
      handler () {
        this.updateViewerHeight()
      },
      flush: 'post'
    },
    refviewerNumb: {
      handler () {
        this.updateViewerHeight()
      },
      flush: 'post'
    }
  },
  created () {
  },
  mounted () {
    this.initViewer()
    this.updateViewerHeight()
  },
  activated () {
    this.updateViewerHeight()
  },
  beforeUnmount () {
    this.$store.commit('imageViewers/removeCornerstoneViewer', this.$refs.viewer)
  },
  methods: {
    initViewer () {
      // enable element for cornerstone
      cornerstone.enable(this.$refs.viewer, {
        renderer: 'webgl'
      })
      // disable right click on image viewer
      this.$refs.viewer.addEventListener(
        'contextmenu',
        function (e) {
          e.preventDefault()
        },
        false
      )
      // update vuex store
      const viewer = this.$store.getters['imageViewers/viewer'](this.viewerIndex, this.viewerType)
      if (viewer === undefined) {
        this.$store.commit('imageViewers/initViewer', { viewertype: this.viewerType })
      }
      this.$store.commit('imageViewers/updateViewerElement', {
        index: this.viewerIndex,
        element: this.$refs.viewer,
        viewertype: this.viewerType
      })
    },
    loadDisplayCornerstone (stack, viewportSaved = null, toolStateSaved = null, segDataSaved = null) {
      // load images and set the stack
      cornerstone.loadAndCacheImage(stack.imageIds[0])
        .then((image) => {
          this.activeImage = image
          // viewport
          var viewport = viewportSaved !== null ? viewportSaved : cornerstone.getDefaultViewportForImage(this.$refs.viewer, image)
          this.$store.commit('imageViewers/cornerstoneViewportUpdate', {
            viewport: viewport,
            index: this.viewerIndex,
            viewertype: this.viewerType
          })
          // display image
          cornerstone.displayImage(this.$refs.viewer, image, viewport)
          cornerstoneTools.addStackStateManager(this.$refs.viewer, ['stack'])
          cornerstoneTools.addToolState(this.$refs.viewer, 'stack', stack)
        })
        .then(() => {
          if (toolStateSaved) {
            toolStateSaved.forEach((state, index) => {
              if (state) {
                cornerstoneTools.globalImageIdSpecificToolStateManager.restoreImageIdToolState(stack.imageIds[index], state)
                // $(element).trigger('cornerstonetoolsmeasurementrestored', [stack.imageIds[index], element])
              }
            })
          }
        })
    },
    // when no image selected load a black blank screen
    resetViewer () {
      cornerstone.disable(this.$refs.viewer)
      console.log('disable')
      this.initViewer()
    },
    displayStackIndex (event) {
      if (this.stackDisplayed && this.stackDisplayed.csStack.imageIds.length > 1) {
        const index = event.detail.enabledElement.toolStateManager.toolState.stack.data[0].currentImageIdIndex + 1
        var slice = this.$refs.slice_index
        slice.innerHTML =
          'Stack Position:' +
          index +
         '/' +
          this.stackDisplayed.csStack.imageIds.length
      }
    },
    updateViewportSettings () {
      // bug fix where update Viewport settings is triggered and $refs.viewer returns null
      // open questions, why is event triggered? why is ref.viewer == null?
      // debugger // eslint-disable-line
      if (this.$refs.viewer !== null) {
        var viewport = cornerstone.getViewport(this.$refs.viewer)
        this.$store.commit('imageViewers/cornerstoneViewportUpdate', { viewport: viewport, index: this.viewerIndex, viewertype: this.viewerType })
      }
    },
    updateViewerHeight () {
      const element = this.$refs.viewer
      var heigth = this.viewerHeight
      if (this.$store.getters['openStudy/viewerHeightAuto']) {
        heigth = Math.min(Number(element.clientWidth), Number(window.innerHeight - 250))
      }
      element.style.height = heigth + 'px'
      cornerstone.resize(element)
      cornerstone.updateImage(element)
      this.$store.commit('openStudy/viewerHeight', heigth)
    },
    // will be called when measurment completed (add new or update form of exisiting roi)
    addAnnotation (e) {
      this.$emit('cornerstonetoolsmeasurementmodified', e)
      const toolName = e.detail.toolName
      // assumption: toolName only defined when new measurment added
      if (toolName) {
        const annotation = {
          toolName: toolName,
          measurementData: e.detail.measurementData
        }
        const uuid = e.detail.measurementData.uuid
        const toolType = e.detail.toolType
        this.$store.commit('imageViewers/addAnnotation', {
          annotation: annotation,
          type: toolType,
          uuid: uuid,
          index: this.viewerIndex,
          viewertype: this.viewerType
        })
      }
    },
    // will be called when measurment modified (update exisiting)
    updateAnnotation (e) {
      this.$emit('cornerstonetoolsmeasurementmodified', e)
      const toolName = e.detail.toolName
      const annotation = {
        toolName: toolName,
        measurementData: e.detail.measurementData
      }
      const uuid = e.detail.measurementData.uuid
      const toolType = e.detail.toolType
      this.$store.commit('imageViewers/updateAnnotation', {
        annotation: annotation,
        type: toolType,
        uuid: uuid,
        index: this.viewerIndex,
        viewertype: this.viewerType
      })
    },
    // will be called when measurment deleted (update exisiting)
    removeAnnotation (e) {
      const toolName = e.detail.toolName
      const annotation = {
        toolName: toolName,
        measurementData: e.detail.measurementData
      }
      const uuid = e.detail.measurementData.uuid
      const toolType = e.detail.toolType
      this.$store.commit('imageViewers/removeAnnotation', { annotation: annotation, type: toolType, uuid: uuid, index: this.viewerIndex, viewertype: this.viewerType })
    }
  }
}
</script>

<style>
</style>
