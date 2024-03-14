<template>
  <!-- viewport info -->
  <div>
    <div class="row mx-auto">
      <button class="text-start btn-light btn col-10" data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
        <div class="mr-auto">{{heading}}</div>
      </button>
      <!--reset buttons -->
      <button class="btn btn-light col-2" @click="resetViewport"
      title="Reset Viewer to default values.">
        &#8634;
      </button>
    </div>

    <div :id="id" class="collapse show">
      <!-- windowing -->
      <div class="mx-auto">
        <div class="input-group mx-auto">
          <label class="input-group-text tw-w-20">WW/WC</label>
          <input type="Number" step="any" min="0" class="form-control ww viewport_prop" placeholder="WW"
            v-model="windowWidth" />
          <input type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC"
            v-model="windowCenter"/>
        </div>
      </div>

      <!-- window zoom -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text tw-w-20">Zoom</label>
          <input type="Number" step="0.1" min="0.1" class="form-control zoom viewport_prop"
            placeholder="Zoom" v-model="scale"/>
        </div>
      </div>

      <!-- window position -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text tw-w-20">Pos</label>
          <input type="Number" step="any" class="form-control pos_x viewport_prop" placeholder="x" v-model="posX"/>
          <input type="Number" step="any" class="form-control pos_y viewport_prop" placeholder="y" v-model="posY"/>
        </div>
      </div>

      <!-- rotation -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text tw-w-20">Rotation</label>
          <input type="Number" step="1" class="form-control pos_y viewport_prop" placeholder="rotation" v-model="rotation"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cornerstone from 'cornerstone-core'

export default {
  props: {
    targetViewer: Number,
    viewerType: String
  },
  data () {
    return {
    }
  },
  computed: {
    id () {
      return 'viewportControl_' + this.targetViewer
    },
    heading () {
      return 'Viewer ' + (this.targetViewer + 1)
    },
    windowWidth: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerWindowWidth'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.voi.windowWidth = Number(value)
        cornerstone.updateImage(element)
      }
    },
    windowCenter: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerWindowCenter'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.voi.windowCenter = Number(value)
        cornerstone.updateImage(element)
      }
    },
    scale: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerScale'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.scale = Number(value)
        // not sure why update not working here
        cornerstone.setViewport(element, viewport)
      }
    },
    posX: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerPosX'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.translation.x = Number(value)
        cornerstone.updateImage(element)
      }
    },
    posY: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerPosY'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.translation.y = Number(value)
        cornerstone.updateImage(element)
      }
    },
    rotation: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerRotation'](this.targetViewer, this.viewerType)
      },
      set (value) {
        // viewer settings in store are updated by function triggered on image rendered, see dicomviewer
        const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
        var viewport = cornerstone.getViewport(element)
        viewport.rotation = Number(value)
        cornerstone.setViewport(element, viewport)
      }
    }
  },
  methods: {
    resetViewport () {
      const element = this.$store.getters['imageViewers/element'](this.targetViewer, this.viewerType)
      const enabledElement = cornerstone.getEnabledElement(element)
      var defViewport = cornerstone.getDefaultViewportForImage(element, enabledElement.image)
      this.$store.commit('imageViewers/cornerstoneViewportUpdate', { viewport: defViewport, index: this.targetViewer, viewertype: this.viewerType })
      cornerstone.reset(element)
    }
  }
}
</script>

<style>
</style>
