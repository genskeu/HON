<template>
  <div id="general_settings">
    <!-- General Settings -->
    <div class="row mx-auto mt-1" id="general_settings_title">
      <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#general_settings_content"
        aria-expanded="true" aria-controls="general_settings_content"
        title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
        <h5 class="mt-1">General Settings</h5>
      </button>
    </div>
    <div id="general_settings_content" class="collapse">
      <div class="mx-auto">
        <div class="input-group mx-auto" title="Controls max number of reference images">
          <label for="numb_refimg" class="input-group-text w-50">RefImg Viewer #</label>
          <input class="form-control" type="Number" min="0" max="2" id="numb_refimg" v-model="refviewerNumb"/>
        </div>

        <div class="input-group mx-auto" title="Controls max number of images">
          <label for="numb_img" class="input-group-text w-50">Img Viewer #</label>
          <input class="form-control" type="Number" min="1" max="50" id="numb_img" v-model="viewerNumb"/>
        </div>

        <div class="input-group mx-auto my-auto" title="Controls max number of images">
          <label for="numb_img" class="input-group-text w-50">Viewer Layout</label>
          <input type="number" min="1" max="5" class="form-control" id="numb_img_cols" v-model="viewerLayoutCols"/>
        </div>

        <!-- window size -->
        <div class="input-group mx-auto"
          title="Controls the size (width, height) of the screen section used for displaying images.">
          <label class="input-group-text w-50">Set Viewer Size</label>
          <div class="form-check form-switch form-control mb-0">
            <input class="form-check-input" type="checkbox" id="viewerHeightAuto" v-model="viewerHeightAuto">
            <label class="form-check-label" for="viewerHeightAuto">{{viewerHeightAutoText}}</label>
          </div>
        </div>

        <div v-if="!viewerHeightAuto" class="input-group mx-auto"
          title="Controls the size (width, height) of the screen section used for displaying images.">
          <label class="input-group-text w-50">Size in px</label>
          <!-- <button :class='viewerHeightAutoBtnDesign' @click='setViewerHeightAuto'>{{viewerHeightAuto}}</button> -->
          <input id="img_height" type="Number" step="any" min="1" class="image_size form-control" placeholder="height" v-model="viewerHeight"/>
        </div>

        <div class="input-group row mx-auto"
          title="Controls if image settings such as windowing or zoom level are displayed.">
          <label class="input-group-text w-50">Viewer Metadata</label>
          <div class="form-check form-switch form-control mb-0">
            <input class="form-check-input" type="checkbox" id="viewerHeightAuto" v-model="viewerMetainfo">
            <label class="form-check-label" for="viewerHeightAuto">{{viewerMetainfoText}}</label>
          </div>
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text w-50">Text Color</label>
          <input class="form-control" type="text" id="text_color" placeholder="Text-Color (Hex or Name)" v-model="textColor" />
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text w-50">BG Color</label>
          <input class="form-control" type="text" id="background_color" placeholder="Background-Color (Hex or Name)"
            v-model="backgroundColor" />
        </div>

        <div class="input-group mx-auto" title="Time (sec) the screen will be blank between two image-sets.">
          <label class="input-group-text w-50">Transition Time</label>
          <input class="form-control" type="number" min="0" name="instructions" id="transition_time" placeholder="sec"
            v-model="transitionTime" />
        </div>

        <div class="row input-group mx-auto"
          title="Controls the text of the buttons displayed beneath each image to continue to the next image-set.">
          <label class="input-group-text w-50">Button Label</label>
          <input class="form-control" type="text" name="buttonLabels" id="button_labels" placeholder="Btn Label" v-model="buttonLabels" />
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
        return this.$store.getters['openStudy/refviewerNumb']
      },
      set (value) {
        this.$store.commit('openStudy/refviewerNumber', value)
      }
    },
    viewerNumb: {
      get () {
        return this.$store.getters['openStudy/viewerNumb']
      },
      set (value) {
        this.$store.commit('openStudy/viewerNumber', value)
      }
    },
    viewerLayoutCols: {
      get () {
        return this.$store.getters['openStudy/viewerLayoutCols']
      },
      set (value) {
        this.$store.commit('openStudy/viewerLayoutCols', value)
      }
    },
    viewerHeight: {
      get () {
        return this.$store.getters['openStudy/viewerHeight']
      },
      set (value) {
        this.$store.commit('openStudy/viewerHeight', value)
      }
    },
    viewerHeightAuto: {
      get () {
        return this.$store.getters['openStudy/viewerHeightAuto']
      },
      set (value) {
        this.$store.commit('openStudy/viewerHeightAuto', value)
      }
    },
    viewerHeightAutoText: {
      get () {
        if (this.$store.getters['openStudy/viewerHeightAuto']) {
          return 'automatically'
        } else {
          return 'manual'
        }
      }
    },
    viewerWidth: {
      get () {
        return this.$store.getters['openStudy/viewerWidth']
      },
      set (value) {
        this.$store.commit('openStudy/viewerWidth', value)
      }
    },
    viewerMetainfo: {
      get () {
        return this.$store.getters['openStudy/viewerMetainfo']
      },
      set (value) {
        this.$store.commit('openStudy/viewerMetainfo', value)
      }
    },
    viewerMetainfoText: {
      get () {
        if (this.$store.getters['openStudy/viewerMetainfo']) {
          return 'show'
        } else {
          return 'hidden'
        }
      }
    },
    backgroundColor: {
      get () {
        return this.$store.getters['openStudy/backgroundColor']
      },
      set (value) {
        this.$store.commit('openStudy/backgroundColor', value)
      }
    },
    textColor: {
      get () {
        return this.$store.getters['openStudy/textColor']
      },
      set (value) {
        this.$store.commit('openStudy/textColor', value)
      }
    },
    transitionTime: {
      get () {
        return this.$store.getters['openStudy/transitionTime']
      },
      set (value) {
        this.$store.commit('openStudy/transitionTime', value)
      }
    },
    buttonLabels: {
      get () {
        return this.$store.getters['openStudy/buttonLabels']
      },
      set (value) {
        this.$store.commit('openStudy/buttonLabels', value)
      }
    }
  },
  methods: {
  }
}
</script>

<style>
</style>
