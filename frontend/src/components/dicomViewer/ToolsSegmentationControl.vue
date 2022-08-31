<template>
  <div>
        <!--Segmentations-->
        <div
          id="seg_settings_container"
          class="w-100 mb-1"
          style="display: none"
          title=""
        >
          <div class="row mx-auto roi_input">
            <button
              class="btn btn-dark col-12 mb-1"
              data-bs-toggle="collapse"
              data-bs-target="#seg_settings"
              aria-expanded="true"
              aria-controls="seg_settings"
            >
              <h4 class="w-100 mt-1">Segmentation &#9776;</h4>
            </button>
          </div>
          <div id="seg_settings" class="collapse mb-3 show">
            <!-- roi info -->
            <div class="mt-1">
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Brush-Size</span>
                  </div>
                  <input
                    type="Number"
                    min="1"
                    class="form-control col"
                    value="10"
                    id="brush_size"
                  />
                </div>
              </div>
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Label</span>
                  </div>
                  <input
                    type="Number"
                    min="1"
                    class="form-control col"
                    value="1"
                    id="seg_label"
                  />
                </div>
              </div>
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