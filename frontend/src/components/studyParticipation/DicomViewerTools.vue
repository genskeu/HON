<template>
    <!-- tool select menus -->
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Active Tool Left Mouse Key</label>
        <select class='form-select' v-model="toolActiveLeft">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(tool, label) in viewerSettingToolsMousekeys" :key="tool" :value="tool.cs_name">{{label}}</option>
            <option class="h5" disabled>Annotation</option>
            <template v-for="(tool, label) in annotationToolsMousekeys" :key="tool">
              <option v-if="!tool.settings.labels" :value="tool.cs_name">{{label}}</option>
              <option v-else v-for="l in tool.settings.labels" :key="l" :value="l + tool.cs_name">{{l + ' (' + label + ')'}}</option>
            </template>
            <option class="h5" disabled>Segmentation</option>
            <option v-for="(tool, label) in segmentationToolsMousekeys" :key="tool" :value="tool.cs_name">{{label}}</option>
        </select>
        <label class="input-group-text">Right Mouse Key</label>
        <select class='form-select' v-model="toolActiveRight">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(tool, label) in viewerSettingToolsMousekeys" :key="tool" :value="tool.cs_name">{{label}}</option>
            <option class="h5" disabled>Annotation</option>
            <template v-for="(tool, label) in annotationToolsMousekeys" :key="tool">
              <option v-if="!tool.settings.labels" :value="tool.cs_name">{{label}}</option>
              <option v-else v-for="l in tool.settings.labels" :key="l" :value="l + tool.cs_name">{{l + ' (' + label + ')'}}</option>
            </template>
            <option class="h5" disabled>Segmentation</option>
            <option v-for="(tool, label) in segmentationToolsMousekeys" :key="tool" :value="tool.cs_name">{{label}}</option>
        </select>
        <label class="input-group-text">Mouse Wheel</label>
        <select class='form-select' v-model="toolActiveWheel">
            <option></option>
            <option class="h5" disabled>ViewerSettings</option>
            <option v-for="(tool, label) in viewerSettingToolsMousewheel" :key="tool" :value="tool.cs_name">{{label}}</option>
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
  props: {
    toolsMousekeysp: {},
    toolsMousewheelp: {}
  },
  data () {
    return {
      toolActiveLeft: undefined,
      toolActiveRight: undefined,
      toolActiveWheel: undefined
    }
  },
  mounted () {
    // var toolsInitialized = this.$store.getters['imageViewers/toolsInitialized']
    // console.log(cornerstoneTools.store.state)
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
      return this.$store.getters['currentStudy/annToolsMousekeysParticipant']
    },
    segmentationToolsMousekeys () {
      return this.$store.getters['currentStudy/segToolsMousekeysParticipant']
    },
    viewerSettingToolsMousekeys () {
      return this.$store.getters['currentStudy/viewerToolsMousekeysParticipant']
    },
    viewerSettingToolsMousewheel () {
      return this.$store.getters['currentStudy/viewerToolsMousewheelParticipant']
    },
    toolsParticipant () {
      return this.$store.getters['currentStudy/tools']
    }
  },
  watch: {
    activeToolLeft (newTool, oldTool) {
      if (oldTool !== undefined) {
        cornerstoneTools.setToolEnabled(oldTool)
      }
      cornerstoneTools.setToolActive(newTool, { mouseButtonMask: 1 })
    },
    activeToolRight (newTool, oldTool) {
      if (oldTool !== undefined) {
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
      this.toolsParticipant.forEach(tool => {
        const toolCornerStone = cornerstoneTools[tool.cs_name + 'Tool']
        if (tool.settings.labels) {
          tool.settings.labels.forEach(label => {
            const toolConfig = {
              name: label + tool.cs_name,
              type: tool.cs_name
            }
            cornerstoneTools.addTool(toolCornerStone, toolConfig)
          })
        } else {
          cornerstoneTools.addTool(toolCornerStone)
        }
      })
      this.$store.commit('imageViewers/toolsInitialized', true)
    }
  }
}
</script>

<style>
</style>
