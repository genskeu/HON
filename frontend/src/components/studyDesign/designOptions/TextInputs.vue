<template>
  <div id="text_inputs">
    <div class="row">
      <div class="col-2 my-auto mx-auto">
        <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
          :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
        </button>
      </div>
      <div class="col-10">
        <h2 class="accordion-header">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#text_inputs_container" aria-expanded="false" aria-controls="text_inputs_container">
            Text Input(s)
          </button>
        </h2>
      </div>
    </div>
    <div id="text_inputs_container" class="w-100 mx-0 px-0 collapse">
      <div class="mx-auto accordion-body px-0 py-0">
        <TextInputAdmin v-for="(field, index) in textFields" :key="index" :field-index="index"></TextInputAdmin>
        <div class="row mx-auto">
          <button class="btn btn-success btn-block col" @click="addField">&#43; add text input</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TextInputAdmin from '@/components/studyDesign/designOptions/TextInput.vue'

export default {
  name: 'TextInputsDesign',
  components: { TextInputAdmin },
  data () {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'Define free-text fields (e.g. comments, short sentences) that participants fill in after each image set. The instruction text is displayed above the input field during the study.'
    }
  },
  computed: {
    textFields () { return this.$store.getters['currentStudy/textFields'] }
  },
  methods: {
    addField () {
      this.$store.commit('currentStudy/addTextField', { text: '' })
    }
  }
}
</script>