<template>
    <div class="row mx-auto">
        <h4 class="mx-auto" style="text-align:center;">
            <button  class="btn btn-success vote_button mx-auto" id="vote_">{{this.buttonLabel}}</button>
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
  }
}
</script>

<style>

</style>
