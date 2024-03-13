<template>
  <div class='tw-relative tw-grid tw-grid-cols-1' @cornerstoneimagerendered.capture='(event) => displayStackIndex(event)'>
    <!-- image viewer :style='viewerSizeCSS' -->
    <div :id="'dicom-viewer-'+viewerIndex" ref='viewer' class='dicom_viewer tw-col-span-1 tw-relative'
    @cornerstoneimagerendered="updateViewportSettings"
    @cornerstonetoolsmeasurementcompleted="addAnnotation"
    @cornerstonetoolsmeasurementmodified="updateAnnotation"
    @cornerstonetoolsmeasurementremoved="removeAnnotation">
      <!-- metadata viewer -->
      <div class='tw-absolute tw-top-0 tw-left-0 p-4 text-white'>
        <ul class='tw-list-none tw-text-left'>
          <li v-for='(metadata, index) in stackMetadataTL' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='tw-absolute tw-top-0 tw-right-0 p-4 text-white'>
        <ul class='tw-list-none tw-text-right'>
          <li v-for='(metadata, index) in stackMetadataTR' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div v-if="loading" tabindex="-1">
        <div class="tw-h-10 tw-w-10 mx-auto spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class='tw-absolute tw-bottom-0 tw-left-0 p-4 text-white'>
        <ul id='viewer_bl' class='tw-list-none tw-text-left'>
          <li ref='windowSettings'>{{this.windowSettings}}</li>
          <li ref='slice_index'></li>
          <li v-for='(metadata, index) in stackMetadataBL' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='tw-absolute tw-bottom-0 tw-right-0 p-4 text-white'>
        <ul class='tw-list-none tw-text-right'>
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
      loading: false,
      metaDataTL: ['x00100010', 'x00100020', 'x00081030', 'x0008103e'],
      metaDataTR: ['x00080080', 'x00081090', 'x00080090'],
      metaDataBL: ['x00200011', 'x00180050', 'x00201041'],
      metaDataBR: ['x00181151', 'x00281051', 'x00281051']
    }
  },
  computed: {
    viewerMetainfo () {
      return this.$store.getters['currentStudy/viewerMetainfo']
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
      return this.$store.getters['currentStudy/viewerHeight']
    },
    viewerNumb () {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    refviewerNumb () {
      return this.$store.getters['currentStudy/refviewerNumb']
    },
    viewerLayout () {
      return this.$store.getters['currentStudy/viewerLayoutCols']
    },
    windowSettings () {
      if (this.stackDisplayed && this.stackDisplayed.csStack.imageIds.length) {
        const ww = this.$store.getters['imageViewers/cornerstoneViewerWindowWidth'](this.viewerIndex, this.viewerType)
        const wc = this.$store.getters['imageViewers/cornerstoneViewerWindowCenter'](this.viewerIndex, this.viewerType)
        return 'WW: ' + Math.round(ww) + ' WC: ' + Math.round(wc)
      } else {
        return ''
      }
    }
  },
  watch: {
    stackDisplayed: {
      handler (newStack) {
        if (newStack && newStack.csStack.imageIds.length > 0) {
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
    this.updateStore()
    this.updateViewerHeight()
    const fontFamily =
    'Work Sans, Roboto, OpenSans, HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, Lucida Grande, sans-serif';

    cornerstoneTools.textStyle.setFont(`16px ${fontFamily}`);

    // Set the tool width
    cornerstoneTools.toolStyle.setToolWidth(2);

    // Set color for inactive tools
    cornerstoneTools.toolColors.setToolColor('rgb(150, 150, 0)');

    // Set color for active tools
    cornerstoneTools.toolColors.setActiveColor('rgb(0, 200, 0)');
  },
  activated () {
    this.updateViewerHeight()
    this.updateStore()
  },
  beforeUnmount () {
    this.$store.commit('imageViewers/removeCornerstoneViewer', this.$refs.viewer)
    cornerstone.disable(this.$refs.viewer)
  },
  methods: {
    initViewer () {
      // enable element for cornerstone
      cornerstone.enable(this.$refs.viewer)
      // disable right click on image viewer
      this.$refs.viewer.addEventListener(
        'contextmenu',
        function (e) {
          e.preventDefault()
        },
        false
      )
    },
    updateStore () {
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
    loadDisplayCornerstone (stack, viewportSaved = null, toolStateSaved = null) {
      // load images and set the stack
      this.loading = true
      // bugs with chromium stack.imageIds.forEach((imageId) => cornerstone.loadAndCacheImage(imageId))
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
          // ensure no toolstate shown for image (might be present from previously loading the same image)
          } else {
            const toolNames = Object.keys(cornerstoneTools.store.state.globalTools)
            toolNames.forEach((toolName) => {
              cornerstoneTools.clearToolState(this.$refs.viewer, toolName)
            })
          }
        })
        .finally(() => {
          this.loading = false
      })
    },
    // when no image selected load a black blank screen
    resetViewer () {
      cornerstone.disable(this.$refs.viewer)
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
      if (this.$refs.viewer !== null) {
        var viewport = cornerstone.getViewport(this.$refs.viewer)
        this.$store.commit('imageViewers/cornerstoneViewportUpdate', { viewport: viewport, index: this.viewerIndex, viewertype: this.viewerType })
      }
    },
    updateViewerHeight () {
      const element = this.$refs.viewer
      var heigth = this.viewerHeight
      if (this.$store.getters['currentStudy/viewerHeightAuto']) {
        heigth = Math.min(Number(element.clientWidth), Number(window.innerHeight - 260))
      }
      element.style.height = heigth + 'px'
      cornerstone.resize(element)
      cornerstone.updateImage(element)
      this.$store.commit('currentStudy/viewerHeight', heigth)
    },
    // will be called when measurment completed (add new or update form of exisiting roi)
    addAnnotation (e) {
      e.image = this.activeImage
      this.$emit('cornerstonetoolsmeasurementmodified', e)
      const toolName = e.detail.toolName
      // assumption: toolName only defined when new measurment added
      if (toolName) {
        const annotation = {
          toolName: toolName,
          measurementData: e.detail.measurementData
        }
        const uuid = e.detail.measurementData.uuid
        const toolType = e.detail.toolType.split('-')[0]
        const element = this.$refs.viewer
        e.detail.toolType = toolType

        if (this.isLabeled(e) & this.numbAnns(e, element) > 1) {
          cornerstoneTools.removeToolState(element, toolName, e.detail.measurementData)
        } else {
          this.$store.commit('imageViewers/addAnnotation', {
            annotation: annotation,
            type: toolType,
            uuid: uuid,
            index: this.viewerIndex,
            viewertype: this.viewerType
          })
        }
      }
    },
    // will be called when measurment modified (update exisiting)
    updateAnnotation (e) {
      e.image = this.activeImage
      this.$emit('cornerstonetoolsmeasurementmodified', e)
      const toolName = e.detail.toolName
      const annotation = {
        toolName: toolName,
        measurementData: e.detail.measurementData
      }
      const uuid = e.detail.measurementData.uuid
      const toolType = e.detail.toolType.split('-')[0]
      e.detail.toolType = toolType

      this.$store.commit('imageViewers/updateAnnotation', {
        annotation: annotation,
        type: toolType,
        uuid: uuid,
        index: this.viewerIndex,
        viewertype: this.viewerType
      })
    },
    // will be called when measurment deleted
    removeAnnotation (e) {
      const toolName = e.detail.toolName
      const annotation = {
        toolName: toolName,
        measurementData: e.detail.measurementData
      }
      const uuid = e.detail.measurementData.uuid
      const toolType = e.detail.toolType.split('-')[0]
      this.$store.commit('imageViewers/removeAnnotation', {
        annotation: annotation,
        type: toolType,
        uuid: uuid,
        index: this.viewerIndex,
        viewertype: this.viewerType
      })
    },
    // helper to prevent double measurments for labeled tools
    isLabeled (event) {
      return event.detail.toolName.split('-').length > 1
    },
    numbAnns (event, element) {
      const imageIds = cornerstoneTools.getToolState(element, 'stack').data[0].imageIds
      const toolState = imageIds.map((id) => {
        return cornerstoneTools.globalImageIdSpecificToolStateManager.getImageIdToolState(id, event.detail.toolName)
      })
      const toolStateFiltered = toolState.filter((state) => state !== undefined)
      const lengthToolState = toolStateFiltered.reduce((length, state) => {
        return length + state.data.length
      }, 0)
      return lengthToolState
    }
    // e.detail.measurementData.handles.textBox.x += 200
    // e.detail.measurementData.handles.textBox.hasMoved = true
    // console.log(e.detail.measurementData.handles.textBox)
  }
}
</script>

<style>
</style>
