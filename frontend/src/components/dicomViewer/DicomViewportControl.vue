<template>
  <!-- viewport info -->
  <div>
    <div class="row mx-auto mt-1">
      <button class="btn btn-secondary col-12" data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
        <h5 class="mt-1">Viewer</h5>
      </button>
    </div>

    <div :id="id" class="collapse">
      <!-- windowing -->
      <div class="mx-auto">
        <div class="input-group mx-auto">
          <label class="input-group-text w-20">WW/WC</label>
          <input id="ww_" type="Number" step="any" min="0" class="form-control ww viewport_prop" placeholder="WW"
            v-model="windowWidth" />
          <input id="wc_" type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC" v-model="windowCenter"/>
        </div>
      </div>

      <!-- window zoom -->
      <div class="mx-auto">
        <div class="input-group">
          <label class="input-group-text w-20">Zoom</label>
          <input id="zoom_" type="Number" step="0.1" min="0.1" class="form-control zoom viewport_prop"
            placeholder="Zoom" v-model="zoom"/>
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
    targetViewer: Number
  },
  data () {
    return {
    }
  },
  // functions to control viewport settings, can properly be optimizied
  computed: {
    id () {
      return 'viewportControl_' + this.targetViewer
    },
    windowWidth: {
      get () {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        if (viewport !== undefined && viewport.voi !== undefined) {
          return viewport.voi.windowWidth
        } else {
          return NaN
        }
      },
      set (value) {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        var element = this.$store.getters.cornerstoneViewer(this.targetViewer)
        if (viewport !== undefined && viewport.voi !== undefined) {
          viewport.voi.windowWidth = value
          cornerstone.setViewport(element, viewport)
        }
      }
    },
    windowCenter: {
      get () {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        if (viewport !== undefined && viewport.voi !== undefined) {
          return viewport.voi.windowCenter
        } else {
          return NaN
        }
      },
      set (value) {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        var element = this.$store.getters.cornerstoneViewer(this.targetViewer)
        if (viewport !== undefined && viewport.voi !== undefined) {
          viewport.voi.windowCenter = value
          this.$store.commit('cornerstoneViewportUpdate', { viewport: viewport, index: this.targetViewer })
          cornerstone.setViewport(element, viewport)
        }
      }
    },
    zoom: {
      get () {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        if (viewport !== undefined) {
          return viewport.scale
        } else {
          return NaN
        }
      },
      set (value) {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        var element = this.$store.getters.cornerstoneViewer(this.targetViewer)
        if (viewport !== undefined) {
          viewport.scale = value
          this.$store.commit('cornerstoneViewportUpdate', { viewport: viewport, index: this.targetViewer })
          cornerstone.setViewport(element, viewport)
        }
      }
    },
    posX: {
      get () {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        if (viewport !== undefined && viewport.translation !== undefined) {
          return viewport.translation.x
        } else {
          return NaN
        }
      },
      set (value) {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        var element = this.$store.getters.cornerstoneViewer(this.targetViewer)
        if (viewport !== undefined && viewport.translation !== undefined) {
          viewport.translation.x = value
          this.$store.commit('cornerstoneViewportUpdate', { viewport: viewport, index: this.targetViewer })
          cornerstone.setViewport(element, viewport)
        }
      }
    },
    posY: {
      get () {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        if (viewport !== undefined && viewport.translation !== undefined) {
          return viewport.translation.y
        } else {
          return NaN
        }
      },
      set (value) {
        var viewport = this.$store.getters.cornerstoneViewport(this.targetViewer)
        var element = this.$store.getters.cornerstoneViewer(this.targetViewer)
        if (viewport !== undefined && viewport.translation !== undefined) {
          viewport.translation.y = value
          this.$store.commit('cornerstoneViewportUpdate', { viewport: viewport, index: this.targetViewer })
          cornerstone.setViewport(element, viewport)
        }
      }
    }
  },
  methods: {
    resetViewport () {
      const element = this.$store.getters.cornerstoneViewer(this.targetViewer)
      const enabledElement = cornerstone.getEnabledElement(element)
      var defViewport = cornerstone.getDefaultViewportForImage(element, enabledElement.image)
      this.$store.commit('cornerstoneViewportUpdate', { viewport: defViewport, index: this.targetViewer })
      cornerstone.setViewport(element, defViewport)
    }
  }
}
</script>

<style>
</style>
