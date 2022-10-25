<template>
    <!-- tool select menus -->
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Active Tool Left Mouse Key</label>
        <select class='form-select' v-model="toolActiveLeft">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(label, tool) in viewerSettingToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
            <option class="h5" disabled>Annotation</option>
            <option v-for="(label, tool) in annotationToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
            <option class="h5" disabled>Segmentation</option>
            <option v-for="(label, tool) in segmentationToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
        </select>
        <label class="input-group-text">Right Mouse Key</label>
        <select class='form-select' v-model="toolActiveRight">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(label, tool) in viewerSettingToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
            <option class="h5" disabled>Annotation</option>
            <option v-for="(label, tool) in annotationToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
            <option class="h5" disabled>Segmentation</option>
            <option v-for="(label, tool) in segmentationToolsMousekeys" :key="tool" :value="tool">{{label}}</option>
        </select>
        <label class="input-group-text">Mouse Wheel</label>
        <select class='form-select' v-model="toolActiveWheel">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(label, tool) in viewerSettingToolsMousewheel" :key="tool" :value="tool">{{label}}</option>
        </select>
    </div>
</template>

<script>
import Hammer from 'hammerjs'
import cornerstoneMath from 'cornerstone-math'
import cornerstone from 'cornerstone-core'
import cornerstoneTools from 'cornerstone-tools'

cornerstoneTools.external.cornerstoneMath = cornerstoneMath
cornerstoneTools.external.cornerstone = cornerstone
cornerstoneTools.external.Hammer = Hammer

export default {
  name: 'cornerstoneTools',
  data () {
    return {
      toolActiveLeft: undefined,
      toolActiveRight: undefined,
      toolActiveWheel: undefined
    }
  },
  mounted () {
    // var toolsInitialized = this.$store.getters['imageViewers/toolsInitialized']
    this.initCornerstoneTools()
  },
  computed: {
    activeToolLeft () {
      return this.toolActiveLeft
    },
    activeToolRight () {
      return this.toolActiveRight
    },
    activeToolWheel () {
      return this.toolActiveWheel
    },
    annotationToolsMousekeys () {
      return this.$store.getters['imageViewers/annotationToolsMousekeys']
    },
    segmentationToolsMousekeys () {
      return this.$store.getters['imageViewers/segmentationToolsMousekeys']
    },
    viewerSettingToolsMousekeys () {
      return this.$store.getters['imageViewers/viewerSettingToolsMousekeys']
    },
    viewerSettingToolsMousewheel () {
      return this.$store.getters['imageViewers/viewerSettingToolsMousewheel']
    }
  },
  watch: {
    activeToolLeft (newTool, oldTool) {
      if (oldTool !== undefined & oldTool !== this.activeToolRight) {
        cornerstoneTools.setToolEnabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 1 })
    },
    activeToolRight (newTool, oldTool) {
      if (oldTool !== undefined & oldTool !== this.activeToolLeft) {
        cornerstoneTools.setToolEnabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 2 })
    },
    activeToolWheel (newTool, oldTool) {
      if (oldTool !== undefined) {
        cornerstoneTools.setToolEnabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 3 })
    }
  },
  methods: {
    initCornerstoneTools () {
      cornerstoneTools.init({
        globalToolSyncEnabled: true
      })
      const toolsAlreadyAdded = Object.keys(cornerstoneTools.store.state.globalTools)
      Object.keys(this.viewerSettingToolsMousekeys).forEach(tool => {
        if (!toolsAlreadyAdded.includes(tool)) {
          cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
        }
      })
      Object.keys(this.annotationToolsMousekeys).forEach(tool => {
        if (!toolsAlreadyAdded.includes(tool)) {
          cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
        }
      })
      Object.keys(this.segmentationToolsMousekeys).forEach(tool => {
        if (!toolsAlreadyAdded.includes(tool)) {
          cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
        }
      })
      Object.keys(this.viewerSettingToolsMousewheel).forEach(tool => {
        if (!toolsAlreadyAdded.includes(tool)) {
          cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
        }
      })
      // this.$store.commit('imageViewers/toolsInitialized', true)
    }
  }
}
</script>

<style>
</style>
