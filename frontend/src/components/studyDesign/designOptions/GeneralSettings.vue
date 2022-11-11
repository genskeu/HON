<template>
  <div id="general_settings" class="accordion">
    <!-- General Settings -->
    <div class="accordion-item">
      <!-- <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#general_settings_content"
          aria-expanded="true" aria-controls="general_settings_content"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">General Settings</h5>
        </button>
      </div> -->
      <h3 class="accordion-header" id="general_settings_title">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#general_settings_content" aria-expanded="true" aria-controls="general_settings_content">
          General Settings
        </button>
      </h3>

      <div id="general_settings_content" class="accordion-collapse collapse" aria-labelledby="general_settings_title">
        <div class="mx-auto accordion-body px-0 py-0">
          <div class="input-group mx-auto" title="Controls max number of reference images">
            <label for="numb_refimg" class="input-group-text col-7"># RefImg Viewer</label>
            <input class="form-control" type="Number" min="0" max="5" id="numb_refimg" v-model="refviewerNumb"/>
          </div>

          <div class="input-group mx-auto" title="Controls max number of images">
            <label for="numb_img" class="input-group-text col-7"> # Img Viewer</label>
            <input class="form-control" type="Number" min="1" max="50" id="numb_img" v-model="viewerNumb"/>
          </div>

          <div class="input-group mx-auto my-auto" title="Controls max number of images">
            <label for="numb_img" class="input-group-text col-7">Viewers per Row</label>
            <input type="number" min="1" max="5" class="form-control" id="numb_img_cols" v-model="viewerLayoutCols"/>
          </div>

          <!-- window size -->
          <div class="input-group mx-auto"
            title="Controls the size (width, height) of the screen section used for displaying images.">
            <label class="input-group-text col-7">Set Viewer Size</label>
            <div class="form-switch form-control mb-0">
              <input class="form-check-input mr-2" type="checkbox" id="viewerHeightAuto" v-model="viewerHeightAuto">
              <label class="form-check-label" for="viewerHeightAuto">{{viewerHeightAutoText}}</label>
            </div>
          </div>

          <div v-if="!viewerHeightAuto" class="input-group mx-auto"
            title="Controls the size (width, height) of the screen section used for displaying images.">
            <label class="input-group-text col-7">Size in px</label>
            <input id="img_height" type="Number" step="any" min="1" class="image_size form-control" placeholder="height" v-model="viewerHeight"/>
          </div>

          <div class="input-group row mx-auto"
            title="Controls if image settings such as windowing or zoom level are displayed.">
            <label class="input-group-text col-7">Viewer Metadata</label>
            <div class="form-switch form-control mb-0">
              <input class="form-check-input mr-2" type="checkbox" id="viewerHeightAuto" v-model="viewerMetainfo">
              <label class="form-check-label" for="viewerHeightAuto">{{viewerMetainfoText}}</label>
            </div>
          </div>

          <div class="input-group mx-auto">
            <label class="input-group-text col-7">Text Color</label>
            <input class="form-control" type="text" id="text_color" placeholder="Text-Color (Hex or Name)" v-model="textColor" />
          </div>

          <div class="input-group mx-auto">
            <label class="input-group-text col-7">BG Color</label>
            <input class="form-control" type="text" id="background_color" placeholder="Background-Color (Hex or Name)"
              v-model="backgroundColor" />
          </div>

          <div class="input-group mx-auto" title="Time (sec) the screen will be blank between two image-sets.">
            <label class="input-group-text col-7">Transition Time</label>
            <input class="form-control" type="number" min="0" name="instructions" id="transition_time" placeholder="sec"
              v-model="transitionTime" />
          </div>

          <div class="row input-group mx-auto"
            title="Controls the text of the buttons displayed beneath each image to continue to the next image-set.">
            <label class="input-group-text col-7">Button Label</label>
            <input class="form-control" type="text" name="buttonLabels" id="button_labels" placeholder="Btn Label" v-model="buttonLabels" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    refviewerNumb: {
      get () {
        return this.$store.getters['currentStudy/refviewerNumb']
      },
      set (value) {
        this.$store.commit('currentStudy/refviewerNumber', value)
      }
    },
    viewerNumb: {
      get () {
        return this.$store.getters['currentStudy/viewerNumb']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerNumber', value)
      }
    },
    viewerLayoutCols: {
      get () {
        return this.$store.getters['currentStudy/viewerLayoutCols']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerLayoutCols', value)
      }
    },
    viewerHeight: {
      get () {
        return this.$store.getters['currentStudy/viewerHeight']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerHeight', value)
      }
    },
    viewerHeightAuto: {
      get () {
        return this.$store.getters['currentStudy/viewerHeightAuto']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerHeightAuto', value)
      }
    },
    viewerHeightAutoText: {
      get () {
        if (this.$store.getters['currentStudy/viewerHeightAuto']) {
          return 'auto'
        } else {
          return 'manual'
        }
      }
    },
    viewerWidth: {
      get () {
        return this.$store.getters['currentStudy/viewerWidth']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerWidth', value)
      }
    },
    viewerMetainfo: {
      get () {
        return this.$store.getters['currentStudy/viewerMetainfo']
      },
      set (value) {
        this.$store.commit('currentStudy/viewerMetainfo', value)
      }
    },
    viewerMetainfoText: {
      get () {
        if (this.$store.getters['currentStudy/viewerMetainfo']) {
          return 'show'
        } else {
          return 'hide'
        }
      }
    },
    backgroundColor: {
      get () {
        return this.$store.getters['currentStudy/backgroundColor']
      },
      set (value) {
        this.$store.commit('currentStudy/backgroundColor', value)
      }
    },
    textColor: {
      get () {
        return this.$store.getters['currentStudy/textColor']
      },
      set (value) {
        this.$store.commit('currentStudy/textColor', value)
      }
    },
    transitionTime: {
      get () {
        return this.$store.getters['currentStudy/transitionTime']
      },
      set (value) {
        this.$store.commit('currentStudy/transitionTime', value)
      }
    },
    buttonLabels: {
      get () {
        return this.$store.getters['currentStudy/buttonLabels']
      },
      set (value) {
        this.$store.commit('currentStudy/buttonLabels', value)
      }
    }
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>
</style>
