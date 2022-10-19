<template>
    <div id="sclae_temp" class="mt-1 scale_template">
        <!-- <span class="badge badge-light w-100 mt-1">
            <h6 id="scale_heading_" class="mt-1 scale_heading">Scale {{this.scaleIndex + 1}}</h6>
        </span> -->
        <!-- participant view of scale -->
        <div class="mx-auto mb-3 scale_view_user" id="scale_view_user_">
            <div class="row mx-auto justify-content-center">
                <div id="scale_text_" class="col scale_text" style="white-space: pre-wrap; text-align: center">
                    {{this.scaleText}}
                </div>
            </div>
            <div class="mx-auto justify-content-center mt-1 scale_values">
                <div v-for="(value, index) in scaleValues" :key="value" class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" :value="value" :name=this.scaleIndex v-model="scaleInput">
                    <label class="form-check-label" for="inlineRadio1">{{scaleLabels[index]}}</label>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    scaleIndex: Number
  },
  computed: {
    scaleText () {
      return this.$store.getters['currentStudy/scaleText'](this.scaleIndex)
    },
    scaleMin () {
      return this.$store.getters['currentStudy/scaleMin'](this.scaleIndex)
    },
    scaleMax () {
      return this.$store.getters['currentStudy/scaleMax'](this.scaleIndex)
    },
    scaleType () {
      return this.$store.getters['currentStudy/scaleMax'](this.scaleIndex)
    },
    scaleValues () {
      var values = []
      for (let i = this.scaleMin; i <= this.scaleMax; i++) {
        values.push(i)
      }
      return values
    },
    scaleLabels () {
      return this.$store.getters['currentStudy/scaleLabels'](this.scaleIndex)
    },
    scaleInput: {
      get () {
        return this.$store.getters['currentStudy/scaleInput'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('currentStudy/scaleInput', { index: this.scaleIndex, input: value })
      }
    }
  }
}
</script>

<style>

</style>
