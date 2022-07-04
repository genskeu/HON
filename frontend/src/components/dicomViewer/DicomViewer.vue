<template>
  <div class='relative grid grid-rows-6 grid-cols-1' @cornerstoneimagerendered.capture='displayStackIndex'>
    <!-- image viewer :style='viewerSizeCSS' -->
    <div ref='viewer' class='dicom_viewer row-span-5 col-span-1 relative' @cornerstoneimagerendered="updateViewportSettings">
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
    <!-- image and mask selector -->
    <div class='flex items-center row-span-1 col-span-1 animate-fade-in-up'>
      <div class='flex grow items-center mr-2'>
        <label class='block text-sm font-medium'>Select your Image:
        </label>
        <select ref='image_select_id'
          class='border grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5' v-model="stackDisplayed">
          <option></option>
          <option v-for='stack in stacks' :key='stack.name' :value="stack">
            {{ stack.name }}
          </option>
        </select>
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
  props: {
    viewerIndex: Number
  },
  data () {
    return {
      // replace all by computed properties?
      activeImage: undefined,
      metaDataTL: ['x00100010', 'x00100020', 'x00081030', 'x0008103e'],
      metaDataTR: ['x00080080', 'x00081090', 'x00080090'],
      metaDataBL: ['x00200011', 'x00180050', 'x00201041'],
      metaDataBR: ['x00181151', 'x00281051', 'x00281051'],
      maskDisplayed: undefined
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
    stacks () {
      return this.$store.getters['openStudy/stacks']
    },
    stackDisplayed: {
      get () {
        return this.$store.getters['imageViewers/stackDisplayed'](this.viewerIndex)
      },
      set (stack) {
        // can be deleted after db change
        this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack, index: this.viewerIndex })
      }
    }
  },
  watch: {
    stackDisplayed: {
      handler (newStack) {
        var stack = {
          currentImageIdIndex: newStack.currentImageIdIndex,
          imageIds: [newStack.imageIds[0]]
        }
        stack.imageIds[0] = stack.imageIds[0].replace('127.0.0.1', 'localhost:5000')
        this.loadDisplayCornerstone(stack).then(() => {
        })
      }
    }
  },
  created () {
  },
  mounted () {
    this.initViewer()
    this.$store.commit('imageViewers/cornerstoneViewer', {
      element: this.$refs.viewer,
      stackDisplayed: undefined,
      viewportSettings: {
        windowWidth: Number,
        windowCenter: Number,
        scale: Number,
        posX: Number,
        posY: Number,
        rotation: Number
      },
      toolState: {}
    })
  },
  beforeUnmount () {
    this.$store.commit('imageViewers/removeCornerstoneViewer', this.$refs.viewer)
  },
  methods: {
    initViewer () {
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
    },
    loadDisplayCornerstone (stack) {
      // load images and set the stack
      const promise = cornerstone.loadImage(stack.imageIds[0]).then((image) => {
        this.activeImage = image
        cornerstone.displayImage(this.$refs.viewer, image)
        cornerstoneTools.addStackStateManager(this.$refs.viewer, ['stack'])
        cornerstoneTools.addToolState(this.$refs.viewer, 'stack', stack)
        var viewport = cornerstone.getViewport(this.$refs.viewer)
        this.$store.commit('imageViewers/cornerstoneViewportUpdate', { viewport: viewport, index: this.viewerIndex })
      })
      return promise
    },
    displayStackIndex () {
      if (this.stackDisplayed) {
        var slice = this.$refs.slice_index
        slice.innerHTML =
          'Image:' +
          (this.stackDisplayed.currentImageIdIndex + 1) +
         '/' +
          this.stackDisplayed.imageIds.length
      }
    },
    updateViewportSettings () {
      var viewport = cornerstone.getViewport(this.$refs.viewer)
      this.$store.commit('imageViewers/cornerstoneViewportUpdate', { viewport: viewport, index: this.viewerIndex })
    }
  }
}
</script>

<style>
</style>
