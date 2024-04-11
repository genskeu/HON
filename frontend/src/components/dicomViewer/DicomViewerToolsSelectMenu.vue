<template class="col">
    <label class="col input-group-text" v-html="title" v-if="numberOfTools"></label>
    <select class='col form-select' @change="(event) => activateTool(event)" v-if="numberOfTools">
        <option></option>
        <option v-if="viewerSettingTools" class="btn btn-secondary col" disabled>Image Settings</option>
        <option class="col" v-for="(toolprops, toolcsname) in viewerSettingTools" :key="toolcsname" :value="toolcsname" v-html="toolprops.name" @change="(event) => activateTool(event, toolcsname)" :title="toolprops.name" ></option>
        
        <template v-if="annotationTools">
            <template v-for="(toolprops, toolcsname) in annotationTools" :key="toolcsname">
                <option v-if="!toolprops.settings" :value="toolcsname" v-html="toolprops.name"></option>
                <option v-else-if="!toolprops.settings.labels" :value="toolcsname" v-html="toolprops.name"></option>
                <option v-else v-for="l in toolprops.settings.labels" :key="l" :value="toolcsname + '-' + l">{{l + ' (' + toolprops.name + ')'}}</option>
            </template>
        </template>
        
        <option v-if="segmentationTools" class="btn btn-secondary col" disabled>Segmentation</option>
        <option class="col" v-for="(toolprops, toolcsname) in segmentationTools" :key="toolcsname" :value="toolcsname" v-html="toolprops.name" @change="(event) => activateTool(event, toolcsname)" :title="toolprops.name" ></option>
    </select>
</template>

<script>
import cornerstoneTools from 'cornerstone-tools'

export default {
    data() {
        return {
            activeTool: undefined
        }
    },
    props: {
        title: String,
        viewerSettingTools: Object,
        annotationTools: Object,
        segmentationTools: Object,
        mouseKey: Number
    },
    computed: {
        numberOfViewerSettingTools() {
            if (this.viewerSettingTools) {
                return Object.keys(this.viewerSettingTools).length
            } else {
                return 0
            }
        },
        numberOfAnnotationTools() {
            if (this.annotationTools) {
                return Object.keys(this.annotationTools).length
            } else {
                return 0
            }
        },
        numberOfSegmentationTools() {
            if (this.segmentationTools) {
                return Object.keys(this.segmentationTools).length
            } else {
                return 0
            }
        },
        numberOfTools() {
            return this.numberOfViewerSettingTools + this.numberOfAnnotationTools + this.numberOfSegmentationTools
        }
    },
    methods: {
        activateTool(event) {
            const tool = event.target.value
            event.preventDefault()
            var mouseButton = this.mouseKey
            if (this.activeTool === tool) {
                return
            } else if (this.activeTool) {
                cornerstoneTools.setToolPassive(this.activeTool, { mouseButtonMask: mouseButton })
            } 
            cornerstoneTools.setToolActive(tool, { mouseButtonMask: mouseButton })
            this.activeTool = tool
        }
    }
}
</script>