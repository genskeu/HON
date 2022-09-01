<template>
    <!-- progressbar -->
    <div class="mx-auto fixed-bottom">
        <div class="progress w-100">
            <div id="progressbar" class="progress-bar" role="progressbar" aria-valuenow="70" aria-valuemin="0"
                aria-valuemax="100" :style="progress">
                {{`${this.imgsetsFinished}/${this.imgsetsTotal}`}} items finished
            </div>
        </div>
    </div>
</template>

<script>
export default {
  computed: {
    imgsetsFinished () {
      return 10
    },
    imgsetsTotal () {
      return 100
    },
    progress () {
      var percFinished = this.imgsetsFinished / this.imgsetsTotal * 100
      return {
        width: percFinished + '%',
        color: 'black'
      }
    }
  }
}
</script>

<style>

</style>
