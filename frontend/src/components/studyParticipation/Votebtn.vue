<template>
    <div class="row mx-auto">
        <h4 class="mx-auto" style="text-align:center;">
            <button  class="btn btn-success vote_button mx-auto" @click="saveResult">{{this.buttonLabel}}</button>
        </h4>
    </div>
</template>

<script>
export default {
  computed: {
    buttonLabel: {
      get () {
        return this.$store.getters['openStudy/buttonLabels']
      }
    }
  },
  methods: {
    saveResults () {
      // get viewer id
      // get displayed imagestacks incl viewport settings (ww, wc ...) and tool states from store
      // get scale data
      // sent data to backend via axios
      // load next image set
    }
  }
}
</script>

<style>

</style>
