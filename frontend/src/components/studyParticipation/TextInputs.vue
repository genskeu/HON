<template>
  <div v-if="textFields.length">
    <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#text_inputs_container_user"
      aria-expanded="true" aria-controls="text_inputs_container_user">
      <h5 class="my-auto">Comments</h5>
    </button>
    <div id="text_inputs_container_user" class="collapse show">
      <TextInputParticipation v-for="(field, index) in textFields" :key="index" :field-index="index"></TextInputParticipation>
    </div>
  </div>
</template>

<script>
import TextInputParticipation from '@/components/studyParticipation/TextInput.vue'

export default {
  name: 'TextInputsParticipation',
  components: { TextInputParticipation },
  computed: {
    textFields () { return this.$store.getters['currentStudy/textFields'] }
  }
}
</script>