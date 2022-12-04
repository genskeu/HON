<template>
  <div id="scales">
    <!-- General Settings -->
    <div>
      <div class="row">
        <div class="col-2 my-auto mx-auto">
          <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
            :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
          </button>
        </div>

        <div class="col-10">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#scales_container" aria-expanded="true" aria-controls="scales_container">
              Scale(s)
            </button>
          </h2>
        </div>
      </div>
      <div id="scales_container" class="w-100 mx-0 px-0 collapse">
        <div class="mx-auto accordion-body px-0 py-0">
          <div id="scales" class="">
            <ScaleAdminView v-for="(scale, index) in scales" :key="index" :scale-index="index"></ScaleAdminView>
          </div>
          <div class="row mx-auto">
            <button class="btn btn-success btn-block col" id="add_scale" @click="addScale">
              &#43; add scale
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ScaleAdminView from '@/components/studyDesign/designOptions/Scale.vue'

export default {
  name: 'SaclesDesign',
  components: {
    ScaleAdminView
  },
  data () {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'This section allows for the creation and customization of rating scales displayed to participants. Design options include a scale text, the range of numerical values covered by the scale as well as labels for each value.'
    }
  },
  computed: {
    scales () {
      return this.$store.getters['currentStudy/scales']
    }
  },
  methods: {
    addScale () {
      var labels = []
      for (let i = 1; i <= 7; i++) {
        labels.push(i)
      }
      const defScale = {
        min: 1,
        max: 7,
        text: '',
        type: '',
        labels: labels
      }
      this.$store.commit('currentStudy/addScale', defScale)
    }
  }
}
</script>

<style>

</style>
