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
    <div id="general_settings_content" class="collapse show">
      <div class="mx-auto">
        <div class="input-group mx-auto" title="Controls max number of reference images">
          <label for="numb_refimg" class="input-group-text w-50">Ref-Image #</label>
          <select class="form-select" id="numb_refimg">
            <option value=""></option>
          </select>
        </div>

        <div class="input-group mx-auto" title="Controls max number of images">
          <label for="numb_img" class="input-group-text w-50">Image #</label>
          <select class="form-select" id="numb_img" v-model="viewerNumb">
            <option v-for="n in 20" :key="n">{{n}}</option>
          </select>
        </div>

        <div class="input-group mx-auto my-auto" title="Controls max number of images">
          <label for="numb_img" class="input-group-text w-50">Image Layout</label>
          <select class="form-select" id="numb_img">
            <option v-for="n in 5" :key="n">{{n}}</option>
          </select>
          x
          <select class="form-select" id="numb_img">
            <option v-for="n in 5" :key="n">{{n}}</option>
          </select>
        </div>

        <!-- window size -->
        <div class="input-group mx-auto"
          title="Controls the size (width, height) of the screen section used for displaying images.">
          <label class="input-group-text w-50">Viewport-Size</label>
          <input id="img_width" type="Number" step="any" class="image_size form-control" placeholder="width" />
          <input id="img_height" type="Number" step="any" class="image_size form-control" placeholder="height" />
        </div>

        <div class="input-group mx-auto" title="Controls the number of annotations (e.g. rois)
                    that need to be drawn by participants
                    before evaluating the next picture.
                    Set to 0 to allow any number.">
          <label for="numb_rois" class="input-group-text w-50">Annotation #</label>
          <input class="form-control" type="Number" step="any" id="numb_rois" min="0" />
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text w-50">Text Color</label>
          <input class="form-control" type="text" id="text_color" placeholder="Text-Color (Hex or Name)" value="" />
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text w-50">BG Color</label>
          <input class="form-control" type="text" id="background_color" placeholder="Background-Color (Hex or Name)"
            value="" />
        </div>

        <div class="input-group mx-auto" title="Time (sec) the screen will be blank between two image-sets.">
          <label class="input-group-text w-50">Transition Time</label>
          <input class="form-control" type="number" min="0" name="instructions" id="transition_time" placeholder="sec"
            value="" />
        </div>

        <div class="row input-group mx-auto"
          title="Controls the text of the buttons displayed beneath each image to continue to the next image-set.">
          <label class="input-group-text w-50">Button Label</label>
          <input class="form-control" type="text" name="buttonLabels" id="button_labels" placeholder="Btn Label" />
        </div>

        <div class="input-group row mx-auto"
          title="Controls if image settings such as windowing or zoom level are displayed.">
          <label class="input-group-text w-50">Img Metadata</label>
          <input type="button btn" name="show_display" id="show_viewport_info" class="form-control" />
        </div>

        <!-- Save Design Settings -->
          <div class="form-group">
            <button class="input-group-text btn btn-success btn-lg btn-block mt-1 w-100" id="submit_design">Save Design</button>
          </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    viewerNumb: {
      get () {
        return this.$store.state.open_study ? Number(this.$store.state.open_study.design.numb_img) : undefined
      },
      set (value) {
        this.$store.commit('updateNumbViewer', value)
      }
    },
    viewerLayoutColNumb: {
      get () {
        return this.$store.state.open_study ? Number(this.$store.state.open_study.design.layout_img_col) : undefined
      },
      set (value) {
        this.$store.commit('updateViewerLayoutColNumb', value)
      }
    }
  }
}
</script>

<style>
</style>
