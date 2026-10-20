<template>
  <div class="p-0">
    <h5 class="input-group-text bg-gray-300 mb-0">Text Input {{this.fieldIndex + 1}}</h5>
    <div class="mx-auto scale_view_admin">
      <div class="input-group mx-auto">
        <label class="input-group-text w-25">Instr.</label>
        <textarea class="form-control" v-model="fieldText" rows="3"></textarea>
      </div>
      <button class="btn btn-danger btn-block scale_rm w-100" @click="deleteField">&#8722; delete text input</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextInputDesign',
  props: { fieldIndex: Number },
  computed: {
    fieldText: {
      get () { return this.$store.getters['currentStudy/textFields'][this.fieldIndex].text },
      set (value) { this.$store.commit('currentStudy/setTextFieldText', { index: this.fieldIndex, text: value }) }
    },
  },
  methods: {
    deleteField () { this.$store.commit('currentStudy/delTextField', this.fieldIndex) }
  }
}
</script>