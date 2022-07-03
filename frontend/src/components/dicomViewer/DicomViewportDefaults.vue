<template>
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
</template>

<script>
export default {

}
</script>

<style>

</style>