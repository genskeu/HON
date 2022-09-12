<template>
    <div class="row mx-auto">
        <h4 class="mx-auto" style="text-align:center;">
            <button  class="btn btn-success vote_button mx-auto" @click="saveResult">{{this.buttonLabel}}</button>
        </h4>
    </div>
</template>

<script>
export default {
  props: {
    viewerIndex: Number
  },
  computed: {
    buttonLabel () {
      return this.$store.getters['openStudy/buttonLabels']
    },
    scalesInput () {
      return this.$store.getters['openStudy/scalesInput']
    },
    imgsetDisplayed () {
      return this.$store.getters['openStudy/imgsetDisplayed']
    },
    imgsetInput () {
      return this.$store.getters['imageViewers/getImgset']
    }
  },
  methods: {
    saveResult () {
      // get viewer id
      // get displayed imagestacks incl viewport settings (ww, wc ...) and tool states from store
      const imgset = this.imgsetInput
      // get scale data
      // sent data to backend via axios
      const payload = {
        imgset_id: this.imgsetDisplayed.id,
        picked_stack: imgset.stacks[this.viewerIndex],
        stacks_displayed: imgset.stacks,
        scale_input: this.scalesInput
      }
      this.$store.dispatch('openStudy/saveResult', payload)
    }
  }
}
</script>

<style>

</style>
