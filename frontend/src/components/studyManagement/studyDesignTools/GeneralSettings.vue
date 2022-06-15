<template>
  <div>
    <!-- General Settings -->
          <div class="row mx-auto mt-1">
            <button
              class="btn-secondary btn col-12"
              data-bs-toggle="collapse"
              data-bs-target="#general_settings"
              aria-expanded="true"
              aria-controls="general_settings"
              title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously."
            >
              <h5 class="mt-1">General Settings</h5>
            </button>
          </div>
          <div id="general_settings" class="collapse">
            <div class="mx-auto">
              <div
                class="input-group row mx-auto"
                title="Controls max number of reference images"
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Ref-Images</span>
                </div>
                <select class="custom-select" id="numb_refimg">
                  <option value=""></option>
                </select>
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls the number of images (m-AFC tests)"
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Images</span>
                </div>
                <select class="custom-select" id="numb_img">
                  <option value=""></option>
                </select>
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls the number of annotations (e.g. rois)
                    that need to be drawn by participants
                    before evaluating the next picture.
                    Set to 0 to allow any number."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Annotations</span>
                </div>
                <input
                  class="form-control"
                  type="Number"
                  step="any"
                  id="numb_rois"
                  min="0"
                />
              </div>

              <!-- window size -->
              <div class="row mx-auto">
                <div
                  class="input-group"
                  title="Controls the size (width, height) of the screen section used for displaying images."
                >
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Viewport-Size</span>
                  </div>
                  <input
                    id="img_width"
                    type="Number"
                    step="any"
                    class="image_size form-control"
                    placeholder="width"
                  />
                  <input
                    id="img_height"
                    type="Number"
                    step="any"
                    class="image_size form-control"
                    placeholder="height"
                  />
                </div>
              </div>

              <div class="input-group row mx-auto">
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Text Color</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  id="text_color"
                  placeholder="Text-Color (Hex or Name)"
                  value=""
                />
              </div>

              <div class="input-group row mx-auto">
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">BG Color</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  id="background_color"
                  placeholder="Background-Color (Hex or Name)"
                  value=""
                />
              </div>

              <div
                class="input-group row mx-auto"
                title="Time (sec) the screen will be blank between two image-sets."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Transition Time</span>
                </div>
                <input
                  class="form-control"
                  type="number"
                  min="0"
                  name="instructions"
                  id="transition_time"
                  placeholder="sec"
                  value=""
                />
              </div>

              <div
                class="row input-group mx-auto"
                title="Controls the text of the buttons displayed beneath each image to continue to the next image-set."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Button Label</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  name="buttonLabels"
                  id="button_labels"
                  placeholder="Btn Label"
                />
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls if image settings such as windowing or zoom level are displayed."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Img Viewer Info</span>
                </div>
                <input
                  type="button"
                  name="show_display"
                  id="show_viewport_info"
                />
              </div>
            </div>
          </div>
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>