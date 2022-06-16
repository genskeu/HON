<template>
  <div class='relative grid grid-rows-6 grid-cols-1' @cornerstoneimagerendered.capture='displayStackIndex' style="min-height: 520px;">
    <!-- image viewer -->
    <div ref='viewer' class='dicom_viewer row-span-5 col-span-1 relative'>
      <!-- metadata viewer -->
      <div class='absolute top-0 left-0 p-4 text-white'>
        <ul class='list-none text-left'>
          <li v-for='(metadata, index) in stack_meta_data.tl' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute top-0 right-0 p-4 text-white'>
        <ul class='list-none text-right'>
          <li v-for='(metadata, index) in stack_meta_data.tr' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute bottom-0 left-0 p-4 text-white'>
        <ul id='viewer_bl' class='list-none text-left'>
          <li ref='slice_index'></li>
          <li v-for='(metadata, index) in stack_meta_data.bl' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
      <div class='absolute bottom-0 right-0 p-4 text-white'>
        <ul class='list-none text-right'>
          <li v-for='(metadata, index) in stack_meta_data.br' :key='index'>
            {{ metadata.tag }} {{ metadata.value }}
          </li>
        </ul>
      </div>
    </div>
    <!-- image and mask selector -->
    <div class='flex items-center row-span-1 col-span-1 animate-fade-in-up'>
      <div class='flex grow items-center mr-2'>
        <label class='block text-sm font-medium text-gray-900 dark:text-gray-400'>Select your Image:
        </label>
        <select ref='image_select_id'
          class='bg-gray-50 border border-gray-300 text-gray-900 grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
          @change='loadStackOnSelect'>
          <option></option>
          <option v-for='stack in getStacknames.sort()' :key='stack'>
            {{ stack }}
          </option>
        </select>
      </div>
      <div class='flex grow items-center'>
        <label class='block text-sm font-medium text-gray-900 dark:text-gray-400'>Select your Mask:
        </label>

        <select ref='maskSelect_id'
          class='bg-gray-50 border border-gray-300 text-gray-900 grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
          @change='loadMaskOnSelect'>
          <option></option>
          <option disabled>Grundtruth Masks</option>
          <option v-for='mask in gt_masks' :key='mask' mask-type='gt'>
            {{ mask }}
          </option>
          <option disabled>Pred Masks (output)</option>
          <option v-for='mask in pred_masks' :key='mask' mask-type='pred'>
            {{ mask }}
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
import axios from 'axios'

// Cornerstone DICOM Viewer Setup
cornerstoneWADOImageLoader.external.cornerstone = cornerstone
cornerstoneWADOImageLoader.external.dicomParser = dicomParser
cornerstoneTools.external.cornerstoneMath = cornerstoneMath
cornerstoneTools.external.cornerstone = cornerstone
cornerstoneTools.external.Hammer = Hammer

export default {
  data () {
    return {
      viewer_id: 'test',
      element: undefined,
      stack_select_id: 'test_sel',
      stack_displayed: undefined,
      stack_meta_data: {
        tl: undefined,
        tr: undefined,
        bl: undefined,
        br: undefined
      },
      current_stack: undefined,
      stacks: [],
      stackNames: [],
      maskSelect_id: 'test_mask_sel',
      mask_displayed: undefined,
      gt_masks: [],
      pred_masks: []
    }
  },
  computed: {
    getMasknames () {
      return this.gt_masks.concat(this.pred_masks)
    },
    getStacknames () {
      if (this.$store.state.open_study) {
        const imageNames = this.$store.state.open_study.images.map(
          obj => {
            return obj.name
          }
        )
        return imageNames
      } else {
        return []
      }
    }
  },
  watch: {},
  created () {
    // this.stacks = this.$store.state.input.stackData
    // this.stackNames = this.$store.state.input.stackNames
    // this.gt_masks = this.$store.state.input.gtmaskNames
    // this.pred_masks = this.$store.state.output.predmaskNames
  },
  mounted () {
    this.initViewer()
    var elements = cornerstone.getEnabledElements()
    elements.forEach((ele) => cornerstone.resize(ele.element))
  },
  unmounted () {
    var elements = cornerstone.getEnabledElements()
    elements.forEach((ele) => cornerstone.resize(ele.element))
  },
  methods: {
    initViewer () {
      this.element = this.$refs.viewer
      cornerstone.enable(this.element, {
        renderer: 'webgl'
      })

      this.element.addEventListener(
        'contextmenu',
        function (e) {
          e.preventDefault()
        },
        false
      )
    },
    loadMaskOnSelect (event) {
      const segMaskName = event.target.value
      var segmentation = cornerstoneTools.getModule('segmentation')
      const element = this.element
      segmentation.setters.activeLabelmapIndex(this.element, 0)
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
    loadStackOnSelect (event) {
      const stackName = event.target.value
      const baseUrl = this.$store.state.open_study.images.find(image => image.name === stackName).base_url.replace('127.0.0.1', 'localhost:5000')
      if (stackName !== '') {
        const data = { name: stackName, size: 0, data: [stackName] }
        const stacks = this.parseImagesCornerstone(data.data, baseUrl)
        console.log(stacks)
        this.loadDisplayCornerstone(stacks[0], stacks[1], 'input').then(() => {
          this.setMetaData('input')
          this.filterMasks(stackName)
        })
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
        cornerstone.displayImage(this.element, image)
        cornerstoneTools.addStackStateManager(this.element, ['stack'])
        cornerstoneTools.addToolState(this.element, 'stack', stack)
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
  }
}
</script>

<style>
</style>
