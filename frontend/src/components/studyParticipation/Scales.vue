<template>
  <div>
    <!-- scales -->
    <div v-if="scales.length" class="row mx-auto mt-1"
      title="Scales can be customized and are displayed to participants throughout studies.">
      <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#scales_container"
        aria-expanded="true" aria-controls="scales_container">
        <h5 class="mt-1">Scales</h5>
      </button>
    </div>
    <div id="scales_container" class="collapse show">
      <div id="scales" class="mt-1">
          <Scale v-for="(scale, index) in scales" :key="index" :scale-index="index"></Scale>
      </div>
    </div>
  </div>
</template>

<script>
import Scale from '@/components/studyParticipation/Scale.vue'

export default {
  components: {
    Scale
  },
  computed: {
    scales () {
      return this.$store.getters['openStudy/scales']
    }
  },
  methods: {
  }
}
</script>

<style>

</style>
