<template>
  <div class="container-fluid mt-4" id="content">
    <div class="row mx-auto h-100">
      <!-- Imgsets -->
      <div class="col-lg-10 mb-2 h-100">
        <div class="row w-100 mx-auto">
          <button
            class="btn btn-dark mb-2"
            data-bs-toggle="collapse"
            data-bs-target="#imgset_creation"
            aria-expanded="true"
            aria-controls="imgset_creation"
          >
            <h4 class="mt-1">Image Sets &#9776;</h4>
          </button>
        </div>
        <!-- Create Image Sets -->
        <div id="imgset_creation" class="collapse show row mx-auto">
          <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
          <div id="imgset" class="w-100">
            <!--Images -->
            <!-- <div id="ref_images">
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Reference Image Stack(s)</h4>
              </span>
            </div> -->
              <span class="badge bg-secondary w-100 mb-2">
                <h4 class="mt-1">Image Stack(s)</h4>
              </span>
                <div id="comp_images" class="relative grid flex grid-cols-1 grid-rows-1">
                    <dicom-viewer v-for="index in viewerNumb" :key="index"></dicom-viewer>
                </div>
            <!-- modify buttons -->
            <div id="imgset_buttons">
              <div class="row mt-3 mb-2">
                <div class="col-lg-12 text-center">
                  <button
                    value="append imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="add_imgset"
                    title="add image-set to the end of the study"
                  >append imgset</button>
                  <input
                    value="insert imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="insert_imgset"
                    title="inserts image-set at the currently selected position"
                  />
                  <input
                    value="update imgset"
                    class="imgset_btn btn-light btn col-lg-2"
                    id="upd_imgset"
                    title="update currently selected image-set"
                  />
                  <input
                    value="delete imgset"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_imgset"
                    title="delete currently selected image-set"
                  />
                  <input
                    value="delete all imgsets"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_all_imgsets"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2">
        <!-- Design Settings -->
        <div class="row mx-auto">
          <button
            class="btn btn-dark col-12 mb-1"
            data-bs-toggle="collapse"
            data-bs-target="#design_settings"
            title="Click on the sections to expand the sub-menus.
                    Study design options were divided into general settings, tools, instructions and scales.
                    After changing any design options dont forget to press the Save Design button.
                              "
            aria-expanded="true"
            aria-controls="design_settings"
          >
            <h4 class="w-100 mt-1">Design Options &#9776;</h4>
          </button>
        </div>
        <div id="design_settings" class="collapse show">
          <!-- Save Design Settings -->
          <form method="post">
            <div class="form-group">
              <input
                class="btn btn-light btn-lg btn-block mt-1 w-100"
                type="button"
                id="submit_design"
                value="Save Design"
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'

export default {
  name: 'Design',
  components: {
    DicomViewer
  },
  computed: {
    viewerNumb: {
      get () {
        return this.$store.state.open_study ? Number(this.$store.state.open_study.design.numb_img) : undefined
      },
      set (value) {
        this.$store.commit('updateNumbViewer', value)
      }
    }
  }
}
</script>

<style>
</style>
