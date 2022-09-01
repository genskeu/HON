<template>
  <div class="my-1">
     <div class="input-group-text " data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
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
export default {
  props: {
    targetViewer: Number,
    uuid: String,
    toolName: String
  },
  computed: {
    heading () {
      return this.uuid
    },
    startX: {
      get () {
        const roi = this.$store.getters['imageViewers/EllipticalRoi'](this.targetViewer, this.uuid)
        const startX = roi.measurementData.handles.start.x
        return startX.toFixed(2)
      }
    },
    startY: {
      get () {
        const roi = this.$store.getters['imageViewers/EllipticalRoi'](this.targetViewer, this.uuid)
        const startY = roi.measurementData.handles.start.y
        return startY.toFixed(2)
      }
    },
    endX: {
      get () {
        const roi = this.$store.getters['imageViewers/EllipticalRoi'](this.targetViewer, this.uuid)
        const endX = roi.measurementData.handles.end.x
        return endX.toFixed(2)
      }
    },
    endY: {
      get () {
        const roi = this.$store.getters['imageViewers/EllipticalRoi'](this.targetViewer, this.uuid)
        const endY = roi.measurementData.handles.end.y
        return endY.toFixed(2)
      }
    }
  },
  methods: {
    deleteAnnotation () {
      this.$store.commit('imageViewers/removeAnnotation', { type: 'EllipticalRoi', uuid: this.uuid, index: this.targetViewer })
    }
  }
}
</script>

<style>

</style>
