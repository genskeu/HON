<template>
  <div>
    <!-- default viewport settings -->
    <div id="viewport_settings_container" class="w-100" title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                    Each viewport can be controlled individually.
                    To globally control viewport settings use the defaults submenu.">
      <div class="row mt-1 mx-auto">
        <button class="btn btn-dark col-12 mb-2" data-bs-toggle="collapse" data-bs-target="#viewport_settings"
          aria-expanded="true" aria-controls="viewport_settings">
          <h4 class="w-100 mt-1" id="imgset_btn">Image Viewer &#9776;</h4>
        </button>
      </div>
    </div>
    <div id="viewport_settings" class="mb-3 collapse show">
      <button class="btn btn-secondary btn-block" data-bs-toggle="collapse" data-bs-target="#viewport_def"
        aria-expanded="true" aria-controls="viewport_def">
        <h5 class="mt-1 col-12">Defaults</h5>
      </button>
      <div id="viewport_def" class="collapse">
        <!-- ww/wc -->
        <div class="row mx-auto">
          <div class="input-group">
            <div class="input-group-prepend col-4 px-0 mx-0">
              <span class="input-group-text col-12">WW/WC</span>
            </div>
            <input id="def_ww" type="Number" step="any" min="0" class="form-control def_ww viewport_prop_def"
              placeholder="WW" />
            <input id="def_wc" type="Number" step="any" min="0" class="form-control def_wc viewport_prop_def"
              placeholder="WC" />
          </div>
        </div>
        <!-- zoom -->
        <div class="row mx-auto">
          <div class="input-group">
            <div class="input-group-prepend col-4 px-0 mx-0">
              <span class="input-group-text col-12">Zoom</span>
            </div>
            <input id="def_zoom" type="Number" step="any" min="0.0" class="form-control def_zoom viewport_prop_def"
              placeholder="Zoom" />
          </div>
        </div>
        <!-- position -->
        <div class="row mx-auto">
          <div class="input-group">
            <div class="input-group-prepend col-4 px-0 mx-0">
              <span class="input-group-text col-12">Pos</span>
            </div>
            <input id="def_pos_x" type="Number" step="any" class="form-control def_pos_x viewport_prop_def"
              placeholder="x" />
            <input id="def_pos_y" type="Number" step="any" class="form-control def_pos_y viewport_prop_def"
              placeholder="y" />
          </div>
        </div>
        <div class="row mx-auto">
          <!-- position -->
          <button id="update_viewports" class="btn btn-light col-12">
            update existing image-sets
          </button>
        </div>
      </div>

      <div class="mx-auto" id="viewports">
        <!-- viewport info -->
        <div id="viewports_man_container">
          <div id="viewports_auto_container">
            <div id="viewport_info_">
              <div class="row mx-auto mt-1">
                <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#viewport_"
                  aria-expanded="true" aria-controls="viewport_">
                  <h5 class="mt-1">Viewer</h5>
                </button>
              </div>

              <div id="viewport_" class="collapse">
                <!-- windowing -->
                <div class="row mx-auto">
                  <div class="input-group">
                    <div class="input-group-prepend col-4 px-0 mx-0">
                      <span class="input-group-text col-12">WW/WC</span>
                    </div>
                    <input id="ww_" type="Number" step="any" min="0" class="form-control ww viewport_prop"
                      placeholder="WW" />
                    <input id="wc_" type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC" />
                  </div>
                </div>
                <!-- window zoom -->
                <div class="row mx-auto">
                  <div class="input-group">
                    <div class="input-group-prepend col-4 px-0 mx-0">
                      <span class="input-group-text col-12">Zoom</span>
                    </div>
                    <input id="zoom_" type="Number" step="any" min="0.0" class="form-control zoom viewport_prop"
                      placeholder="Zoom" />
                  </div>
                </div>
                <!-- window position -->
                <div class="row mx-auto">
                  <div class="input-group">
                    <div class="input-group-prepend col-4 px-0 mx-0">
                      <span class="input-group-text col-12">Pos</span>
                    </div>
                    <input id="pos_x_" type="Number" step="any" class="form-control pos_x viewport_prop"
                      placeholder="x" />
                    <input id="pos_y_" type="Number" step="any" class="form-control pos_y viewport_prop"
                      placeholder="y" />
                  </div>
                </div>
                <!--reset buttons -->
                <button id="reset_" class="btn btn-block btn-light reset">
                  reset
                </button>
              </div>
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
