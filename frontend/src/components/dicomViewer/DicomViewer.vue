<template>
  <div class='relative grid grid-rows-6 grid-cols-1' @cornerstoneimagerendered.capture='displayStackIndex'>
    <!-- image viewer :style='viewerSizeCSS' -->
    <div ref='viewer' class='dicom_viewer row-span-5 col-span-1 relative' >
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
          class='border grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5'
          @change='loadStackOnSelect'>
          <option></option>
          <option v-for='stack in getStacknames.sort()' :key='stack'>
            {{ stack }}
          </option>
        </select>
      </div>
      <!-- select menu for masks -->
      <!-- <div class='flex grow items-center'>
        <label class='block text-sm font-medium text-gray-900 dark:text-gray-400'>Select your Mask:
        </label>

        <select ref='maskSelect_id'
          class='bg-gray-50 border border-gray-300 text-gray-900 grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
          @change='loadMaskOnSelect'>
          <option></option>
          <option disabled>Grundtruth Masks</option>
          <option v-for='mask in gtMasks' :key='mask' mask-type='gt'>
            {{ mask }}
          </option>
          <option disabled>Pred Masks (output)</option>
          <option v-for='mask in predMasks' :key='mask' mask-type='pred'>
            {{ mask }}
          </option>
        </select>
      </div> -->
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
      stack_displayed: undefined,
      current_stack: undefined,
      metaDataTL: ['x00100010', 'x00100020', 'x00081030', 'x0008103e'],
      metaDataTR: ['x00080080', 'x00081090', 'x00080090'],
      metaDataBL: ['x00200011', 'x00180050', 'x00201041'],
      metaDataBR: ['x00181151', 'x00281051', 'x00281051'],
      maskDisplayed: undefined
    }
  },
  computed: {
    // used for mask display
    // getMasknames () {
    //   return this.gtMasks.concat(this.predMasks)
    // },
    viewerMetainfo: {
      get () {
        return this.$store.getters.viewerMetainfo
      }
    },
    getStacknames () {
      if (this.$store.state.openStudy) {
        const imageNames = this.$store.state.openStudy.images.map(
          obj => {
            return obj.name
          }
        )
        return imageNames
      } else {
        return []
      }
    },
    stackMetadataTL () {
      var metadata = []
      if (this.stack_displayed && this.viewerMetainfo) {
        this.metaDataTL.forEach(string => {
          metadata.push({ tag: '', value: this.stack_displayed.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataTR () {
      var metadata = []
      if (this.stack_displayed && this.viewerMetainfo) {
        this.metaDataTR.forEach(string => {
          metadata.push({ tag: '', value: this.stack_displayed.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataBL () {
      var metadata = []
      if (this.stack_displayed && this.viewerMetainfo) {
        this.metaDataBL.forEach(string => {
          metadata.push({ tag: '', value: this.stack_displayed.data.string(string) })
        })
      }
      return metadata
    },
    stackMetadataBR () {
      var metadata = []
      if (this.stack_displayed && this.viewerMetainfo) {
        this.metaDataBR.forEach(string => {
          metadata.push({ tag: '', value: this.stack_displayed.data.string(string) })
        })
      }
      return metadata
    }
  },
  watch: {
  },
  created () {
  },
  mounted () {
    this.initViewer()
    this.$store.commit('cornerstoneViewers/cornerstoneViewer', {
      element: this.$refs.viewer,
      viewport: {},
      toolState: {}
    })
  },
  beforeUnmount () {
    this.$store.commit('cornerstoneViewers/removeCornerstoneViewer', this.$refs.viewer)
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
    loadStackOnSelect (event) {
      const stackName = event.target.value
      const baseUrl = this.$store.state.openStudy.images.find(image => image.name === stackName).base_url.replace('127.0.0.1', 'localhost:5000')
      if (stackName !== '') {
        const data = { name: stackName, size: 0, data: [stackName] }
        const stacks = this.parseImagesCornerstone(data.data, baseUrl)
        this.loadDisplayCornerstone(stacks[0], stacks[1], 'input').then(() => {
        })
      }
    },
    parseImagesCornerstone (images, baseUrl) {
      const scheme = 'wadouri'
      const imageIds = images.map(
        (image) =>
         `${scheme}:${baseUrl}${image}`
      )
      const stack = {
        currentImageIdIndex: 0,
        imageIds
      }
      return [imageIds, stack]
    },
    loadDisplayCornerstone (imageIds, stack) {
      // load images and set the stack
      const promise = cornerstone.loadImage(imageIds[0]).then((image) => {
        this.stack_displayed = image
        this.current_stack = stack
        cornerstone.displayImage(this.$refs.viewer, image)
        cornerstoneTools.addStackStateManager(this.$refs.viewer, ['stack'])
        cornerstoneTools.addToolState(this.$refs.viewer, 'stack', stack)
        var viewport = cornerstone.getViewport(this.$refs.viewer)
        this.$store.commit('cornerstoneViewers/cornerstoneViewportUpdate', { viewport: viewport, index: this.viewerIndex })
      })
      return promise
    },
    displayStackIndex () {
      const stack = this.current_stack
      if (stack) {
        var slice = this.$refs.slice_index
        slice.innerHTML =
          'Image:' +
          (stack.currentImageIdIndex + 1) +
         '/' +
          stack.imageIds.length
      }
    }
    /*     loadMaskOnSelect (event) {
      const segMaskName = event.target.value
      var segmentation = cornerstoneTools.getModule('segmentation')
      const element = this.$refs.viewer
      segmentation.setters.activeLabelmapIndex(this.$refs.viewer, 0)
      var labelmap3D = segmentation.getters.labelmap3D(element, 0)
      const masktype =
        event.target.selectedOptions[0].getAttribute('mask-type')
      var url = 'http://localhost:5000/maskdata/' + masktype + '/' + segMaskName
      if (segMaskName) {
        axios.get(url).then((response) => {
          var segData = response.data.maskData
          labelmap3D.labelmaps2D = Array(segData.length)
          segData.forEach(function (seg, index) {
            if (seg) {
              var l2dforImageIdIndex = {
                pixelData: Uint16Array.from(JSON.parse(seg)),
                segmentsOnLabelmap: [0, 1, 2]
              }
              labelmap3D.labelmaps2D.splice(index, 0, l2dforImageIdIndex)
            }
          })
          cornerstone.updateImage(element)
        }).catch(error => {
          alert('Mask not found!')
          console.log(error)
        })
      } else {
        labelmap3D.labelmaps2D = []
        cornerstone.updateImage(element)
      }
    },
    filterMasks (volName) {
      var maskSelect = this.$refs.maskSelect_id
      maskSelect.value = ''
      for (var option of maskSelect) {
        if (
          option.value.includes(volName) |
          option.value.includes('gt') |
          (option.value === '') |
          (option.disabled === true)
        ) {
          option.removeAttribute('hidden')
        } else {
          option.setAttribute('hidden', 'hidden')
        }
      }
    } */
  }
}
</script>

<style>
</style>
