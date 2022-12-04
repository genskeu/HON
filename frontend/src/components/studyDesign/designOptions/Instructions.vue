<template>
  <div id="instructions">
    <!-- General Settings -->
    <div>
      <div class="row">
        <div class="col-2 my-auto mx-auto">
          <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle" :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
          </button>
        </div>

        <div class="col-10">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#instructions_container" aria-expanded="true" aria-controls="instructions_container">
              Instructions
            </button>
          </h2>
        </div>
      </div>
      <div id="instructions_container" class="w-100 mx-0 px-0 collapse">
        <div class="mx-auto accordion-body px-0 py-0">
          <div class="input-group" id="instructions_input_field">
            <textarea rows="5" class="form-control" type="text" name="instructions" id="instructions"
              placeholder="Instructions" v-model="instructions"></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InstructionsDesign',
  data () {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'Instructions can be customized and are displayed to participants throughout the study.'
    }
  },
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
