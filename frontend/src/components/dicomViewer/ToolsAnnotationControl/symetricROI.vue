<template>
  <div class="my-1">
     <div class="input-group-text " data-bs-toggle="collapse" data-bs-target= "#id"
        aria-expanded="true" aria-controls="id">
        <h5 class="mx-auto">{{heading}}</h5>
      </div>
      <div class="mx-auto">
        <div class="input-group mx-auto">
          <label class="input-group-text w-20">Start</label>
          <input type="Number" step="any" class="form-control" placeholder="X"
            v-model="startX" />
          <input type="Number" step="any" class="form-control" placeholder="Y"
            v-model="startY"/>
        </div>
      </div>

      <!-- end -->
      <div class="mx-auto">
        <div class="input-group mx-auto">
          <label class="input-group-text w-20">End</label>
          <input type="Number" step="any" class="form-control" placeholder="X"
            v-model="endX" />
          <input type="Number" step="any" class="form-control" placeholder="Y"
            v-model="endY"/>
        </div>
      </div>

      <!--reset buttons -->
      <button class="btn btn-block btn-danger w-100" @click="deleteAnnotation">
        delete
      </button>
  </div>
</template>

<script>
// import cornerstoneTools from 'cornerstone-tools'
import cornerstone from 'cornerstone-core'

export default {
  props: {
    targetViewer: Number,
    viewerType: String,
    uuid: String,
    toolName: String
  },
  data () {
    return {
    }
  },
  computed: {
    heading () {
      return this.uuid
    },
    // hacky solution to control roi position, could be improved
    // get positions reactive via vuex store (contains reference to cornerstone tool state)
    // set operates directly on reference to cornerstone tool state
    startX: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const startX = roi.measurementData.handles.start.x
        return startX.toFixed(2)
      },
      set (value) {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        roi.measurementData.handles.start.x = Number(value)
        roi.measurementData.invalidated = true
        cornerstone.updateImage(element)
      }
    },
    startY: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const startY = roi.measurementData.handles.start.y
        return startY.toFixed(2)
      },
      set (value) {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        roi.measurementData.handles.start.y = Number(value)
        roi.measurementData.invalidated = true
        cornerstone.updateImage(element)
      }
    },
    endX: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const endX = roi.measurementData.handles.end.x
        return endX.toFixed(2)
      },
      set (value) {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        roi.measurementData.handles.end.x = Number(value)
        roi.measurementData.invalidated = true
        cornerstone.updateImage(element)
      }
    },
    endY: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const endY = roi.measurementData.handles.end.y
        return endY.toFixed(2)
      },
      set (value) {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        roi.measurementData.handles.end.y = Number(value)
        roi.measurementData.invalidated = true
        cornerstone.updateImage(element)
      }
    }
  },
  methods: {
    deleteAnnotation () {
      const payload = {
        type: this.toolName,
        uuid: this.uuid,
        index: this.targetViewer,
        viewertype: this.viewerType
      }
      this.$store.commit('imageViewers/removeAnnotation', payload)
      // cornerstoneTools.removeToolState(this.toolName)
    }
  }
}
</script>

<style>

</style>
