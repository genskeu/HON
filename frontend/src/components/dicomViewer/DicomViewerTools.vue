<template>
    <!-- tool select menus -->
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Active Tools</label>
        <select class='form-select' v-model="toolActiveLeft">
            <option></option>
            <option v-for="tool in Object.keys(toolsButtons)" :key="tool" :value="tool">{{toolsButtons[tool]}}</option>
        </select>
        <select class='form-select' v-model="toolActiveWheel">
            <option></option>
            <option v-for="tool in Object.keys(toolsWheel)" :key="tool" :value="tool">{{toolsWheel[tool]}}</option>
        </select>        <select class='form-select' v-model="toolActiveRight">
            <option></option>
            <option v-for="tool in Object.keys(toolsButtons)" :key="tool" :value="tool">{{toolsButtons[tool]}}</option>
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
      toolsButtons: {
        Wwwc: 'Windowing',
        WwwcRegion: 'Windowing (region auto)',
        Pan: 'Move',
        Magnify: 'Magnify',
        Rotate: 'Rotate',
        Zoom: 'Zoom',
        StackScroll: 'Stack scroll',
        CircleRoi: 'Circle-roi',
        EllipticalRoi: 'Elliptical-roi',
        RectangleRoi: 'Rectangle-roi',
        FreehandRoi: 'Freehand-roi',
        Length: 'Length Measurment',
        Eraser: 'Remove ROI/Length',
        Brush: 'Brush-Segmentation',
        FreehandScissors: 'Freehand-Segmentation',
        CorrectionScissors: 'Freehand with correction',
        RectangleScissors: 'Rectangle-Segmentation'
      },
      toolsWheel: {
        ZoomMouseWheel: 'Zoom (mouse wheel)',
        StackScrollMouseWheel: 'Stack scroll (mouse wheel)'
      },
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
      Object.keys(this.toolsButtons).forEach(tool => {
        cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
      })
      Object.keys(this.toolsWheel).forEach(tool => {
        cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
      })
      this.$store.commit('imageViewers/toolsInitialized', true)
    }
  }
}
</script>

<style>
</style>
