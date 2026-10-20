<template>
  <div class="mt-1">
    <div v-if="fieldName" class="row mx-auto justify-content-center">
      <div class="col scale_text" style="white-space: pre-wrap; text-align:center">{{fieldName}}</div>
    </div>
    <textarea v-model="textInputValue" rows="3" class="form-control mt-1"></textarea>
  </div>
</template>

<script>
export default {
  name: 'TextInputParticipation',
  props: { fieldIndex: Number },
  computed: {
    fieldName () { return this.$store.getters['studyInput/textInputs'][this.fieldIndex].name },
    textInputValue: {
      get () {
        const input = this.$store.getters['studyInput/textInput'](this.fieldIndex)
        return input && input.value !== null ? input.value : ''
      },
      set (value) { this.$store.commit('studyInput/updTextInput', { index: this.fieldIndex, value }) }
    }
  },
  created () {
    const field = this.$store.getters['currentStudy/textFields'][this.fieldIndex]
    this.$store.commit('studyInput/addTextInput', { index: this.fieldIndex, name: field ? field.text : '', value: null })
  }
}
</script>