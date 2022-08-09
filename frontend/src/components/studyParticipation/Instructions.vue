<template>
  <div>
    <div class="row mx-auto"
      title="Instructions can be customized and are displayed to participants throughout studies.">
      <!-- instructions -->
      <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#instructions_container"
        aria-expanded="true" aria-controls="instructions_container">
        <h5 class="mt-1 col-12">Instructions</h5>
      </button>
      <div id="instructions_container" class="w-100 collapse show">
        {{this.instructions}}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    instructions: {
      get () {
        return this.$store.getters['openStudy/instructions']
      }
    }
  }
}
</script>

<style>

</style>
