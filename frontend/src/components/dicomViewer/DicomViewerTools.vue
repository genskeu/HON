<template>
    <!-- tool select menus -->
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Tool Active</label>
        <label class="input-group-text">Left Mouse Key</label>
        <select class='form-select' v-model="toolActiveLeft">
            <option></option>
            <option v-for="tool in Object.keys(toolsMousekeys)" :key="tool" :value="tool">{{toolsMousekeys[tool]}}</option>
        </select>
        <label class="input-group-text">Right Mouse Key</label>
        <select class='form-select' v-model="toolActiveRight">
            <option></option>
            <option v-for="tool in Object.keys(toolsMousekeys)" :key="tool" :value="tool">{{toolsMousekeys[tool]}}</option>
        </select>
        <label class="input-group-text">Mouse Wheel</label>
        <select class='form-select' v-model="toolActiveWheel">
            <option></option>
            <option v-for="tool in Object.keys(toolsMousewheel)" :key="tool" :value="tool">{{toolsMousewheel[tool]}}</option>
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
    var toolsInitialized = this.$store.getters['imageViewers/toolsInitialized']
    if (!toolsInitialized) {
      this.initCornerstoneTools()
    }
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
    toolsMousekeys () {
      return this.$store.getters['imageViewers/toolsMousekeys']
    },
    toolsMousewheel () {
      return this.$store.getters['imageViewers/toolsMousewheel']
    }
  },
  watch: {
    activeToolLeft (newTool, oldTool) {
      if (oldTool !== undefined) {
        cornerstoneTools.setToolDisabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 1 })
    },
    activeToolRight (newTool, oldTool) {
      if (oldTool !== undefined) {
        cornerstoneTools.setToolDisabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 2 })
    },
    activeToolWheel (newTool, oldTool) {
      if (oldTool !== undefined) {
        cornerstoneTools.setToolDisabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 3 })
    }
  },
  methods: {
    initCornerstoneTools () {
      cornerstoneTools.init({
        globalToolSyncEnabled: true
      })
      Object.keys(this.toolsMousekeys).forEach(tool => {
        cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
      })
      Object.keys(this.toolsMousewheel).forEach(tool => {
        cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
      })
      this.$store.commit('imageViewers/toolsInitialized', true)
    }
  }
}
</script>

<style>
</style>
