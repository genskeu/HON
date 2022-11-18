<template>
    <div class="scale_template p-1">
        <h5 class="input-group-text scale_heading">Scale {{this.scaleIndex + 1}}</h5>
        <!-- admin view to define scale -->
        <div class="mx-auto scale_view_admin">
                <div class="input-group mx-auto">
                    <label class="input-group-text w-25">Text</label>
                    <textarea class="form-control scale_text_input" v-model="scaleText" rows="3"></textarea>
                </div>
                <div class="input-group mx-auto">
                    <label class="input-group-text w-25">Start</label>
                    <input class="form-control" min="-100" max="100" type="number" id="scale_min_input_"
                        placeholder="min" v-model="scaleMin"/>
                    <label class="input-group-text w-25">End</label>
                    <input class="form-control" min="-100" max="100" type="number" id="scale_max_input_"
                        placeholder="max"  v-model="scaleMax" />
                </div>
                <div class="input-group mx-auto">
                  <button class="input-group-text accordion-button accordion-button-lables collapsed" type="button" data-bs-toggle="collapse" :data-bs-target= "'#labels_scale_' + this.scaleIndex" aria-expanded="true" :aria-controls="'#labels_scale_' + this.scaleIndex">
                    Labels
                  </button>
                </div>
                <div :id="'labels_scale_' + this.scaleIndex" class="collapse">
                  <div v-for="(value, index) in scaleValues" :key="value" class="input-group mx-auto">
                    <label class="input-group-text w-25">{{value}}</label>
                    <input class="form-control" type="text" :value="scaleLabels[index]" @change="updateScaleLabel(index)"/>
                  </div>
                </div>
<!--                 <div class="input-group" title="Can be left blank for most studies except for FROC designs,
                    where a scale needs to be repeated each time a new roi is drawn.">
                    <label class="input-group-text w-25">Type</label>
                    <select id="scale_type_input_" class="form-control scale_type_input">
                        <option value=""></option>
                        <option value=""></option>
                    </select>
                </div> -->
            <button class="btn btn-danger btn-block scale_rm w-100" @click="deleteScale">
              &#8722; delete scale
            </button>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    scaleIndex: Number
  },
  data () {
    return {
    }
  },
  computed: {
    scaleText: {
      get () {
        return this.$store.getters['currentStudy/scaleText'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('currentStudy/scaleText', { index: this.scaleIndex, text: value })
      }
    },
    scaleMin: {
      get () {
        return this.$store.getters['currentStudy/scaleMin'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('currentStudy/scaleMin', { index: this.scaleIndex, min: value })
      }
    },
    scaleMax: {
      get () {
        return this.$store.getters['currentStudy/scaleMax'](this.scaleIndex)
      },
      set (value) {
        this.$store.commit('currentStudy/scaleMax', { index: this.scaleIndex, max: value })
      }
    },
    scaleType: {
      get () {
        return this.$store.getters['currentStudy/scaleMax'](this.scaleIndex)
      },
      set () {
      }
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
    }
  },
  methods: {
    deleteScale () {
      this.$store.commit('currentStudy/delScale', { index: this.scaleIndex })
    },
    updateScaleLabel (i) {
      this.$store.commit('currentStudy/scaleLabel', { index: this.scaleIndex, labelIndex: i, label: event.target.value })
    }
  }
}
</script>

<style>
.accordion-button-lables {
  font-size: 1rem;
  color: black;
  background-color: #e9ecef;
  padding-left: 0.75rem;
  padding-top: 0.3rem ;
  padding-bottom: 0.3rem ;
}

.accordion-button-lables:after {
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='black'><path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/></svg>");
}
</style>
