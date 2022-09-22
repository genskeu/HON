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
    toolName: String,
    measurementData: Object
  },
  data () {
    return {
      handles: this.measurementData.handles,
      data: this.measurementData,
      cachedStats: this.measurementData.cachedStats
    }
  },
  computed: {
    heading () {
      return this.uuid
    },
    startX: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const startX = roi.measurementData.handles.start.x
        return startX.toFixed(2)
      },
      // test
      set (value) {
        this.handles.start.x = Number(value)
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        this.data.invalidated = true
        cornerstone.updateImage(element)
      }
    },
    startY: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const startY = roi.measurementData.handles.start.y
        return startY.toFixed(2)
      }
    },
    endX: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const endX = roi.measurementData.handles.end.x
        return endX.toFixed(2)
      }
    },
    endY: {
      get () {
        const roi = this.$store.getters['imageViewers/Roi'](this.targetViewer, this.viewerType, this.uuid, this.toolName)
        const endY = roi.measurementData.handles.end.y
        return endY.toFixed(2)
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
