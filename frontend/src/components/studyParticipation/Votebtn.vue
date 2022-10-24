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
      return this.$store.getters['currentStudy/buttonLabels']
    },
    scalesInputDB () {
      return this.$store.getters['currentStudy/scalesInputDB']
    },
    imgsetDisplayed () {
      return this.$store.getters['currentStudy/imgsetDisplayed']
    },
    imgsetInput () {
      return this.$store.getters['imageViewers/getImgset']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    }
  },
  methods: {
    saveResult () {
      // get viewer id
      // get displayed imagestacks incl viewport settings (ww, wc ...) and tool states from store
      const imgset = this.imgsetInput
      // get scale data
      // sent data to backend via axios
      const stackIndex = this.refimageViewers.length + this.viewerIndex
      const stackPicked = imgset.stacks[stackIndex]
      const payload = {
        imgset_id: this.imgsetDisplayed.id,
        picked_stack: stackPicked,
        stacks_displayed: imgset.stacks,
        scale_input: this.scalesInputDB
      }
      this.$store.dispatch('currentStudy/saveResult', payload)
    }
  }
}
</script>

<style>

</style>
