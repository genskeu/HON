<template>
    <div id="sclae_temp" class="mt-1 scale_template">
        <span class="badge badge-light w-100 mt-1">
            <h6 id="scale_heading_" class="mt-1 scale_heading">Scale</h6>
        </span>
        <!-- admin view to define scale -->
        <div class="mx-auto scale_view_admin" id="scale_view_admin_">
                <div class="input-group mx-auto">
                    <label class="input-group-text w-25">Text</label>
                    <textarea class="form-control scale_text_input" v-model="scaleText" rows="3"></textarea>
                </div>
                <div class="input-group mx-auto">
                    <label class="input-group-text w-25">Start</label>
                    <input class="form-control scale_min_input" min="-100" max="100" type="number" id="scale_min_input_"
                        placeholder="min" v-model="scaleMin"/>
                </div>
                <div class="input-group">
                    <label class="input-group-text w-25">End</label>
                    <input class="form-control scale_max_input" min="-100" max="100" type="number" id="scale_max_input_"
                        placeholder="max"  v-model="scaleMax" />
                </div>
                <div class="input-group" title="Can be left blank for most studies except for FROC designs,
                    where a scale needs to be repeated each time a new roi is drawn.">
                    <label class="input-group-text w-25">Type</label>
                    <select id="scale_type_input_" class="form-control scale_type_input">
                        <option value=""></option>
                        <option value=""></option>
                    </select>
                </div>
            <button class="btn btn-danger btn-block scale_rm w-100" id="scale_rm_">
                delete scale
            </button>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    scaleIndex: Number
  },
  computed: {
    scaleText: {
      get () {
        return this.$store.getters['openStudy/scaleText'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('openStudy/scaleText', { index: this.scaleIndex, text: value })
      }
    },
    scaleMin: {
      get () {
        return this.$store.getters['openStudy/scaleMin'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('openStudy/scaleMin', { index: this.scaleIndex, min: value })
      }
    },
    scaleMax: {
      get () {
        return this.$store.getters['openStudy/scaleMax'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('openStudy/scaleMax', { index: this.scaleIndex, max: value })
      }
    },
    scaleType: {
      get () {
        return this.$store.getters['openStudy/scaleMax'](this.scaleIndex)
      },
      set () {
      }
    }
  }
}
</script>

<style>

</style>
