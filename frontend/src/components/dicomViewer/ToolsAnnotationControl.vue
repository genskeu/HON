<template>
  <!-- viewport info -->
  <div>
    <div class="row mx-auto">
      <button class="input-group-text " data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
        <h5 class="mx-auto">{{heading}}</h5>
      </button>
    </div>
    <div :id="id" class="collapse show" v-if="EllipticalRois">
      <div class="row mx-auto">
        <button class="input-group-text " data-bs-toggle="collapse" data-bs-target= "#EllipticalRois"
          aria-expanded="true" aria-controls="EllipticalRois">
          <h5 class="mx-auto">EllipticalRois</h5>
        </button>
      </div>
      <div id="EllipticalRois" class="collapse show">
        <symetric-ROI v-for="uuid in Object.keys(EllipticalRois)" :key="uuid" :uuid="uuid" :target-viewer="this.targetViewer" viewer-type="viewers" :tool-name="'EllipticalRoi'" :measurement-data="EllipticalRois[uuid].measurementData"></symetric-ROI>
      </div>

      <div class="row mx-auto" v-if="RectangleRois">
        <button class="input-group-text " data-bs-toggle="collapse" data-bs-target= "#RectangleRois"
          aria-expanded="true" aria-controls="RectangleRois">
          <h5 class="mx-auto">RectangleRois</h5>
        </button>
      </div>
      <div id="RectangleRois" class="collapse show">
        <symetric-ROI v-for="uuid in Object.keys(RectangleRois)" :key="uuid" :uuid="uuid" :target-viewer="this.targetViewer" viewer-type="viewers" :tool-name="'RectangleRoi'"></symetric-ROI>
      </div>

      <div class="row mx-auto" v-if="CircleRois">
        <button class="input-group-text " data-bs-toggle="collapse" data-bs-target= "#CircleRois"
          aria-expanded="true" aria-controls="CircleRois">
          <h5 class="mx-auto">CircleRois</h5>
        </button>
      </div>
      <div id="CircleRois" class="collapse show">
        <symetric-ROI v-for="uuid in Object.keys(CircleRois)" :key="uuid" :uuid="uuid" :target-viewer="this.targetViewer" viewer-type="viewers" :tool-name="'CircleRoi'"></symetric-ROI>
      </div>
    </div>
  </div>
</template>

<script>
import symetricROI from '@/components/dicomViewer/ToolsAnnotationControl/symetricROI.vue'

export default {
  props: {
    targetViewer: Number,
    viewerType: String
  },
  components: {
    symetricROI
  },
  data () {
    return {
    }
  },
  computed: {
    id () {
      return 'annotationControl_' + this.targetViewer
    },
    heading () {
      return 'Viewer ' + (this.targetViewer + 1)
    },
    EllipticalRois () {
      return this.$store.getters['imageViewers/EllipticalRois'](this.targetViewer, this.viewerType)
    },
    RectangleRois () {
      return this.$store.getters['imageViewers/RectangleRois'](this.targetViewer, this.viewerType)
    },
    CircleRois () {
      return this.$store.getters['imageViewers/CircleRois'](this.targetViewer, this.viewerType)
    }
  }
}
</script>

<style>

</style>
