<template>
  <!-- viewport info -->
  <div>
    <div class="row mx-auto mt-1">
      <button class="btn btn-secondary col-12" data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
        <h5 class="mt-1">{{heading}}</h5>
      </button>
    </div>

    <div :id="id" class="collapse">
      <!-- windowing -->
      <div class="mx-auto">
        <div class="input-group mx-auto">
          <label class="input-group-text w-20">WW/WC</label>
          <input id="ww_" type="Number" step="any" min="0" class="form-control ww viewport_prop" placeholder="WW"
            v-model="windowWidth" />
          <input id="wc_" type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC"
            v-model="windowCenter"/>
        </div>
      </div>

      <!-- window zoom -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-20">Zoom</label>
          <input id="zoom_" type="Number" step="0.1" min="0.1" class="form-control zoom viewport_prop"
            placeholder="Zoom" v-model="scale"/>
        </div>
      </div>

      <!-- window position -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-20">Pos</label>
          <input id="pos_x_" type="Number" step="any" class="form-control pos_x viewport_prop" placeholder="x" v-model="posX"/>
          <input id="pos_y_" type="Number" step="any" class="form-control pos_y viewport_prop" placeholder="y" v-model="posY"/>
        </div>
      </div>

      <!-- rotation -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-20">Rotation</label>
          <input id="pos_y_" type="Number" step="1" class="form-control pos_y viewport_prop" placeholder="rotation" v-model="rotation"/>
        </div>
      </div>

      <!--reset buttons -->
      <button class="btn btn-block btn-light w-100" @click="resetViewport">
        reset
      </button>
    </div>
  </div>
</template>

<script>
import cornerstone from 'cornerstone-core'

export default {
  props: {
    targetViewer: Number,
    test: Object
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
      return 'Viewer ' + this.targetViewer
    },
    windowWidth: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerWindowWidth'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerWindowWidth', {
          viewer: this.targetViewer,
          windowWidth: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.voi.windowWidth = value
        cornerstone.updateImage(element)
      }
    },
    windowCenter: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerWindowCenter'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerWindowCenter', {
          viewer: this.targetViewer,
          windowCenter: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.voi.windowCenter = value
        cornerstone.updateImage(element)
      }
    },
    scale: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerScale'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerScale', {
          viewer: this.targetViewer,
          scale: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.scale = value
        // not sure why update not working here
        cornerstone.setViewport(element, viewport)
      }
    },
    posX: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerPosX'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerPosX', {
          viewer: this.targetViewer,
          posX: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.translation.x = value
        cornerstone.updateImage(element)
      }
    },
    posY: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerPosY'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerPosY', {
          viewer: this.targetViewer,
          posY: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.translation.y = value
        cornerstone.updateImage(element)
      }
    },
    rotation: {
      get () {
        return this.$store.getters['imageViewers/cornerstoneViewerRotation'](this.targetViewer)
      },
      set (value) {
        this.$store.commit('imageViewers/cornerstoneViewerRotation', {
          viewer: this.targetViewer,
          rotation: value
        })
        const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
        var viewport = cornerstone.getViewport(element)
        viewport.rotation = value
        cornerstone.setViewport(element, viewport)
      }
    }
  },
  methods: {
    resetViewport () {
      const element = this.$store.getters['imageViewers/cornerstoneViewer'](this.targetViewer)
      const enabledElement = cornerstone.getEnabledElement(element)
      var defViewport = cornerstone.getDefaultViewportForImage(element, enabledElement.image)
      this.$store.commit('cornerstoneViewportUpdate', { viewport: defViewport, index: this.targetViewer })
      cornerstone.reset(element)
    }
  }
}
</script>

<style>
</style>
