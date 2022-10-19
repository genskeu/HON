<template>
  <div>
    <div class="row mx-auto mt-1"
      title="Instructions can be customized and are displayed to participants throughout studies.">
      <!-- instructions -->
      <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#instructions_container"
        aria-expanded="true" aria-controls="instructions_container">
        <h5 class="mt-1 col-12">Instructions</h5>
      </button>
      <div id="instructions_container" class="w-100 mx-0 px-0 collapse">
        <div class="input-group" id="instructions_input_field">
          <textarea rows="3" class="form-control" type="text" name="instructions" id="instructions"
            placeholder="Instructions" v-model="instructions"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    instructions: {
      get () {
        return this.$store.getters['currentStudy/instructions']
      },
      set (value) {
        this.$store.commit('currentStudy/instructions', value)
      }
    }
  }
}
</script>

<style>

</style>
