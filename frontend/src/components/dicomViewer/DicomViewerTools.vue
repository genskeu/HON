<template>
    <!-- tool select menus -->
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left" ref="toolMenu"
    title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
      <div class="row mx-auto">
        <DicomViewerToolsSelectMenu title="Active Tool Left Mouse Key" :viewerSettingTools="viewerSettingToolsMousekeys" :annotationTools="annotationToolsMousekeys" :segmentationTools="segmentationToolsMousekeys" :mouseKey="1"></DicomViewerToolsSelectMenu>
        <DicomViewerToolsSelectMenu title="Right Mouse Key" :viewerSettingTools="viewerSettingToolsMousekeys" :annotationTools="annotationToolsMousekeys" :segmentationTools="segmentationToolsMousekeys" :mouseKey="2"></DicomViewerToolsSelectMenu>
        <DicomViewerToolsSelectMenu title="Mouse Wheel" :viewerSettingTools="viewerSettingToolsMousewheel" :mouseKey="3"></DicomViewerToolsSelectMenu>
      </div>
    </div>
</template>

<script>
import Hammer from 'hammerjs'
import cornerstoneMath from 'cornerstone-math'
import cornerstone from 'cornerstone-core'
import cornerstoneTools from 'cornerstone-tools'
import DicomViewerToolsSelectMenu from '@/components/dicomViewer/DicomViewerToolsSelectMenu.vue'

cornerstoneTools.external.cornerstoneMath = cornerstoneMath
cornerstoneTools.external.cornerstone = cornerstone
cornerstoneTools.external.Hammer = Hammer

export default {
  name: 'cornerstoneTools',
  props: {
    toolsMousekeys: {},
    toolsMousewheel: {}
  },
  components: {
    DicomViewerToolsSelectMenu
  },
  data () {
    return {
      activeTool: undefined,
    }
  },
  computed: {
    annotationToolsMousekeys () {
      return this.toolsMousekeys.annotation
    },
    segmentationToolsMousekeys () {
      return this.toolsMousekeys.segmentation
    },
    viewerSettingToolsMousekeys () {
      return this.toolsMousekeys.viewerSetting
    },
    viewerSettingToolsMousewheel () {
      return this.toolsMousewheel.viewerSetting

    }
  },
  mounted () {
    cornerstoneTools.init({
      globalToolSyncEnabled: true
    })
    this.initCornerstoneTools()
  },
  activated () {
    this.initCornerstoneTools()
  },
  methods: {
    initCornerstoneTools () {
      const toolsAlreadyAdded = Object.keys(cornerstoneTools.store.state.globalTools)
      // merge tools from props
      const tools = {
        annotation: this.annotationToolsMousekeys,
        segmentation: this.segmentationToolsMousekeys,
        viewerSetting: {...this.viewerSettingToolsMousekeys, ...this.viewerSettingToolsMousewheel}
      }
      Object.keys(tools).forEach(toolType => {
        if (tools[toolType] === undefined) {
          return
        }
        Object.keys(tools[toolType]).forEach(tool => {
          if (!toolsAlreadyAdded.includes(tool)) {
            cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'])
          }
          // add labeled tools
          var toolSettings = tools[toolType][tool].settings
          if (toolSettings === undefined) {
            toolSettings = {}
          }
          if (Object.keys(toolSettings).includes('labels') ){
            toolSettings.labels.forEach(label => {
              const toolConfig = {
                name: tool + '-' + label
              }
              if (!toolsAlreadyAdded.includes(toolConfig.name)) {
                cornerstoneTools.addTool(cornerstoneTools[tool + 'Tool'], toolConfig)
              }
            })
          }
        })
      })
      // this.$store.commit('imageViewers/toolsInitialized', true)
      // prevent the context menu from appearing over the toolsMenu
      this.$refs.toolMenu.addEventListener('contextmenu', (event) => {
        event.preventDefault()
      })
    },
}
}
</script>