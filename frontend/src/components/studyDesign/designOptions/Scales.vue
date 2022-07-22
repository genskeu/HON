<template>
  <div>
    <!-- scales -->
    <div class="row mx-auto mt-1"
      title="Scales can be customized and are displayed to participants throughout studies.">
      <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#scales_container"
        aria-expanded="true" aria-controls="scales_container">
        <h5 class="mt-1">Scale(s)</h5>
      </button>
    </div>
    <div id="scales_container" class="collapse">
      <div class="row mx-auto">
        <button class="btn btn-success btn-block col" id="add_scale">
          add scale
        </button>
      </div>

      <div id="scales" class="mt-1">
          <ScaleAdminView v-for="(scale, index) in scales" :key="index" :scale-index="index"></ScaleAdminView>
        <!-- templetate to create new scales using js -->
      </div>
    </div>
  </div>
</template>

<script>
import ScaleAdminView from '@/components/studyDesign/designOptions/Scale.vue'

export default {
  components: {
    ScaleAdminView
  },
  computed: {
    scales () {
      return this.$store.getters['openStudy/scales']
    }
  }
}
</script>

<style>

</style>
