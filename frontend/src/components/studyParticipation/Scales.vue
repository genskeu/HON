<template>
  <div>
    <!-- scales -->
    <div v-if="scales.length" class="row mx-auto">
      <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#scales_container"
        aria-expanded="true" aria-controls="scales_container">
        <h5 class="my-auto">Scales</h5>
      </button>
    </div>
    <div id="scales_container" class="collapse show">
      <div id="scales" class="mt-1 mb-1">
          <Scale v-for="(scale, index) in scales" :key="index" :scale-index="index"></Scale>
      </div>
    </div>
  </div>
</template>

<script>
import Scale from '@/components/studyParticipation/Scale.vue'

export default {
  name: 'ScalesParticipation',
  components: {
    Scale
  },
  computed: {
    scales () {
      return this.$store.getters['currentStudy/scales']
    },
    scalesInput () {
      return this.$store.getters['currentStudy/scalesInput']
    }
  },
  methods: {
    captureScaleInput(e) {
      const isNumber = /^[0-9]$/.test(e.key)
      if (e.key >= 0 && e.key <= 9 && isNumber) {
        // find the first scale that has not been answered
        var scale = this.scalesInput.find(scale => scale.value === null)
        if (scale) {
          scale.value = e.key
        }
      }
    }
  },
  created () {
    // listen for keydown events and capture scale input
    window.addEventListener('keydown', this.captureScaleInput)
  },
  unmounted () {
    window.removeEventListener('keydown', this.captureScaleInput)
  }
}
</script>

<style>

</style>
